#!/usr/bin/env bash
# deploy-from-git.sh — parsiunčia naujus commit'us ir paleidžia deploy-agent.sh.
#
# Skirtas systemd timeriui (žr. deploy/systemd/). Paleidžiamas dažnai, todėl
# TYLI, kai nėra ko daryti — jokių laiškų, jokio triukšmo žurnale.
#
# Saugikliai:
#   • flock — du deploy'ai vienu metu nesusidurs;
#   • švarus darbo katalogas privalomas — jei kas nors redagavo KODĄ serveryje,
#     nieko nedarom (deploy-agent.sh tokį darbą užtrintų); docs/ pakeitimai
#     deploy'o nestabdo — padedami į stash'ą (žr. komentarą ties vartais);
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

# Žurnalas rašomas ir į failą, ne tik į journald: `journalctl` pasiekiamas
# ne visiems ir ne iš visur, o klausimas „kodėl svetainėje senas kodas"
# užduodamas dažnai. Failas rotuojamas paprastai — laikom 200 paskutinių
# tūkstančių eilučių, daugiau nereikia.
ZURNALAS="${ZURNALAS:-/var/log/autoleft-deploy.log}"
mkdir -p "$(dirname "$ZURNALAS")" 2>/dev/null || true
log() {
    local eil="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$eil"
    echo "$eil" >> "$ZURNALAS" 2>/dev/null || true
}
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
# Bet NE tyliai: 2026-09-23..24 taip buvo atmesta 13 commit'ų iš eilės, o
# servisas kas minutę rodė „status=0/SUCCESS" — niekas nepastebėjo. Kol
# master neįdiegtas, unit'as lieka „failed" (matosi `systemctl --failed`).
if [[ -f "$BLOGAS_FAILAS" ]] && [[ "$(cat "$BLOGAS_FAILAS")" == "$UPSTREAM" ]]; then
    IDIEGTA_DABAR="$(tr -d '[:space:]' < "${APP_DIR}/VERSIJA" 2>/dev/null || true)"
    if [[ "${UPSTREAM:0:12}" == "$IDIEGTA_DABAR" ]]; then
        exit 0   # ranka jau įdiegta — žymė nebeaktuali
    fi
    echo "UŽBLOKUOTA: ${UPSTREAM:0:12} krito per patikrą, gyvai ${IDIEGTA_DABAR:-?}. Žr. /var/log/autoleft-deploy.log; po pataisymo naujas commit'as žymę nuvalo." >&2
    exit 1
fi

# ── Ar ĮDIEGTA tai, kas guli diske? ────────────────────────────────────
#
# 2026-09-13..15 svetainė septynias paras rodė seną kodą, nors serverio
# git buvo ant naujausio commit'o, o servisas kas minutę baigdavosi
# `status=0/SUCCESS`. Kaltas šitas palyginimas: jis klausė „ar git HEAD
# sutampa su upstream", o ne „ar tai, kas guli diske, tikrai atiduodama
# lankytojui".
#
# Eiga tokia. Žemiau `git merge --ff-only` darbo katalogą pastumia PIRMA,
# o gunicorn perkraunamas tik pabaigoje (deploy-agent.sh). Kai systemd
# nutraukė vieną paleidimą per vidurį (13:10:00, „Failed with result
# 'timeout'"), medis jau buvo pastumtas, o perkrovimas nebeįvyko. Nuo tos
# akimirkos LOCAL == UPSTREAM, tad kiekvienas kitas ciklas išeidavo čia —
# tyliai ir „sėkmingai". Diegimas nebeįvyktų NIEKADA: klaida pati save
# palaiko.
#
# Todėl tikrinam ne tik git, bet ir VERSIJA — žymę, kurią rašo
# deploy-agent.sh TADA, kai tikrai perkrovė aplikaciją. Jei ji atsilieka
# nuo darbo katalogo, diegimas liko nebaigtas ir jį reikia pabaigti.
HEAD_TRUMPAS="$(git rev-parse --short=12 HEAD)"
IDIEGTA="$(tr -d '[:space:]' < "${APP_DIR}/VERSIJA" 2>/dev/null || true)"
NEBAIGTAS=0
if [[ -n "$IDIEGTA" && "$IDIEGTA" != "$HEAD_TRUMPAS" ]]; then
    NEBAIGTAS=1
fi

