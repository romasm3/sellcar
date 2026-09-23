#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# DEPLOY ŠVARUMO VARTŲ TESTAS
#
# Paleidžia TIKRĄ deploy-from-git.sh su tikrais git repozitoriumis; tik
# deploy-agent.sh ir patikra.sh pakeisti maketais.
#
# Kodėl reikia: 2026-09 deploy'as stovėjo 8 paras. Serveryje dirbantys
# agentai rašo pastabas į docs/klaidos/*.md, tie failai sekami, ir
# švarumo patikra stabdydavo KIEKVIENĄ timerio ciklą — apie 11 000
# bandymų. Tekstinis žinynas blokavo kodo diegimą.
#
# Tikrinam tris eigas:
#   1. švaru                  → diegiama
#   2. pakeisti tik docs/     → diegiama, docs padėti į stash'ą
#   3. pakeistas kodas        → sustojama (kaip ir anksčiau)
#
# Paleidimas:  bash docs/deploy_svarumo_test.sh
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
mkdir -p deploy scripts docs/klaidos
echo "# pastabos" > docs/klaidos/BENDROS.md
cp "$SAKNIS/deploy-from-git.sh" .
cat > deploy-agent.sh <<'AG'
#!/usr/bin/env bash
echo x >> "$SKAITIKLIS"
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

KLONAS="$T/klonas"
git clone -q "$NUOTOLINIS" "$KLONAS"
cd "$KLONAS"; git config user.email t@t; git config user.name T

naujas_commitas() {                     # kad visada būtų ką diegti
  cd "$KLONAS"; echo "$RANDOM" > failas.txt
  git commit -qam "naujas"; git push -q origin master; cd "$APP"
}
paleisti() {
  APP_DIR="$APP" LOCKFILE="$T/lock" SKAITIKLIS="$SKAITIKLIS" \
    ./deploy-from-git.sh >"$T/isvestis" 2>&1 || true
}
kvietimu() { [[ -f "$SKAITIKLIS" ]] && wc -l < "$SKAITIKLIS" | tr -d ' ' || echo 0; }
klaidos=0
tik() { if [[ "$1" == "1" ]]; then echo "  ✔ $2"; else echo "  ✘ $2"; klaidos=$((klaidos+1)); fi; }

cd "$APP"

echo "── 1. Švarus katalogas ──"
naujas_commitas; paleisti
tik "$([[ "$(kvietimu)" == "1" ]] && echo 1)" "diegiama (kvietimų: $(kvietimu))"

echo "── 2. Pakeisti TIK docs/ — deploy'as nesustoja ──"
naujas_commitas
echo "nauja pastaba serveryje" >> "$APP/docs/klaidos/BENDROS.md"
paleisti
tik "$([[ "$(kvietimu)" == "2" ]] && echo 1)" \
    "diegiama nepaisant docs/ (kvietimų: $(kvietimu))"
tik "$([[ -z "$(git -C "$APP" status --porcelain --untracked-files=no)" ]] && echo 1)" \
    "katalogas po to švarus"
tik "$([[ -n "$(git -C "$APP" stash list)" ]] && echo 1)" \
    "docs pakeitimai padėti į stash'ą, ne ištrinti"
# Turinys atkuriamas — būtent dėl to ir stash, o ne checkout.
git -C "$APP" stash pop --quiet 2>/dev/null || true
tik "$(grep -q 'nauja pastaba serveryje' "$APP/docs/klaidos/BENDROS.md" && echo 1)" \
    "stash pop grąžina pastabą"
git -C "$APP" checkout -- docs/ 2>/dev/null || true

echo "── 3. Pakeistas KODAS — deploy'as sustoja ──"
naujas_commitas
echo "# rankinis redagavimas" >> "$APP/deploy-agent.sh"
paleisti
tik "$([[ "$(kvietimu)" == "2" ]] && echo 1)" \
    "agentas NEBUVO kviestas (kvietimų: $(kvietimu))"
tik "$(grep -q 'nešvarus' "$T/isvestis" && echo 1)" "pasakyta, kodėl sustota"
tik "$(grep -q 'deploy-agent.sh' "$T/isvestis" && echo 1)" "įvardytas kaltas failas"

echo
if [[ "$klaidos" == "0" ]]; then echo "VISKAS GERAI"; else echo "KLAIDŲ: $klaidos"; fi
[[ "$klaidos" == "0" ]]
