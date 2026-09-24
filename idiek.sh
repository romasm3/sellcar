#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# Rankinis diegimas viena komanda (automatinis deploy'as IŠJUNGTAS).
#
# Tvarka:  redaguoju → ./idiek.sh → git push (tik kopija)
#
# 1. Nesucommit'inti pakeitimai → git add -A && git commit (PRIEŠ
#    perkrovimą, kad atsukus niekas nedingtų iš istorijos).
# 2. Įsimenam commit'ą ir ar svetainė JAU dabar grąžina 200.
# 3. collectstatic + systemctl restart gunicorn.
# 4. https://autoleft.com/ iki 10 kartų po 2 s.
# 5. 200 → „GYVA: <commit>".
# 6. Ne 200, o prieš tai buvo 200 → git reset --hard HEAD~1, perkrovimas,
#    pranešimas DIDELĖMIS raidėmis ir įrašas deploy/idiegimai.log.
# 7. Ne 200 ir prieš tai irgi ne 200 → nieko neatsukam, tik pranešam.
#
# Tylaus atsukimo nėra: kiekvienas matomas ekrane ir žurnale.
# Migracijų skriptas NEleidžia — jei yra nepritaikytų, sustoja
# (pirma pg_dump į /root/backups/, tada migrate ranka).
# ═══════════════════════════════════════════════════════════════════════
set -u
cd "$(dirname "$0")" || exit 1
URL="${IDIEK_URL:-https://autoleft.com/}"   # IDIEK_URL — tik atsukimo bandymui
PAGRINDINIS="https://autoleft.com/"
ZURNALAS="deploy/idiegimai.log"

zurnalas() { echo "[$(date '+%F %T')] $*" >> "$ZURNALAS"; }

kodas() {
    curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$URL"
}

laukiam_200() {
    local k=""
    for _ in 1 2 3 4 5 6 7 8 9 10; do
        sleep 2
        k="$(kodas)"
        [[ "$k" == "200" ]] && break
    done
    echo "$k"
}

perkrauk() {
    # Versijos žymę settings.py skaito paleidžiant — rašom PRIEŠ restart.
    git rev-parse --short=12 HEAD > VERSIJA
    venv/bin/python manage.py collectstatic --noinput -v 0 \
        || echo "DĖMESIO: collectstatic krito"
    systemctl restart gunicorn || echo "DĖMESIO: systemctl restart gunicorn krito"
}

# ── 0. Migracijos — ne šio skripto darbas ──────────────────────────────
if venv/bin/python manage.py showmigrations --plan 2>/dev/null | grep -q '^\[ \]'; then
    echo "SUSTOTA: yra nepritaikytų migracijų:"
    venv/bin/python manage.py showmigrations --plan | grep '^\[ \]' | sed 's/^/    /'
    echo "Pirma pg_dump į /root/backups/, tada: venv/bin/python manage.py migrate"
    exit 1
fi

# ── 1. Commit'as PRIEŠ perkrovimą ──────────────────────────────────────
if [[ -n "$(git status --porcelain)" ]]; then
    git add -A
    DRAUDZIAMI="$(git diff --cached --name-only \
        | grep -E '(^|/)\.env|\.bak|\.sql(\.gz)?$|\.dump$|^media/' || true)"
    if [[ -n "$DRAUDZIAMI" ]]; then
        git reset --quiet
        echo "SUSTOTA: tokių failų necommit'inam:"
        echo "$DRAUDZIAMI" | sed 's/^/    /'
        exit 1
    fi
    FAILAI="$(git diff --cached --name-only)"
    git commit --quiet -m "chore(idiek): pakeitimai prieš diegimą

$(echo "$FAILAI" | sed 's/^/- /')" || { echo "SUSTOTA: git commit nepavyko"; exit 1; }
    echo "Sucommit'inta prieš perkrovimą:"
    echo "$FAILAI" | sed 's/^/    /'
fi

# ── 2. Kas yra dabar ───────────────────────────────────────────────────
COMMIT="$(git rev-parse --short=12 HEAD)"
ANKSCIAU="$(kodas)"
echo "── Diegiu: $(git log --oneline -1)   (svetainė prieš: ${ANKSCIAU:-neatsako})"

# ── 3–4. Perkraunam ir tikrinam ────────────────────────────────────────
perkrauk
PO="$(laukiam_200)"

# ── 5. Gyva ────────────────────────────────────────────────────────────
if [[ "$PO" == "200" ]]; then
    GYVAI="$(curl -s --max-time 15 "$PAGRINDINIS" | grep -o 'name="versija" content="[^"]*"' | cut -d'"' -f4)"
    if [[ "$GYVAI" != "$COMMIT" ]]; then
        echo "DĖMESIO: / → 200, bet versijos žymė '${GYVAI:-nėra}', laukta $COMMIT (nginx talpykla?)"
        zurnalas "200, bet versija '${GYVAI:-nėra}' ≠ $COMMIT"
        exit 3
    fi
    echo "GYVA: $COMMIT"
    zurnalas "GYVA: $COMMIT — $(git log --format=%s -1)"
    exit 0
fi

# ── 7. Buvo sulūžusi dar prieš mus ─────────────────────────────────────
if [[ "$ANKSCIAU" != "200" ]]; then
    echo
    echo "SVETAINĖ BUVO SULŪŽUSI DAR PRIEŠ ŠĮ PAKEITIMĄ (prieš: ${ANKSCIAU:-neatsako}, po: ${PO:-neatsako})."
    echo "Nieko neatsukta. Žiūrėk: journalctl -u gunicorn -n 50 --no-pager"
    zurnalas "NEATSUKTA: $COMMIT — svetainė ir prieš buvo ${ANKSCIAU:-neatsako}, po ${PO:-neatsako}"
    exit 2
fi

# ── 6. Mes sulaužėm → atsukam ──────────────────────────────────────────
ATSUKTAS="$(git log --oneline -1)"
git reset --hard HEAD~1 --quiet
perkrauk
PO_ATSUKIMO="$(laukiam_200)"

PRANESIMAS="ATSUKTA: ${ATSUKTAS}
PRIEŽASTIS: PO PERKROVIMO ${URL} GRĄŽINO ${PO:-NEATSAKO} (PRIEŠ TAI BUVO 200).
DABAR: $(git log --oneline -1), SVETAINĖ → ${PO_ATSUKIMO:-NEATSAKO}."
GRAZINTI="git reset --hard ${COMMIT} && ./idiek.sh"
echo
echo "════════════════════════════════════════════════════════════════"
echo "${PRANESIMAS^^}"
echo "GRĄŽINTI ATSUKTĄ:  $GRAZINTI"
echo "════════════════════════════════════════════════════════════════"
zurnalas "$(echo "$PRANESIMAS" | tr '\n' ' ') Grąžinti: $GRAZINTI"
[[ "$PO_ATSUKIMO" == "200" ]] || echo "‼️  IR PO ATSUKIMO NE 200 — journalctl -u gunicorn -n 50 --no-pager"
exit 1
