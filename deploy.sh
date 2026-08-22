#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# ĮDIEGIMAS VIENA KOMANDA — ./deploy.sh
#
# Eiga: parsisiųsti -> priklausomybės -> migracijos -> statika -> vertimai
#       -> testai (krenta = STOP) -> perkrauti -> smoke -> jei blogai,
#       grąžinti ankstesnį commit'ą ir perkrauti atgal.
#
# Nieko nediegia, kol testai nepraėję. Į produkciją niekada nepatenka
# šakos, kurių patikra raudona.
# ═══════════════════════════════════════════════════════════════════════
set -u
cd "$(dirname "$0")"

PY=venv/bin/python
SAKA="$(git rev-parse --abbrev-ref HEAD)"
PRIES="$(git rev-parse HEAD)"
T0=$SECONDS

zingsnis() { printf '\n▸ %s\n' "$1"; }
mirtis()   { printf '\n✖ SUSTOJAU: %s\n' "$1"; printf '  Nieko neįdiegta, sena versija veikia.\n'; exit 1; }

printf '═══ ĮDIEGIMAS %s ═══\n' "$(date '+%Y-%m-%d %H:%M')"
printf 'Šaka: %s   Buvęs commit: %s\n' "$SAKA" "${PRIES:0:8}"

# ── 1. Kodas ──────────────────────────────────────────────────────────
zingsnis "Kodas"
REQ_PRIES="$(md5sum requirements.txt 2>/dev/null | cut -d' ' -f1)"

if [ "$SAKA" = "master" ]; then
    git pull --ff-only origin master >/tmp/deploy_git.log 2>&1 || mirtis "git pull nepavyko ($(tail -1 /tmp/deploy_git.log))"
else
    # Dirbama šakoje: sulydom į master ir diegiam master
    git fetch origin master >/dev/null 2>&1
    git checkout master >/tmp/deploy_git.log 2>&1 || mirtis "negaliu pereiti į master"
    git pull --ff-only origin master >>/tmp/deploy_git.log 2>&1 || mirtis "git pull nepavyko"
    git merge --no-edit "$SAKA" >>/tmp/deploy_git.log 2>&1 || {
        git merge --abort 2>/dev/null; git checkout "$SAKA" >/dev/null 2>&1
        mirtis "šakos $SAKA sulydyti į master nepavyko (konfliktai)"
    }
    PRIES="$(git rev-parse HEAD@{1} 2>/dev/null || echo "$PRIES")"
fi
DABAR="$(git rev-parse HEAD)"
if [ "$PRIES" = "$DABAR" ]; then
    printf '  naujo kodo nėra (%s)\n' "${DABAR:0:8}"
else
    printf '  %s -> %s  (%s commit)\n' "${PRIES:0:8}" "${DABAR:0:8}" \
           "$(git rev-list --count "$PRIES".."$DABAR")"
fi

# ── 2. Priklausomybės ────────────────────────────────────────────────
zingsnis "Priklausomybės"
if [ "$REQ_PRIES" != "$(md5sum requirements.txt 2>/dev/null | cut -d' ' -f1)" ]; then
    venv/bin/pip install -r requirements.txt >/tmp/deploy_pip.log 2>&1 \
        || mirtis "pip install nepavyko (žr. /tmp/deploy_pip.log)"
    printf '  requirements.txt pasikeitė — įdiegta\n'
else
    printf '  nepasikeitė\n'
fi

# ── 3. Migracijos ────────────────────────────────────────────────────
zingsnis "Migracijos"
LAUKIA="$($PY manage.py showmigrations --plan 2>/dev/null | grep -c '^\[ \]')"
$PY manage.py migrate --noinput >/tmp/deploy_migrate.log 2>&1 \
    || mirtis "migrate nepavyko (žr. /tmp/deploy_migrate.log)"
printf '  pritaikyta: %s\n' "$LAUKIA"

# ── 4. Statika ir vertimai ───────────────────────────────────────────
zingsnis "Statika ir vertimai"
STAT="$($PY manage.py collectstatic --noinput 2>&1 | tail -1)"
printf '  %s\n' "$STAT"
$PY manage.py compilemessages >/tmp/deploy_msg.log 2>&1 \
    && printf '  vertimai sukompiliuoti\n' \
    || printf '  vertimai: klaidų (žr. /tmp/deploy_msg.log) — diegimas tęsiamas\n'

# ── 5. Patikra: šablonų nuotėkis + testai ────────────────────────────
zingsnis "Patikra"
NUOTEKIS="$(grep -rn '{#' templates/ --include='*.html' | grep -v '#}' | grep -v '\.bak' || true)"
if [ -n "$NUOTEKIS" ]; then
    printf '%s\n' "$NUOTEKIS" | sed 's/^/  /'
    mirtis "šablone likęs daugiaeilis {# #} — nutekėtų į puslapį"
fi
printf '  šablonai: švaru\n'

TESTAI="$($PY manage.py test apps.listings --testrunner=config.test_runner.BeDuombazes 2>&1)"
TESTU_KODAS=$?
printf '  %s\n' "$(printf '%s' "$TESTAI" | grep -E '^(OK|FAILED|Ran )' | tr '\n' ' ')"
if [ "$TESTU_KODAS" -ne 0 ]; then
    printf '%s\n' "$TESTAI" | grep -E '^(FAIL|ERROR):' | sed 's/^/  /'
    mirtis "testai krito"
fi

# ── 6. Perkrovimas ───────────────────────────────────────────────────
zingsnis "Perkrovimas"
systemctl restart gunicorn || mirtis "gunicorn neperkrautas"
sleep 2
printf '  gunicorn perkrautas\n'

# ── 7. Smoke ─────────────────────────────────────────────────────────
zingsnis "Smoke"
SKELBIMAS="$($PY manage.py shell -c "from apps.listings.models import Listing; l=Listing.objects.filter(status='active', is_shadow_banned=False).order_by('-created_at').first(); print(l.pk if l else '')" 2>/dev/null | tr -d '[:space:]')"
ADRESAI=("/" "/?section=cars" "/searches/")
[ -n "$SKELBIMAS" ] && ADRESAI+=("/$SKELBIMAS/")

BLOGAI=0
for a in "${ADRESAI[@]}"; do
    # -L: /searches/ neprisijungusiam permeta į prisijungimą, tai normalu
    KODAS="$(curl -skL -o /dev/null -w '%{http_code}' "https://127.0.0.1$a")"
    printf '  %-18s %s\n' "$a" "$KODAS"
    [ "$KODAS" != "200" ] && BLOGAI=1
done

# ── 8. Grąžinimas, jei smoke nepavyko ────────────────────────────────
if [ "$BLOGAI" -ne 0 ]; then
    printf '\n✖ Smoke testas nepraėjo — grąžinu %s\n' "${PRIES:0:8}"
    git reset --hard "$PRIES" >/dev/null 2>&1
    $PY manage.py collectstatic --noinput >/dev/null 2>&1
    systemctl restart gunicorn
    sleep 2
    printf '  grąžinta ir perkrauta. Patikrink /tmp/deploy_*.log\n'
    exit 1
fi

printf '\n✔ ĮDIEGTA %s   (%s s)\n' "${DABAR:0:8}" "$((SECONDS - T0))"
