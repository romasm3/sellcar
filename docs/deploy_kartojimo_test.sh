#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# DEPLOY KARTOJIMO SAUGIKLIO TESTAS
#
# Paleidžia TIKRĄ deploy-from-git.sh su tikrais git repozitoriumis; tik
# deploy-agent.sh ir patikra.sh pakeisti maketais.
#
# Kodėl reikia: `.blogas-commitas` saugiklis veikė tik tada, kai krisdavo
# scripts/patikra.sh. Kai krisdavo pats deploy-agent.sh, žymė nebūdavo
# rašoma, ir taimeris kas minutę bandydavo tą patį commit'ą iš naujo —
# kas minutę atsukdamas kodą. 2026-09-01 būtent taip „dingo" keturi darbai.
#
# Tikrinam tris eigas:
#   1. deploy-agent krenta  → žymė įrašoma, git atsuktas
#   2. tas pats commit'as   → net nebandoma (agentas nekviečiamas)
#   3. naujas commit'as     → žymė nebegalioja, bandoma vėl
#
# Paleidimas:  bash docs/deploy_kartojimo_test.sh
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
git config --global init.defaultBranch master >/dev/null 2>&1 || true
echo "v1" > failas.txt
mkdir -p deploy scripts
cp "$SAKNIS/deploy-from-git.sh" .
# Maketai: patikra praeina, agentas KRENTA ir imituoja failų atsukimą
cat > deploy-agent.sh <<'AG'
#!/usr/bin/env bash
echo x >> "$SKAITIKLIS"
echo "v1" > failas.txt      # tarsi restore_code būtų grąžinęs seną versiją
exit 1
AG
cat > scripts/patikra.sh <<'PT'
#!/usr/bin/env bash
exit 0
PT
chmod +x deploy-agent.sh scripts/patikra.sh deploy-from-git.sh
git add -A; git commit -qm pirmas
git branch -M master 2>/dev/null || true
git push -q -u origin master 2>/dev/null
GERAS="$(git rev-parse HEAD)"

# Naujas commit'as nuotoliniame — bus ką diegti
KLONAS="$T/klonas"
git clone -q "$NUOTOLINIS" "$KLONAS"
cd "$KLONAS"; git config user.email t@t; git config user.name T
echo "v2" > failas.txt; git commit -qam antras; git push -q origin master
BLOGAS="$(git rev-parse HEAD)"
cd "$APP"

paleisti() {
  APP_DIR="$APP" LOCKFILE="$T/lock" SKAITIKLIS="$SKAITIKLIS" \
    ./deploy-from-git.sh >"$T/isvestis" 2>&1 || true
}
kvietimu() { [[ -f "$SKAITIKLIS" ]] && wc -l < "$SKAITIKLIS" | tr -d ' ' || echo 0; }
klaidos=0
tik() { if [[ "$1" == "1" ]]; then echo "  ✔ $2"; else echo "  ✘ $2"; klaidos=$((klaidos+1)); fi; }

echo "── 1. deploy-agent krenta ──"
paleisti
tik "$([[ "$(kvietimu)" == "1" ]] && echo 1)" "agentas kviestas 1 kartą (kvietimų: $(kvietimu))"
tik "$([[ -f "$APP/deploy/.blogas-commitas" ]] && echo 1)" "žymė .blogas-commitas įrašyta"
tik "$([[ "$(cat "$APP/deploy/.blogas-commitas" 2>/dev/null)" == "$BLOGAS" ]] && echo 1)" \
    "žymėje būtent kritęs commit'as"
tik "$([[ "$(git -C "$APP" rev-parse HEAD)" == "$GERAS" ]] && echo 1)" \
    "git atsuktas į veikiančią versiją"
tik "$([[ -z "$(git -C "$APP" status --porcelain --untracked-files=no)" ]] && echo 1)" \
    "darbinis katalogas švarus"

echo "── 2. Tas pats commit'as — nebandoma ──"
paleisti
tik "$([[ "$(kvietimu)" == "1" ]] && echo 1)" \
    "agentas NEBUVO kviestas antrą kartą (kvietimų: $(kvietimu))"

echo "── 3. Naujas commit'as — bandoma vėl ──"
cd "$KLONAS"; echo "v3" > failas.txt; git commit -qam trecias; git push -q origin master
cd "$APP"
paleisti
tik "$([[ "$(kvietimu)" == "2" ]] && echo 1)" \
    "naujas commit'as žymę panaikino (kvietimų: $(kvietimu))"

echo
if [[ "$klaidos" == "0" ]]; then echo "VISKAS GERAI"; else echo "KLAIDŲ: $klaidos"; fi
exit "$klaidos"
