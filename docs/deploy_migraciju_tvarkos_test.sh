#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# MIGRACIJOS NIEKADA NEBŪNA NAUJESNĖS UŽ KODĄ
#
# Sena tvarka: migruojam → perkraunam → tikrinam. Kai patikra krisdavo,
# kodas būdavo atsukamas, o DB likdavo naujesnė. Būtent taip neatsukama
# 0107 ištrynė contact_phone reikšmes per NEPAVYKUSĮ bandymą: duomenys
# dingo, o kodas, kuris juos būtų naudojęs, buvo atsuktas atgal.
#
# Nauja tvarka, kurią čia ir tikrinam:
#   1. `manage.py check` eina PRIEŠ migracijas. Krito — `migrate`
#      NEKVIEČIAMAS išvis, DB nepaliesta.
#   2. Jei migracijos JAU pritaikytos, o patikra krenta — kodas
#      NEATSUKAMAS (sena versija liktų su naujesne schema), skriptas
#      sustoja ir pasako, ko reikia.
#   3. Jei migracijų nebuvo — atsukimas veikia kaip anksčiau.
#   4. Patikros išvestis nebemetama į /dev/null: kritus ji atsiduria
#      žurnale, kitaip priežasties nesimato.
#
# Paleidimas:  bash docs/deploy_migraciju_tvarkos_test.sh
# ═══════════════════════════════════════════════════════════════════
set -uo pipefail

SAKNIS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
T="$(mktemp -d)"
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
printf '%s\n' "import os" > manage.py
git add -A; git commit -qm pirmas
SENAS="$(git rev-parse --short=12 HEAD)"
echo "$SENAS" > VERSIJA
mkdir -p "$T/last_good"; echo "$SENAS" > "$T/last_good/VERSIJA"
echo v2 > failas.txt
git add -A; git commit -qm antras

cp "$SAKNIS/deploy-agent.sh" .
chmod +x deploy-agent.sh
cat > venv/bin/activate <<'AC'
deactivate() { :; }
AC

mkdir -p "$T/bin"

# ── Maketai ────────────────────────────────────────────────────────
# python rašo kiekvieną kvietimą į kvietimai.txt, kad matytume, ar
# `migrate` apskritai buvo pasiektas.
cat > "$T/bin/python" <<'PY'
#!/usr/bin/env bash
echo "$*" >> "$KVIETIMAI"
case "$*" in
  *check*)
    if [[ "${CHECK_KRENTA:-0}" == "1" ]]; then
      echo "SystemCheckError: tyčinė klaida šablone" >&2; exit 1
    fi
    exit 0 ;;
  *showmigrations*)
    # Prieš migrate — viena pritaikyta; po jo — dvi (jei MIGRACIJOS_YRA).
    echo "[X] listings.0001"
    if [[ "${MIGRACIJOS_YRA:-0}" == "1" && -f "$MIGRUOTA" ]]; then
      echo "[X] listings.0002"
    fi
    exit 0 ;;
  *migrate*)
    touch "$MIGRUOTA"; exit 0 ;;
esac
exit 0
PY
cat > "$T/bin/curl" <<'CU'
#!/usr/bin/env bash
if [[ "${HEALTH_KRENTA:-0}" == "1" ]]; then
  echo "curl: (7) Failed to connect to gunicorn.sock" >&2
  echo "TyCINE-KLAIDOS-ZYME" >&2
  exit 7
fi
echo "<html>ok</html>"
exit 0
CU
cat > "$T/bin/rsync" <<'RS'
#!/usr/bin/env bash
echo "$*" >> "$RSYNC_KVIETIMAI"
exit 0
RS
cat > "$T/bin/systemctl" <<'SC'
#!/usr/bin/env bash
exit 0
SC
cat > "$T/bin/df" <<'DF'
#!/usr/bin/env bash
echo "Filesystem 1024-blocks Used Available Capacity Mounted"
echo "/dev/testas 100000000 5000000 95000000 5% /"
DF
chmod +x "$T/bin/"*
export PATH="$T/bin:$PATH"

klaidos=0
tik() { if [[ "$1" == "1" ]]; then echo "  ✔ $2"; else echo "  ✘ $2"; klaidos=$((klaidos+1)); fi; }

paleisti() {
  : > "$T/kvietimai"; : > "$T/rsync_kvietimai"; rm -f "$T/migruota"
  APP_DIR="$APP" VENV="$APP/venv" \
  LAST_GOOD="$T/last_good" BACKUP_DIR="$T/backups" \
  KVIETIMAI="$T/kvietimai" RSYNC_KVIETIMAI="$T/rsync_kvietimai" \
  MIGRUOTA="$T/migruota" \
  CHECK_KRENTA="${1:-0}" MIGRACIJOS_YRA="${2:-0}" HEALTH_KRENTA="${3:-0}" \
    ./deploy-agent.sh >"$T/isvestis" 2>&1
  echo $?
}

echo "── 1. manage.py check krenta → migracijos NEPALEIDŽIAMOS ──"
K=$(paleisti 1 1 0)
tik "$([[ "$K" != "0" ]] && echo 1)" "agentas sustojo (grąžino $K)"
tik "$(grep -q 'migrate' "$T/kvietimai" && echo 0 || echo 1)" \
    "migrate NEBUVO kviestas — DB nepaliesta"
tik "$(grep -q 'check' "$T/kvietimai" && echo 1)" "check buvo kviestas"
tik "$(grep -q 'MIGRACIJOS NEPALEISTOS' "$T/isvestis" && echo 1)" \
    "žurnale pasakyta, kad DB nepaliesta"
tik "$(grep -q 'tyčinė klaida šablone' "$T/isvestis" && echo 1)" \
    "žurnale matosi TIKROJI check klaida"

echo "── 2. Migracijos pritaikytos + patikra krenta → kodas NEATSUKAMAS ──"
K=$(paleisti 0 1 1)
tik "$([[ "$K" != "0" ]] && echo 1)" "agentas sustojo (grąžino $K)"
tik "$(grep -q 'MIGRACIJOS JAU PRITAIKYTOS' "$T/isvestis" && echo 1)" \
    "žurnale pasakyta, kodėl neatsukama"
tik "$(grep -q 'last_good' "$T/rsync_kvietimai" && echo 0 || echo 1)" \
    "restore_code NEBUVO kviestas (rsync iš last_good nevyko)"
tik "$(grep -q 'kopija prieš migracijas' "$T/isvestis" && echo 1)" \
    "pasakyta, kur DB kopija"

echo "── 3. Migracijų nebuvo + patikra krenta → atsukama kaip anksčiau ──"
K=$(paleisti 0 0 1)
tik "$([[ "$K" != "0" ]] && echo 1)" "agentas sustojo (grąžino $K)"
tik "$(grep -q 'atkeičiam KODĄ' "$T/isvestis" && echo 1)" "kodas atsuktas"
tik "$(grep -q 'Migracijų šiame diegime nebuvo' "$T/isvestis" && echo 1)" \
    "žurnale pasakyta, kodėl atsukti saugu"

echo "── 4. Patikros išvestis nebemetama į /dev/null ──"
tik "$(grep -q 'TyCINE-KLAIDOS-ZYME' "$T/isvestis" && echo 1)" \
    "curl klaidos tekstas atsidūrė žurnale"

echo
if [[ "$klaidos" == "0" ]]; then echo "VISKAS GERAI"; else echo "KLAIDŲ: $klaidos"; fi
exit "$klaidos"
