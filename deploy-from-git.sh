#!/usr/bin/env bash
# deploy-from-git.sh — parsiunčia naujus commit'us ir paleidžia deploy-agent.sh.
#
# Skirtas systemd timeriui (žr. deploy/systemd/). Paleidžiamas dažnai, todėl
# TYLI, kai nėra ko daryti — jokių laiškų, jokio triukšmo žurnale.
#
# Saugikliai:
#   • flock — du deploy'ai vienu metu nesusidurs;
#   • švarus darbo katalogas privalomas — jei kas nors redagavo kodą serveryje,
#     nieko nedarom (deploy-agent.sh tokį darbą užtrintų);
#   • tik fast-forward — niekada nekuriam merge commit'ų ir neperrašom istorijos;
#   • jei deploy-agent.sh grąžina klaidą, jis PATS jau atkeitė failus iš
#     last_good, bet .git liktų rodyti į blogą commit'ą — todėl git atsukam
#     atgal, kad failai ir istorija vėl sutaptų.
#
# Rankinis paleidimas:  /root/autoleft/deploy-from-git.sh
# Žurnalas:             journalctl -u autoleft-deploy -n 50

set -euo pipefail

APP_DIR="${APP_DIR:-/root/autoleft}"
BRANCH="${DEPLOY_BRANCH:-master}"
REMOTE="${DEPLOY_REMOTE:-origin}"
LOCKFILE="${LOCKFILE:-/run/autoleft-deploy.lock}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
die() { log "❌ $*"; exit 1; }

# ── Vienas deploy'as vienu metu ────────────────────────────────────────
exec 9>"$LOCKFILE"
if ! flock -n 9; then
    log "Kitas deploy'as dar sukasi — praleidžiam šį ciklą."
    exit 0
fi

cd "$APP_DIR" || die "Nerastas $APP_DIR"
[[ -x ./deploy-agent.sh ]] || die "Nerastas vykdomas ./deploy-agent.sh"

# ── Ar yra ko parsisiųsti? ─────────────────────────────────────────────
git fetch --quiet "$REMOTE" "$BRANCH" || die "git fetch nepavyko (patikrink prieigą prie $REMOTE)"

LOCAL="$(git rev-parse HEAD)"
UPSTREAM="$(git rev-parse "${REMOTE}/${BRANCH}")"

# Commit'as, kuris jau krito per patikrą — nekartojam jo kas minutę.
# Naujas commit'as žymę nuvalo (upstream pajudėjo).
BLOGAS_FAILAS="${APP_DIR}/deploy/.blogas-commitas"
if [[ -f "$BLOGAS_FAILAS" ]] && [[ "$(cat "$BLOGAS_FAILAS")" == "$UPSTREAM" ]]; then
    exit 0
fi

if [[ "$LOCAL" == "$UPSTREAM" ]]; then
    # Naujo kodo nėra, bet būklę paskelbiam — taip ją matyti ir tada,
    # kai niekas nediegiama. Skriptas pats nieko nekelia, jei nepasikeitė.
    if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh >/dev/null 2>&1 || true; fi
    exit 0
fi

# ── Nuo šios vietos jau turim ką pranešti ──────────────────────────────
log "=== Naujų commit'ų rasta: ${LOCAL:0:7} → ${UPSTREAM:0:7} ==="
git --no-pager log --oneline "HEAD..${REMOTE}/${BRANCH}" | sed 's/^/    /'

# Ar dabartinė šaka apskritai ta, kurią diegiam?
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$CURRENT_BRANCH" == "$BRANCH" ]] || \
    die "Serveryje iškrauta šaka '$CURRENT_BRANCH', o diegiam '$BRANCH'. Nieko nedarom."

# Nešvarus katalogas = kažkas redagavo kodą serveryje. Deploy tai užtrintų.
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
    log "Nesucommit'inti pakeitimai serveryje:"
    git --no-pager status --short --untracked-files=no | sed 's/^/    /'
    die "Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka."
fi

# ── Parsisiunčiam (tik fast-forward) ───────────────────────────────────
if ! git merge --ff-only "${REMOTE}/${BRANCH}" --quiet; then
    die "Fast-forward negalimas — serverio šaka nuklydusi nuo ${REMOTE}/${BRANCH}. Sutvarkyk ranka."
fi
log "Kodas atnaujintas iki ${UPSTREAM:0:7}"