# Serveris gali būti PRIEŠ upstream (commit'inta serveryje, push dar
# neįvyko). Tai ne „nauji commit'ai" — be šito kiekvienas ciklas darytų
# pilną diegimą (DB kopija + restart), kol push nepavyks.
if [[ "$LOCAL" != "$UPSTREAM" ]] && git merge-base --is-ancestor "$UPSTREAM" "$LOCAL"; then
    UPSTREAM="$LOCAL"
fi

if [[ "$LOCAL" == "$UPSTREAM" && "$NEBAIGTAS" -eq 0 ]]; then
    # Naujo kodo nėra ir įdiegta tai, kas guli diske. Būklę paskelbiam —
    # taip ją matyti ir tada, kai niekas nediegiama.
    if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh >/dev/null 2>&1 || true; fi
    exit 0
fi

# ── Nuo šios vietos jau turim ką pranešti ──────────────────────────────
if [[ "$NEBAIGTAS" -eq 1 ]]; then
    log "=== NEBAIGTAS DIEGIMAS: diske ${HEAD_TRUMPAS}, o įdiegta ${IDIEGTA} — tęsiam ==="
fi
if [[ "$LOCAL" != "$UPSTREAM" ]]; then
    log "=== Naujų commit'ų rasta: ${LOCAL:0:7} → ${UPSTREAM:0:7} ==="
    git --no-pager log --oneline "HEAD..${REMOTE}/${BRANCH}" | sed 's/^/    /'
fi

# Ar dabartinė šaka apskritai ta, kurią diegiam?
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$CURRENT_BRANCH" == "$BRANCH" ]] || \
    die "Serveryje iškrauta šaka '$CURRENT_BRANCH', o diegiam '$BRANCH'. Nieko nedarom."

# Nešvarus katalogas = kažkas redagavo kodą serveryje. Deploy tai užtrintų.
#
# 2026-09: būtent čia deploy'as ir užstrigo 8 paroms. Serveryje dirbantys
# agentai rašo pastabas į docs/klaidos/*.md, tie failai yra sekami, ir
# kiekvienas timerio ciklas — kas 5 min, apie 11 000 kartų — krisdavo ties
# šia patikra. Tekstinis žinynas stabdė KODO diegimą.
#
# Todėl vartai dabar skiria du dalykus:
#   • kodo pakeitimas (viskas ne docs/) — sustojam, kaip ir anksčiau;
#   • vien dokumentacija (docs/) — pasidedam į stash'ą ir tęsiam.
#
# Kodėl ne .gitignore: failai JAU sekami, o sekamam failui .gitignore
# negalioja. Kad galiotų, tektų `git rm --cached`, t. y. išimti žinyną iš
# repo — tada jo nebematytų nei kiti konteineriai, nei kitos sesijos, o
# būtent dėl to jis ir rašomas. Turinys niekur nedingsta: `git stash`
# saugo jį git objektuose, atkuriama su `git stash pop`.
NESVARU="$(git status --porcelain --untracked-files=no)"
if [[ -n "$NESVARU" ]]; then
    KODAS="$(printf '%s\n' "$NESVARU" | grep -v ' docs/' || true)"
    if [[ -n "$KODAS" ]]; then
        log "Nesucommit'inti KODO pakeitimai serveryje:"
        printf '%s\n' "$KODAS" | sed 's/^/    /'
        die "Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka."
    fi
    log "Dokumentacijos pakeitimai serveryje (deploy'o nestabdo):"
    printf '%s\n' "$NESVARU" | sed 's/^/    /'
    if git stash push --quiet -m "deploy $(date '+%Y-%m-%d %H:%M') — docs serveryje" -- docs/; then
        log "Padėta į stash'ą; atkuriama su: git -C ${APP_DIR} stash pop"
    else
        die "Nepavyko padėti docs/ į stash'ą — sutvarkyk ranka."
    fi
    # Jei po to kas nors liko — vadinasi, ne docs/, ir toliau neinam.
    LIKO="$(git status --porcelain --untracked-files=no)"
    [[ -z "$LIKO" ]] || { printf '%s\n' "$LIKO" | sed 's/^/    /'
                          die "Katalogas vis tiek nešvarus — sutvarkyk ranka."; }
fi

# ── Parsisiunčiam (tik fast-forward) ───────────────────────────────────
if [[ "$LOCAL" != "$UPSTREAM" ]]; then
    if ! git merge --ff-only "${REMOTE}/${BRANCH}" --quiet; then
        die "Fast-forward negalimas — serverio šaka nuklydusi nuo ${REMOTE}/${BRANCH}. Sutvarkyk ranka."
    fi
    log "Kodas atnaujintas iki ${UPSTREAM:0:7}"
