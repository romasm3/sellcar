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
LOCKFILE="/run/autoleft-deploy.lock"

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

if [[ "$LOCAL" == "$UPSTREAM" ]]; then
    exit 0                      # tyliai: nieko naujo
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

# ── Deploy per esamą agentą (migrate + collectstatic + restart + health) ──
if ./deploy-agent.sh; then
    log "✅ Deploy OK — gyvai veikia ${UPSTREAM:0:7}"
    exit 0
fi

# deploy-agent.sh jau grąžino FAILUS iš last_good; suderinam ir git istoriją.
log "deploy-agent.sh grąžino klaidą — atsukam git į ${LOCAL:0:7}, kad failai ir istorija sutaptų."
git reset --hard "$LOCAL" --quiet || log "DĖMESIO: git reset nepavyko — reikia rankinio įsikišimo."
die "Deploy nepavyko. Žr. aukščiau esantį health check'o žurnalą."
