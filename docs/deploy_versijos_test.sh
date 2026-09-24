#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# VERSIJOS ŽYMĖ NEMELUOJA NĖ VIENA KRYPTIMI
#
# <meta name="versija"> ateina iš settings.GIT_SHA, o tas — iš failo
# APP_DIR/VERSIJA, kurį rašo deploy-agent.sh. Pagal šitą žymę tikrinamas
# KIEKVIENAS darbas (CLAUDE.md), tad jei ji meluoja, meluoja ir visos
# ataskaitos. 2026-09 taip ir nutiko: trys kartai iš eilės pranešta apie
# „neįvykusį deploy'ą", nors kodas seniai buvo gyvas.
#
# Dvi kryptys, abi blogos:
#   • žymė SENESNĖ nei įdiegtas kodas -> sakom „neįdiegta", nors įdiegta;
#   • žymė NAUJESNĖ nei įdiegtas kodas -> sakom „įdiegta", nors ne.
#
# Antroji buvo tikra skripto yda: apply() įrašydavo žymę PIRMUOJU
# veiksmu, ir jei toliau krisdavo collectstatic ar compilemessages,
# `set -e` nutraukdavo skriptą su NAUJA žyme ant SENO kodo.
#
# Tikrinam:
#   1. sėkmingas diegimas -> VERSIJA = įdiegtas commit'as
#   2. apply() krenta     -> VERSIJA lieka SENA (ne nauja!)
#   3. health_check krenta -> VERSIJA lieka SENA
#
# Paleidimas:  bash docs/deploy_versijos_test.sh
# ═══════════════════════════════════════════════════════════════════
set -uo pipefail

SAKNIS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
T="$(mktemp -d)"
# LAIKYTI=1 palieka laikiną katalogą — kad būtų kur pasižiūrėti agento
# išvestį, kai testas krenta.
if [[ "${LAIKYTI:-0}" == "1" ]]; then
  trap 'echo "laikinas katalogas paliktas: $T"' EXIT
else
  trap 'rm -rf "$T"' EXIT
fi

APP="$T/app"
mkdir -p "$APP"
cd "$APP"
git init -q .
git config user.email t@t; git config user.name T
echo v1 > failas.txt
mkdir -p venv/bin deploy scripts templates static
# `apply()` kviečia manage.py; be jo agentas krenta dar prieš tai, ką
# tikrinam. Turinys nesvarbus — `python` čia irgi maketas.
printf '%s\n' "import os" "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')" > manage.py
git add -A; git commit -qm pirmas
SENAS="$(git rev-parse --short=12 HEAD)"
echo "$SENAS" > VERSIJA          # tarsi ankstesnis deploy'as būtų įrašęs

echo v2 > failas.txt
git add -A; git commit -qm antras
NAUJAS="$(git rev-parse --short=12 HEAD)"

cp "$SAKNIS/deploy-agent.sh" .
chmod +x deploy-agent.sh

# Maketai: python daro tai, ką liepia PYTHON_ELGESYS.
cat > venv/bin/python <<'PY'
#!/usr/bin/env bash
if [[ "${PYTHON_KRENTA:-0}" == "1" && "$*" == *collectstatic* ]]; then
  echo "collectstatic: tyčinė klaida" >&2; exit 1
fi
exit 0
PY
# Tikras `activate` apibrėžia ir `deactivate` — be jo agentas krinta
# su „command not found", ir testas matuotų ne tą, ką nori.
cat > venv/bin/activate <<'AC'
deactivate() { :; }
AC
chmod +x venv/bin/python

klaidos=0
tik() { if [[ "$1" == "1" ]]; then echo "  ✔ $2"; else echo "  ✘ $2"; klaidos=$((klaidos+1)); fi; }
versija() { tr -d '[:space:]' < "$APP/VERSIJA" 2>/dev/null || echo '(nėra)'; }

paleisti() {
  APP_DIR="$APP" VENV="$APP/venv" \
  LAST_GOOD="$T/last_good" BACKUP_DIR="$T/backups" \
  PYTHON_KRENTA="${1:-0}" \
  HEALTH_KRENTA="${2:-0}" \
    ./deploy-agent.sh >"$T/isvestis" 2>&1
  echo $?
}

# deploy-agent.sh kviečia systemctl ir curl — pakeičiam maketais kelyje.
mkdir -p "$T/bin"
cat > "$T/bin/systemctl" <<'SC'
#!/usr/bin/env bash
exit 0
SC
cat > "$T/bin/curl" <<'CU'
#!/usr/bin/env bash
[[ "${HEALTH_KRENTA:-0}" == "1" ]] && exit 7
echo "<html><meta name=\"versija\" content=\"x\"></html>"
exit 0
CU
cat > "$T/bin/rsync" <<'RS'
#!/usr/bin/env bash
exit 0
RS
# Vietos patikra (MIN_LAISVOS_PROC) konteineryje krenta, nes /tmp būna
# beveik pilnas. Čia tikrinam versijos žymę, ne diską — tad `df` sakom,
# kad vietos yra.
# `source venv/bin/activate` yra maketas, tad `python` imamas iš PATH.
cat > "$T/bin/python" <<'PY2'
#!/usr/bin/env bash
if [[ "${PYTHON_KRENTA:-0}" == "1" && "$*" == *collectstatic* ]]; then
  echo "collectstatic: tyčine klaida" >&2; exit 1
fi
exit 0
PY2
cat > "$T/bin/df" <<'DF'
#!/usr/bin/env bash
echo "Filesystem 1024-blocks Used Available Capacity Mounted"
echo "/dev/testas 100000000 5000000 95000000 5% /"
DF
chmod +x "$T/bin/"*
export PATH="$T/bin:$PATH"

echo "── 1. Sėkmingas diegimas ──"
K=$(paleisti 0 0)
echo "     (agentas grąžino $K, VERSIJA=$(versija))"
tik "$([[ "$(versija)" == "$NAUJAS" ]] && echo 1)" \
    "VERSIJA = įdiegtas commit'as ($NAUJAS)"

echo "── 2. apply() krenta -> žymė NEPASIKEIČIA ──"
echo "$SENAS" > "$APP/VERSIJA"
K=$(paleisti 1 0)
echo "     (agentas grąžino $K, VERSIJA=$(versija))"
tik "$([[ "$(versija)" != "$NAUJAS" ]] && echo 1)" \
    "VERSIJA NĖRA naujas commit'as (žymė nemeluoja „įdiegta\")"
tik "$([[ "$(versija)" == "$SENAS" ]] && echo 1)" \
    "VERSIJA grąžinta į senąją ($SENAS)"
tik "$(grep -q 'Versijos žymė grąžinta' "$T/isvestis" && echo 1)" \
    "žurnale pasakyta, kad žymė grąžinta"

echo "── 3. health_check krenta -> žymė NEPASIKEIČIA ──"
echo "$SENAS" > "$APP/VERSIJA"
K=$(paleisti 0 1)
echo "     (agentas grąžino $K, VERSIJA=$(versija))"
tik "$([[ "$(versija)" != "$NAUJAS" ]] && echo 1)" \
    "VERSIJA NĖRA naujas commit'as"

echo
if [[ "$klaidos" == "0" ]]; then echo "VISKAS GERAI"; else echo "KLAIDŲ: $klaidos"; fi
[[ "$klaidos" == "0" ]]