# ── Migracijos PRIEŠ patikrą ───────────────────────────────────────────
# Patikros testai (config.test_runner.BeDuombazes) dirba su GYVA duomenų
# baze — testinės kurti neleidžia teisės. Todėl naujas modelio laukas
# užrakindavo diegimą lygiai taip pat, kaip naujas statinis failas:
#
#   ProgrammingError: column listings_listing.axle_count does not exist
#
# Kodas lauko jau prašo, migracija jį pridėtų — bet ji sukdavosi tik
# deploy-agent.sh viduje, JAU PO patikros. Patikra krisdavo, kodas
# atsukamas, migracija taip ir nepaleidžiama, kitas bandymas krinta taip
# pat. 2026-09 taip užstrigo 19 commit'ų (pirma dėl statinių manifesto,
# paskui dėl šito).
#
# Todėl migracijas paleidžiam pirma. Jos yra pridedančios (AddField,
# AlterField), o senas kodas papildomo stulpelio nemato ir juo
# nesiskundžia — tad jei patikra po to kristų, kodą atsukam, o duomenų
# bazė lieka su nauju stulpeliu ir svetainė veikia toliau. ĮSPĖJIMAS
# rašomas į žurnalą, kad niekas nemanytų, jog DB visai nepaliesta.
#
# Kas duomenis TRINA (RemoveField, DeleteModel), tas per šitą kelią
# neturi eiti — tokią migraciją leisk ranka ir stebėk.
if [[ -x ./venv/bin/python ]]; then
    if MIGRACIJOS="$(./venv/bin/python manage.py migrate --noinput 2>&1)"; then
        # „if … fi" be tinkančios šakos grąžina 0, tad `set -e` nenukerta
        # deploy'o vien todėl, kad migracijų nebuvo.
        if echo "$MIGRACIJOS" | grep -q "Applying "; then
            log "Migracijos pritaikytos:"
            echo "$MIGRACIJOS" | grep "Applying " | sed 's/^/    /'
        fi
    else
        echo "$MIGRACIJOS" | tail -20 | sed 's/^/    /'
        echo "$UPSTREAM" > "$BLOGAS_FAILAS"
        git reset --hard "$LOCAL" --quiet || log "DĖMESIO: git reset nepavyko"
        die "Migracijos krito — grąžinta į ${LOCAL:0:7}. Kito bandymo su tuo pačiu commit'u nebus."
    fi
else
    log "DĖMESIO: nerastas ./venv/bin/python — migracijos praleistos"
fi

# ── Patikra PRIEŠ liečiant produkciją ──────────────────────────────────
# Šablonų nuotėkis ir testai tikrinami dar prieš perkrovimą: jei krenta,
# kodas atsukamas atgal, o gunicorn net nesujudinamas.
if [[ -x ./scripts/patikra.sh ]]; then
    if PATIKRA="$(./scripts/patikra.sh 2>&1)"; then
        log "Patikra praėjo"
    else
        echo "$PATIKRA" | tail -20 | sed 's/^/    /'
        echo "$UPSTREAM" > "$BLOGAS_FAILAS"
        git reset --hard "$LOCAL" --quiet || log "DĖMESIO: git reset nepavyko"
        if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh >/dev/null 2>&1 || true; fi
        log "DĖMESIO: migracijos jau pritaikytos — DB liko naujesnė nei kodas (pridedančios, todėl senas kodas veikia)."
        die "Patikra krito — grąžinta į ${LOCAL:0:7}, gunicorn nepaliestas. Kito bandymo su tuo pačiu commit'u nebus."
    fi
else
    log "DĖMESIO: scripts/patikra.sh nerastas — diegiam be testų"
fi
rm -f "$BLOGAS_FAILAS"

# ── Deploy per esamą agentą (migrate + collectstatic + restart + health) ──
if ./deploy-agent.sh; then
    log "✅ Deploy OK — gyvai veikia ${UPSTREAM:0:7}"
    if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh || true; fi
    exit 0
fi

# Nekartojam to paties commit'o kas minutę.
#
# Žymė iki šiol buvo rašoma TIK tada, kai krisdavo scripts/patikra.sh. Kai
# krisdavo pats deploy-agent.sh, taimeris kas minutę bandydavo tą patį
# commit'ą iš naujo — ir kas minutę atsukdavo kodą. 2026-09-01 būtent taip
# „dingo" keturi darbai iš eilės: taimeris nebuvo sustojęs, jis sukosi.
#
# Žymę nuvalo naujas commit'as (žr. viršuje) arba ranka:
#     rm -f deploy/.blogas-commitas && ./deploy-from-git.sh
echo "$UPSTREAM" > "$BLOGAS_FAILAS"
log "Žymė įrašyta: ${UPSTREAM:0:7} daugiau nebandomas."
log "Kartoti: rm -f ${BLOGAS_FAILAS} && ${APP_DIR}/deploy-from-git.sh"

# deploy-agent.sh jau grąžino FAILUS iš last_good; suderinam ir git istoriją.
log "deploy-agent.sh grąžino klaidą — atsukam git į ${LOCAL:0:7}, kad failai ir istorija sutaptų."
git reset --hard "$LOCAL" --quiet || log "DĖMESIO: git reset nepavyko — reikia rankinio įsikišimo."
if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh || true; fi
die "Deploy nepavyko. Žr. aukščiau esantį health check'o žurnalą."