fi

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
# ── DB kopija PRIEŠ migracijas ─────────────────────────────────────────
# Kopija iki šiol buvo daroma deploy-agent.sh viduje, o tas paleidžiamas
# TIK PO migracijų (žr. žemiau). Vadinasi, blogos migracijos atveju
# atstatyti buvo ne iš ko: pirmas dumpas jau turėjo pakeistą schemą.
#
# Kopiją ima tas pats agentas su --tik-db-kopija, kad pg_dump logika
# liktų vienoje vietoje (nustatymai skaitomi iš Django, ne perrašomi).
#
# Jei kopija nepavyksta — MIGRACIJŲ NELEIDŽIAM. Geriau nediegti, nei
# migruoti be tinklo po kojomis.
if [[ -x ./deploy-agent.sh ]]; then
    if ./deploy-agent.sh --tik-db-kopija; then
        log "DB kopija prieš migracijas paimta"
    else
        echo "$UPSTREAM" > "$BLOGAS_FAILAS"
        git reset --hard "$LOCAL" --quiet || log "DĖMESIO: git reset nepavyko"
        die "DB kopija nepavyko — migracijų neleidžiam, grąžinta į ${LOCAL:0:7}."
    fi
fi

# ── Duomenis keičiančios migracijos — TIK ranka ────────────────────────
# Aukščiau parašyta „kas duomenis TRINA, per šitą kelią neturi eiti", bet
# niekas to netikrino. 2026-09-24 18:52 taip automatiškai prasisuko
# 0107 (RunPython, išvalė contact_phone), o patikra po jos krito ir kodas
# buvo atsuktas — DB liko pakeista, gyvai sukosi senas kodas.
# Todėl žiūrim į planą (--plan nieko nevykdo) ir tokių migracijų neleidžiam.
if [[ -x ./venv/bin/python ]]; then
    PLANAS="$(./venv/bin/python manage.py migrate --plan 2>&1 || true)"
    PAVOJINGOS="$(printf '%s\n' "$PLANAS" \
        | grep -E 'Raw Python operation|Raw SQL operation|Remove field|Delete model' || true)"
    if [[ -n "$PAVOJINGOS" ]]; then
        printf '%s\n' "$PLANAS" | sed 's/^/    /'
        echo "$UPSTREAM" > "$BLOGAS_FAILAS"
        git reset --hard "$LOCAL" --quiet || log "DĖMESIO: git reset nepavyko"
        if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh >/dev/null 2>&1 || true; fi
        die "Duomenis keičianti migracija — automatiškai neleidžiam. Grąžinta į ${LOCAL:0:7}. Ranka: pg_dump į /root/backups/, git merge --ff-only origin/${BRANCH}, ./deploy-agent.sh"
    fi
fi

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
    # „Skriptas nenukrito" NĖRA tas pats, kas „naujas kodas atiduodamas".
    # Septynias paras diegimas baigdavosi sėkme, o lankytojas matė seną
    # kodą. Todėl pabaigoje klausiam PAČIOS svetainės, kuris commit'as
    # gyvas, ir tik tada skelbiam sėkmę.
    LAUKIAMA="$(git rev-parse --short=12 HEAD)"
    GYVAI=""
    for _bandymas in 1 2 3 4 5; do
        GYVAI="$(curl -fsS --max-time 10 -H 'X-Forwarded-Proto: https' \
                     http://127.0.0.1/ 2>/dev/null \
                 | grep -o 'name="versija" content="[0-9a-f]*"' \
                 | grep -o '[0-9a-f]\{6,\}' || true)"
        [[ "$GYVAI" == "$LAUKIAMA" ]] && break
        sleep 2
    done

    if [[ "$GYVAI" == "$LAUKIAMA" ]]; then
        log "✅ Deploy OK — GYVAI veikia ${LAUKIAMA}"
        if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh || true; fi
        exit 0
    fi

    # Failai pakeisti ir servisas perkrautas, bet atiduodamas ne tas kodas.
    # Neskelbiam sėkmės — kitaip klaida vėl liktų nepastebėta.
    log "DĖMESIO: perkrauta, bet svetainė rodo '${GYVAI:-nieko}', laukta ${LAUKIAMA}."
    if [[ -x ./deploy/bukle.sh ]]; then ./deploy/bukle.sh || true; fi
    die "Deploy nepatvirtintas: gyvai ne tas commit'as. Patikrink gunicorn ir nginx talpyklą."
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
