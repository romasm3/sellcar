#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# DB KOPIJA PRIEŠ MIGRACIJAS
#
# Kodėl: pg_dump deploy'e buvo, bet sukdavosi deploy-agent.sh viduje, o
# tas paleidžiamas TIK PO to, kai deploy-from-git.sh jau pritaikė
# migracijas. Blogos migracijos atveju atstatyti buvo ne iš ko — pirmas
# dumpas jau turėjo pakeistą schemą.
#
# Tikrinam eiliškumą TIKRAME skripte, o ne skaitydami kodą:
#   1. kopija paimama PRIEŠ „migrate"
#   2. jei kopija nepavyksta — migracijos NEPALEIDŽIAMOS, kodas atsuktas
#
# Paleidimas:  bash docs/deploy_db_kopijos_test.sh
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

SAKNIS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

NUOTOLINIS="$T/nuotolinis.git"
APP="$T/app"
EIGA="$T/eiga"                      # čia rašom, kas ir kada įvyko

git init -q --bare "$NUOTOLINIS"
git clone -q "$NUOTOLINIS" "$APP" 2>/dev/null
cd "$APP"
git config user.email t@t; git config user.name T
echo "v1" > failas.txt
mkdir -p deploy scripts venv/bin
cp "$SAKNIS/deploy-from-git.sh" .

# Maketai: „python" rašo į eigą, kai kviečiamas migrate.
cat > venv/bin/python <<'PY'
#!/usr/bin/env bash
[[ "$*" == *"migrate"* ]] && echo "MIGRATE" >> "$EIGA"
exit 0
PY
cat > deploy-agent.sh <<'AG'
#!/usr/bin/env bash
if [[ "${1:-}" == "--tik-db-kopija" ]]; then
  echo "KOPIJA" >> "$EIGA"
  [[ "${KOPIJA_KRENTA:-0}" == "1" ]] && exit 1
  exit 0
fi
echo "DIEGIMAS" >> "$EIGA"
git rev-parse --short=12 HEAD > VERSIJA
exit 0
AG
cat > scripts/patikra.sh <<'PT'
#!/usr/bin/env bash
exit 0
PT
chmod +x deploy-agent.sh scripts/patikra.sh deploy-from-git.sh venv/bin/python
git add -A; git commit -qm pirmas
git branch -M master 2>/dev/null || true
git push -q -u origin master 2>/dev/null
GERAS="$(git rev-parse HEAD)"

KLONAS="$T/klonas"
git clone -q "$NUOTOLINIS" "$KLONAS"
cd "$KLONAS"; git config user.email t@t; git config user.name T

naujas() { cd "$KLONAS"; echo "$RANDOM" > failas.txt
           git commit -qam n; git push -q origin master; cd "$APP"; }
paleisti() {
  APP_DIR="$APP" LOCKFILE="$T/lock" EIGA="$EIGA" ZURNALAS="$T/zurnalas" \
    KOPIJA_KRENTA="${1:-0}" ./deploy-from-git.sh >"$T/isvestis" 2>&1 || true
}
klaidos=0
tik() { if [[ "$1" == "1" ]]; then echo "  ✔ $2"; else echo "  ✘ $2"; klaidos=$((klaidos+1)); fi; }

cd "$APP"

echo "── 1. Kopija paimama PRIEŠ migracijas ──"
naujas; : > "$EIGA"; paleisti
EIL="$(tr '\n' ' ' < "$EIGA")"
echo "     eiga: $EIL"
tik "$([[ "$EIL" == "KOPIJA MIGRATE DIEGIMAS "* ]] && echo 1)" \
    "eiliškumas KOPIJA → MIGRATE → DIEGIMAS"
tik "$(grep -q 'DB kopija prieš migracijas paimta' "$T/isvestis" && echo 1)" \
    "žurnale pasakyta, kad kopija paimta"

echo "── 2. Kopija krenta → migracijų nepaleidžiam ──"
naujas; PO_NAUJO="$(git -C "$APP" rev-parse HEAD)"; : > "$EIGA"
paleisti 1
EIL="$(tr '\n' ' ' < "$EIGA")"
echo "     eiga: $EIL"
tik "$([[ "$EIL" != *"MIGRATE"* ]] && echo 1)" "migracijos NEPALEISTOS"
tik "$([[ "$EIL" != *"DIEGIMAS"* ]] && echo 1)" "diegimas NEĮVYKO"
tik "$(grep -q 'DB kopija nepavyko' "$T/isvestis" && echo 1)" "pasakyta, kodėl sustota"
tik "$([[ -f "$APP/deploy/.blogas-commitas" ]] && echo 1)" \
    "žymė įrašyta — nekartosim kas minutę"

echo "── 3. Žurnalas rašomas ir į failą ──"
tik "$([[ -s "$T/zurnalas" ]] && echo 1)" "failas netuščias ($(wc -l < "$T/zurnalas") eil.)"
tik "$(grep -q 'DB kopija' "$T/zurnalas" && echo 1)" "faile yra tos pačios eilutės"

echo
if [[ "$klaidos" == "0" ]]; then echo "VISKAS GERAI"; else echo "KLAIDŲ: $klaidos"; fi
[[ "$klaidos" == "0" ]]
