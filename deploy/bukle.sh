#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# SERVERIO BŪKLĖS ATASKAITA → atskira repo šaka
#
# Kodėl: pokalbis su Claude sukasi debesyje ir tavo serverio NEMATO.
# Vienintelis kanalas atgal — GitHub. Šis skriptas surenka trumpą būklę
# ir įkelia ją į šaką „serverio-bukle", iš kurios ją galima perskaityti
# neturint jokios prieigos prie serverio.
#
# VIENPUSIS: serveris rašo, kiti skaito. Jokių komandų iš repo nevykdo.
#
# Kviečia deploy-from-git.sh po kiekvieno diegimo; galima ir ranka:
#     /root/autoleft/deploy/bukle.sh
# ═══════════════════════════════════════════════════════════════════════
set -u

APP_DIR="${APP_DIR:-/root/autoleft}"
SAKA="${BUKLE_BRANCH:-serverio-bukle}"
DARBO_KOPIJA="${BUKLE_DIR:-/root/autoleft_bukle}"
VENV="${VENV:-$APP_DIR/venv}"
GUNICORN_SOCK="${GUNICORN_SOCK:-/run/gunicorn.sock}"
HEALTH_HOST="${HEALTH_HOST:-autoleft.com}"

cd "$APP_DIR" || { echo "Nerastas $APP_DIR"; exit 1; }

# ── 1. Surenkam ────────────────────────────────────────────────────────
ATASKAITA="$(mktemp)"
trap 'rm -f "$ATASKAITA"' EXIT

{
    echo "# Serverio būklė"
    echo
    echo "Sugeneruota: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo
    echo '## Kodas'
    echo
    echo '```'
    echo "sukasi:      $(git log --oneline -1 2>&1)"
    git fetch --quiet origin master 2>/dev/null \
        && echo "origin/master: $(git log --oneline -1 origin/master 2>&1)" \
        || echo "origin/master: (git fetch nepavyko)"
    echo "šaka:        $(git rev-parse --abbrev-ref HEAD 2>&1)"
    NESVARU="$(git status --porcelain --untracked-files=no 2>/dev/null)"
    if [ -n "$NESVARU" ]; then
        echo "DĖMESIO: darbo katalogas nešvarus —"
        echo "$NESVARU" | sed 's/^/  /'
    else
        echo "darbo katalogas: švarus"
    fi
    echo '```'

    echo
    echo '## Servisai'
    echo
    echo '```'
    for s in gunicorn nginx postgresql autoleft-deploy.timer; do
        printf '%-24s %s\n' "$s" "$(systemctl is-active "$s" 2>&1)"
    done
    echo '```'

    echo
    echo '## Ar svetainė atsako'
    echo
    echo '```'
    if curl -fsS --max-time 5 --unix-socket "$GUNICORN_SOCK" \
            -H "Host: $HEALTH_HOST" -o /dev/null -w 'HTTP %{http_code}, %{time_total}s\n' \
            "http://localhost/" 2>&1; then
        :
    else
        echo "NEATSAKO per $GUNICORN_SOCK"
    fi
    echo '```'

    echo
    echo '## Skelbimų būsenos'
    echo
    echo '```'
    # Be --user: tik kiekiai, jokių asmens duomenų
    if [ -x "$VENV/bin/python" ]; then
        "$VENV/bin/python" manage.py skelbimu_bukle 2>&1 | head -40
    else
        echo "venv nerastas: $VENV"
    fi
    echo '```'

    echo
    echo '## Vietos diske'
    echo
    echo '```'
    df -h "$APP_DIR" 2>&1 | tail -2
    echo '```'

    echo
    echo '## Paskutinis auto-deploy'
    echo
    echo '```'
    journalctl -u autoleft-deploy -n 25 --no-pager 2>&1 | tail -25
    echo '```'
} > "$ATASKAITA"

# ── 2. Paskelbiam ──────────────────────────────────────────────────────
NUOTOLINIS="$(git remote get-url origin 2>/dev/null)"
if [ -z "$NUOTOLINIS" ]; then
    echo "Nerastas origin — ataskaita lieka tik čia:"
    cat "$ATASKAITA"
    exit 0
fi

if [ ! -d "$DARBO_KOPIJA/.git" ]; then
    rm -rf "$DARBO_KOPIJA"
    if ! git clone --quiet --depth 1 --branch "$SAKA" "$NUOTOLINIS" "$DARBO_KOPIJA" 2>/dev/null; then
        # Šakos dar nėra — kuriam tuščią, be pagrindinės istorijos
        mkdir -p "$DARBO_KOPIJA"
        git -C "$DARBO_KOPIJA" init --quiet
        git -C "$DARBO_KOPIJA" remote add origin "$NUOTOLINIS"
        git -C "$DARBO_KOPIJA" checkout --quiet -b "$SAKA"
    fi
fi

# Ar kas nors realiai pasikeitė? Laiko žymė keičiasi visada, tad ją
# lyginant praleidžiam — kitaip gautume po commit'ą kas penkias minutes.
BE_LAIKO='/^Sugeneruota:/d'
if [ -f "$DARBO_KOPIJA/bukle.md" ] \
   && diff -q <(sed "$BE_LAIKO" "$DARBO_KOPIJA/bukle.md") \
              <(sed "$BE_LAIKO" "$ATASKAITA") >/dev/null 2>&1; then
    echo "Būklė nepasikeitė — nieko nekeliam."
    exit 0
fi

cp -f "$ATASKAITA" "$DARBO_KOPIJA/bukle.md"
git -C "$DARBO_KOPIJA" add bukle.md

if git -C "$DARBO_KOPIJA" diff --cached --quiet; then
    echo "Būklė nepasikeitė — nieko nekeliam."
    exit 0
fi

git -C "$DARBO_KOPIJA" -c user.name='autoleft-serveris' \
    -c user.email='serveris@autoleft.local' \
    commit --quiet -m "būklė $(date '+%Y-%m-%d %H:%M')"

if git -C "$DARBO_KOPIJA" push --quiet -u origin "$SAKA" 2>/dev/null; then
    echo "Būklė paskelbta: šaka '$SAKA', failas bukle.md"
else
    echo "Nepavyko įkelti būklės (patikrink git push teises). Ataskaita:"
    cat "$ATASKAITA"
fi
