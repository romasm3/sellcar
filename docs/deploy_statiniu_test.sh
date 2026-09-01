#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# DEPLOY STATINIŲ PATIKROS TESTAS
#
# Paleidžia TIKRAS deploy-agent.sh funkcijas su tuo pačiu
# `set -euo pipefail`, tik `curl` ir `stat` pakeisti maketais.
#
# Kodėl reikia: pirma šitos patikros redakcija nutraukdavo VISĄ deploy'ą
# dar prieš prasidedant. `grep` be atitikmens grąžina 1, `pipefail` tą 1
# paverčia priskyrimo klaida, o `set -e` išmeta iš skripto. Pirmą kartą
# atitikmens ir negali būti — senas HTML sumaišyto vardo neturi. Klaida
# tyli: svetainė nesikeičia, o žurnale nieko akivaizdaus.
#
# Todėl deploy skripto logika tikrinama PALEIDŽIANT ją, ne skaitant.
#
# Paleidimas:  bash docs/deploy_statiniu_test.sh
set -euo pipefail
APP_DIR=/tmp/claude-0/fake_app
GUNICORN_SOCK=/tmp/fake.sock
HEALTH_HOST=autoleft.com
log() { echo "  [log] $*"; }

# Ištraukiam funkcijas iš tikro skripto
sed -n '/^STATINIU_MANIFESTAS=/,/^}$/p' /home/user/sellcar/deploy-agent.sh > /tmp/claude-0/fn.sh
sed -n '/^tikrinti_statinius()/,/^}$/p' /home/user/sellcar/deploy-agent.sh >> /tmp/claude-0/fn.sh
# curl maketas: HTML be maišo arba su maišu
curl() { printf '%s' "$FAKE_HTML"; }
stat() { echo "$FAKE_MT"; }
# shellcheck disable=SC1091
source /tmp/claude-0/fn.sh

mkdir -p "$(dirname "$APP_DIR/staticfiles/staticfiles.json")"

echo "── 1. PIRMAS deploy: senas HTML be maišo (čia ir lūžo) ──"
FAKE_HTML='<link href="/static/css/style.css">'; FAKE_MT=0
PRIES="$(statiniu_bukle)"; echo "  PRIES=[$PRIES]  ✔ nenutrūko"

echo "── 2. Po deploy: HTML su maišu, manifestas naujesnis ──"
touch "$APP_DIR/staticfiles/staticfiles.json"
FAKE_HTML='<link href="/static/css/style.df8265b02e1b.css">'; FAKE_MT=999
SABLONAI_KEITESI=1
if tikrinti_statinius "0" ""; then echo "  ✔ patikra praėjo"; else echo "  ✘ patikra neleido"; fi

echo "── 3. Blogas atvejis: šablonai keitėsi, CSS vardas ne ──"
FAKE_MT=1000
if tikrinti_statinius "999" "style.df8265b02e1b.css"; then
  echo "  ✘ PRALEIDO (neturėtų)"; else echo "  ✔ deploy sustabdytas"; fi

echo "── 4. Blogas atvejis: manifestas neatsinaujino ──"
FAKE_MT=1000
if tikrinti_statinius "1000" ""; then
  echo "  ✘ PRALEIDO (neturėtų)"; else echo "  ✔ deploy sustabdytas"; fi

echo "── 5. Blogas atvejis: HTML be maišo po deploy ──"
FAKE_HTML='<link href="/static/css/style.css">'; FAKE_MT=2000
if tikrinti_statinius "1000" ""; then
  echo "  ✘ PRALEIDO (neturėtų)"; else echo "  ✔ deploy sustabdytas"; fi
echo "VISKAS"
