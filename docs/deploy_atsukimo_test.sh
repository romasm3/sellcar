#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# DEPLOY ATSUKIMO TESTAS
#
# Paleidžia TIKRĄ deploy-agent.sh funkciją `sutvarkyti_po_atsukimo` su
# tikru git repozitoriumi ir tuo pačiu `set -euo pipefail`.
#
# Kodėl reikia: atsukus kodą, rsync perrašo failus sena versija, o git
# HEAD lieka rodyti į naują. Katalogas tampa nešvarus, ir kitas
# `git pull` nulūžta su „local changes would be overwritten by merge" —
# taimeris sukasi, bet nieko nebeparsiunčia, ir atrodo, kad jis mirė.
# Būtent taip 2026-09-01 keturi darbai „dingo" po vieną per minutę.
#
# Tikrinami trys atvejai: sėkmingas sutvarkymas, nėra VERSIJA žymės,
# ne git katalogas. Nė vienas negali nutraukti skripto.
#
# Paleidimas:  bash docs/deploy_atsukimo_test.sh
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail
T=$(mktemp -d); APP_DIR="$T/app"; LAST_GOOD="$T/last_good"; BACKUP_DIR="$T/atsargos"; TS=test
log() { echo "  [log] $*"; }
sed -n '/^sutvarkyti_po_atsukimo()/,/^}$/p' /home/user/sellcar/deploy-agent.sh > "$T/fn.sh"
# shellcheck disable=SC1090
source "$T/fn.sh"

mkdir -p "$APP_DIR"; cd "$APP_DIR"
git init -q; git config user.email t@t; git config user.name T
echo "GERA VERSIJA" > failas.txt; git add -A; git commit -qm gera
GERA=$(git rev-parse --short=12 HEAD)
echo "BLOGA VERSIJA" > failas.txt; git add -A; git commit -qm bloga
BLOGA=$(git rev-parse --short=12 HEAD)

# Imituojam deploy: snapshot geros versijos + VERSIJA žymė
mkdir -p "$LAST_GOOD"; echo "GERA VERSIJA" > "$LAST_GOOD/failas.txt"
echo "$GERA" > "$LAST_GOOD/VERSIJA"
# ...ir restore_code: failai seni, git HEAD rodo į blogą
cp "$LAST_GOOD/failas.txt" "$APP_DIR/failas.txt"
cp "$LAST_GOOD/VERSIJA" "$APP_DIR/VERSIJA"

echo "── PRIEŠ ──"
echo "  HEAD:        $(git rev-parse --short=12 HEAD)  (bloga=$BLOGA)"
echo "  git status:  $(git status --porcelain --untracked-files=no | wc -l) pakeitimai"
git -c advice.detachedHead=false stash list >/dev/null 2>&1 || true
if git merge --ff-only HEAD >/dev/null 2>&1 && [ -z "$(git status --porcelain --untracked-files=no)" ]; then
  echo "  pull veiktų:  taip"; else echo "  pull veiktų:  NE (nešvarus)"; fi

echo "── sutvarkyti_po_atsukimo ──"
sutvarkyti_po_atsukimo

echo "── PO ──"
echo "  HEAD:        $(git rev-parse --short=12 HEAD)  (gera=$GERA)"
echo "  git status:  $(git status --porcelain --untracked-files=no | wc -l) pakeitimai"
[ "$(git rev-parse --short=12 HEAD)" = "$GERA" ] && echo "  ✔ HEAD grąžintas į gerą versiją" || { echo "  ✘ HEAD blogas"; exit 1; }
[ -z "$(git status --porcelain --untracked-files=no)" ] && echo "  ✔ katalogas švarus" || { echo "  ✘ nešvarus"; exit 1; }
[ "$(cat failas.txt)" = "GERA VERSIJA" ] && echo "  ✔ turinys — geros versijos" || { echo "  ✘ turinys blogas"; exit 1; }
ls "$BACKUP_DIR"/pries_reset_*.patch >/dev/null 2>&1 && echo "  ✔ pakeitimai išsaugoti į atsargą" || echo "  · pakeitimų nebuvo, atsargos nereikėjo"
[ -f VERSIJA ] && echo "  ✔ VERSIJA žymė išliko ($(cat VERSIJA))" || { echo "  ✘ VERSIJA dingo"; exit 1; }

echo "── Kraštinis atvejis: nėra VERSIJA žymės ──"
rm -f "$LAST_GOOD/VERSIJA"; echo "KAZKAS KITA" > failas.txt
sutvarkyti_po_atsukimo
echo "  ✔ nenulūžo, tik įspėjo (katalogas liko: $(git status --porcelain --untracked-files=no | wc -l) pakeit.)"

echo "── Kraštinis atvejis: ne git katalogas ──"
APP_DIR="$T/negit"; mkdir -p "$APP_DIR"
sutvarkyti_po_atsukimo
echo "  ✔ nenulūžo"
rm -rf "$T"; echo "VISKAS GERAI"
