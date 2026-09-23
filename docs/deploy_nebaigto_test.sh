#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# NUTRAUKTAS DIEGIMAS PATS PASITAISO
#
# Kodėl reikia. 2026-09-13..15 svetainė septynias paras rodė seną kodą,
# nors serverio git buvo ant naujausio commit'o, o servisas kas minutę
# baigdavosi `status=0/SUCCESS`.
#
# Eiga buvo tokia:
#   1. deploy-from-git.sh PIRMA pastumia darbo katalogą (git merge --ff-only),
#      o gunicorn perkrauna tik pabaigoje (deploy-agent.sh);
#   2. systemd nutraukė vieną paleidimą per vidurį (TimeoutStartSec) —
#      medis jau pastumtas, perkrovimo nebuvo;
#   3. nuo tos akimirkos LOCAL == UPSTREAM, tad kiekvienas kitas ciklas
#      išeidavo tyliai ir „sėkmingai";
#   4. tie commit'ai nebūtų įdiegti NIEKADA — klaida pati save palaikė.
#
# Dabar tikrinam ne tik git, bet ir VERSIJA žymę, kurią deploy-agent.sh
# rašo TADA, kai tikrai perkrovė aplikaciją.
#
# Tikrinam:
#   1. VERSIJA atsilieka nuo HEAD → agentas KVIEČIAMAS, nors naujo kodo nėra
#   2. VERSIJA sutampa su HEAD    → nedaroma nieko (tylus ciklas)
#   3. VERSIJA nėra visai         → nedaroma nieko (pirmas kartas, ne mūsų byla)
#   4. agentas perkrovė, bet gyvai senas commit'as → SĖKMĖ NESKELBIAMA
#
# Paleidimas:  bash docs/deploy_nebaigto_test.sh
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

SAKNIS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

NUOTOLINIS="$T/nuotolinis.git"
APP="$T/app"
SKAITIKLIS="$T/agento-kvietimai"

git init -q --bare "$NUOTOLINIS"
git clone -q "$NUOTOLINIS" "$APP" 2>/dev/null
cd "$APP"
git config user.email t@t; git config user.name T
echo "v1" > failas.txt
mkdir -p deploy scripts
cp "$SAKNIS/deploy-from-git.sh" .

# Agentas: pažymi kvietimą ir įrašo VERSIJA, kaip daro tikrasis.
cat > deploy-agent.sh <<'AG'
#!/usr/bin/env bash
# --tik-db-kopija yra parengiamasis kvietimas (DB kopija pries
# migracijas), ne diegimas — jo neskaiciuojam.
[[ "${1:-}" == "--tik-db-kopija" ]] && exit 0
echo x >> "$SKAITIKLIS"
git rev-parse --short=12 HEAD > VERSIJA
exit 0
AG
cat > scripts/patikra.sh <<'PT'
#!/usr/bin/env bash
exit 0
PT
chmod +x deploy-agent.sh scripts/patikra.sh deploy-from-git.sh
git add -A; git commit -qm pirmas
git branch -M master 2>/dev/null || true
git push -q -u origin master 2>/dev/null

# Naujas commit'as nuotoliniame
KLONAS="$T/klonas"
git clone -q "$NUOTOLINIS" "$KLONAS"
cd "$KLONAS"; git config user.email t@t; git config user.name T
echo "v2" > failas.txt; git commit -qam antras; git push -q origin master
NAUJAS_TRUMPAS="$(git rev-parse --short=12 HEAD)"
cd "$APP"

paleisti() {
  APP_DIR="$APP" LOCKFILE="$T/lock" SKAITIKLIS="$SKAITIKLIS" \
    ./deploy-from-git.sh >"$T/isvestis" 2>&1 || true
}
kvietimu() { [[ -f "$SKAITIKLIS" ]] && wc -l < "$SKAITIKLIS" | tr -d ' ' || echo 0; }
klaidos=0
tik() { if [[ "$1" == "1" ]]; then echo "  ✔ $2"; else echo "  ✘ $2"; klaidos=$((klaidos+1)); fi; }

echo "── 0. Pirmas normalus diegimas ──"
paleisti
tik "$([[ "$(kvietimu)" == "1" ]] && echo 1)" "agentas kviestas (kvietimų: $(kvietimu))"
tik "$([[ "$(cat "$APP/VERSIJA")" == "$NAUJAS_TRUMPAS" ]] && echo 1)" \
    "VERSIJA = $(cat "$APP/VERSIJA")"

echo "── 1. VERSIJA sutampa — tylus ciklas ──"
paleisti
tik "$([[ "$(kvietimu)" == "1" ]] && echo 1)" \
    "agentas NEkviestas antrą kartą (kvietimų: $(kvietimu))"

echo "── 2. NUTRAUKTAS diegimas: medis pastumtas, VERSIJA atsilikusi ──"
# Būtent tai padarė systemd: merge įvyko, perkrovimas — ne.
echo "senas12345ab" > "$APP/VERSIJA"
paleisti
tik "$([[ "$(kvietimu)" == "2" ]] && echo 1)" \
    "agentas kviestas IŠ NAUJO (kvietimų: $(kvietimu))"
tik "$(grep -q "NEBAIGTAS DIEGIMAS" "$T/isvestis" && echo 1)" \
    "žurnale pasakyta, kad diegimas buvo nebaigtas"
tik "$([[ "$(cat "$APP/VERSIJA")" == "$NAUJAS_TRUMPAS" ]] && echo 1)" \
    "VERSIJA pasivijo darbo katalogą"

echo "── 3. VERSIJA failo nėra — nesikišam ──"
rm -f "$APP/VERSIJA"
paleisti
tik "$([[ "$(kvietimu)" == "2" ]] && echo 1)" \
    "agentas NEkviestas (kvietimų: $(kvietimu))"

echo "── 4. Sėkmė neskelbiama, jei gyvai ne tas commit'as ──"
# Tikrasis skriptas pabaigoje klausia svetainės, kuris commit'as gyvas.
tik "$(grep -q "Deploy nepatvirtintas" "$SAKNIS/deploy-from-git.sh" && echo 1)" \
    "skripte yra galutinė gyvo commit'o patikra"
tik "$(grep -q 'name="versija"' "$SAKNIS/deploy-from-git.sh" && echo 1)" \
    "tikrinama būtent versijos žymė puslapyje"
tik "$(grep -q 'GYVAI veikia' "$SAKNIS/deploy-from-git.sh" && echo 1)" \
    "sėkmės eilutė pasako, kuris commit'as gyvas"

echo ""
if [[ "$klaidos" -gt 0 ]]; then
  echo "NEPRAĖJO: $klaidos"
  echo "── paskutinė išvestis ──"; cat "$T/isvestis"
  exit 1
fi
echo "VISI TESTAI PRAĖJO"
