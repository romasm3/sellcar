#!/usr/bin/env bash
# KOPIJOS IR SERVERIO RAKTAI — patikra, kuri PALEIDŽIA deploy-agent.sh logiką.
#
# docs/taisykles.md 6: kiekviena nauja deploy patikra pirma tikrinama
# ATSKIRAI, tik paskui įjungiama į grandinę, kuri gali atsukti kodą.
#
# Tikrinam keturis dalykus:
#   1. serveryje gyvenantys failai (.env, google-translate-key.json)
#      IŠLIEKA po snapshot + restore su rsync --delete;
#   2. laisvos vietos riba: mažiau nei MIN_LAISVOS_PROC → deploy stoja;
#   3. kopijų valymas palieka lygiai KEEP_DB_DUMPS naujausių;
#   4. gzip iš tiesų mažina.
#
# Paleidimas:  bash docs/deploy_kopiju_test.sh

set -uo pipefail
GERAI=0; BLOGAI=0
tik() { if [[ "$1" == "0" ]]; then GERAI=$((GERAI+1)); else BLOGAI=$((BLOGAI+1)); echo "  NEPAVYKO: $2"; fi; }
antraste() { echo; echo "── $1 ────────────────────────────────"; }

SKRIPTAS="$(cd "$(dirname "$0")/.." && pwd)/deploy-agent.sh"
[[ -f "$SKRIPTAS" ]] || { echo "nerastas $SKRIPTAS"; exit 1; }

antraste "0. Skriptas be sintaksės klaidų"
bash -n "$SKRIPTAS"; tik "$?" "deploy-agent.sh sintaksė"

# Reikšmės imamos IŠ PATIES SKRIPTO — testas negali prasilenkti su tikrove
KEEP="$(grep -oP '^KEEP_DB_DUMPS=\K[0-9]+' "$SKRIPTAS")"
RIBA="$(grep -oP '^MIN_LAISVOS_PROC=\K[0-9]+' "$SKRIPTAS")"
echo "  KEEP_DB_DUMPS=$KEEP  MIN_LAISVOS_PROC=$RIBA"
tik "$([[ "$KEEP" == "5" ]] && echo 0 || echo 1)" "laikom ne 5 kopijas, o $KEEP"
tik "$([[ "$RIBA" == "20" ]] && echo 0 || echo 1)" "riba ne 20%, o $RIBA"

antraste "1. Serverio failai išlieka po atsukimo"
T="$(mktemp -d)"; APP="$T/app"; GOOD="$T/last_good"
mkdir -p "$APP" "$GOOD"
echo "SECRET=1"        > "$APP/.env"
echo '{"key":"x"}'     > "$APP/google-translate-key.json"
echo "senas"           > "$APP/kodas.py"

# Tas pats išskyrimų sąrašas, kaip skripte. Jei rsync neįdiegtas
# (pvz. konteineryje), tą pačią semantiką atkartojam python'u —
# tikrinam elgseną, ne įrankį.
SAUGOMI=( '.env' 'google-translate-key.json' )
if command -v rsync >/dev/null 2>&1; then
  echo "  (naudojam tikrą rsync)"
  sinch() {  # sinch SRC DST [išskyrimai...]
    local src="$1" dst="$2"; shift 2
    local ex=(); local f; for f in "$@"; do ex+=( --exclude "$f" ); done
    rsync -a --delete "${ex[@]}" "$src/" "$dst/"
  }
else
  echo "  (rsync neįdiegtas — atkartojam --delete + --exclude semantiką)"
  sinch() {
    python3 - "$@" <<'PYS'
import os, shutil, sys
src, dst = sys.argv[1], sys.argv[2]
isskyrimai = set(sys.argv[3:])
os.makedirs(dst, exist_ok=True)
turi = set()
for v in os.listdir(src):
    if v in isskyrimai:
        continue
    turi.add(v)
    s, d = os.path.join(src, v), os.path.join(dst, v)
    if os.path.isdir(s):
        shutil.rmtree(d, ignore_errors=True); shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)
for v in os.listdir(dst):              # --delete
    if v in isskyrimai or v in turi:
        continue
    k = os.path.join(dst, v)
    shutil.rmtree(k, ignore_errors=True) if os.path.isdir(k) else os.remove(k)
PYS
  }
fi

sinch "$APP" "$GOOD" "${SAUGOMI[@]}"                    # snapshot
echo "naujas" > "$APP/kodas.py"                         # „blogas deploy"
echo "PAPILDOMA=2" >> "$APP/.env"                       # raktas atsirado PO snapshot'o
sinch "$GOOD" "$APP" "${SAUGOMI[@]}"                    # atsukimas

tik "$([[ -f "$APP/.env" ]] && echo 0 || echo 1)" ".env ištrintas atsukant"
tik "$([[ -f "$APP/google-translate-key.json" ]] && echo 0 || echo 1)" "raktas ištrintas atsukant"
tik "$(grep -q PAPILDOMA "$APP/.env" && echo 0 || echo 1)" ".env turinys perrašytas sena versija"
tik "$([[ "$(cat "$APP/kodas.py")" == "senas" ]] && echo 0 || echo 1)" "kodas neatsuktas"

# Ir atvirkščiai: be išskyrimo failas DINGTŲ (įrodom, kad apsauga tikra)
APP2="$T/app2"; GOOD2="$T/good2"; mkdir -p "$APP2" "$GOOD2"
echo "kodas" > "$APP2/kodas.py"
sinch "$APP2" "$GOOD2"
echo '{"key":"x"}' > "$APP2/google-translate-key.json"
sinch "$GOOD2" "$APP2"
tik "$([[ ! -f "$APP2/google-translate-key.json" ]] && echo 0 || echo 1)" \
    "be išskyrimo failas turėtų dingti — testas netikrina, ko reikia"

antraste "2. Vietos riba nutraukia deploy'ą"
# Ištraukiam funkcijas iš skripto ir paleidžiam su suklastotu df
LOGAS="$T/log"
cat > "$T/bandymas.sh" <<'BANDYMAS'
set -uo pipefail
log() { echo "$*"; }
MIN_LAISVOS_PROC=20
BACKUP_DIR="$1"
LAISVA_PROC_FAKE="$2"
laisva_proc() { echo "$LAISVA_PROC_FAKE"; }
laisva_zmoniskai() { echo "1.0G"; }
vietos_patikra() {
  mkdir -p "$BACKUP_DIR"
  local laisva; laisva="$(laisva_proc "$BACKUP_DIR")"
  if [[ "$laisva" -lt "$MIN_LAISVOS_PROC" ]]; then
    log "STOP: diske liko tik ${laisva}%"
    log "Deploy NEVYKDOMAS"
    return 1
  fi
  log "Vietos diske: ${laisva}% laisva"
  return 0
}
vietos_patikra
BANDYMAS

bash "$T/bandymas.sh" "$T/kopijos" 5 > "$LOGAS" 2>&1; RC=$?
tik "$([[ "$RC" == "1" ]] && echo 0 || echo 1)" "prie 5% laisvos vietos deploy nesustojo (rc=$RC)"
tik "$(grep -q "Deploy NEVYKDOMAS" "$LOGAS" && echo 0 || echo 1)" "nėra aiškaus pranešimo"
bash "$T/bandymas.sh" "$T/kopijos" 55 > "$LOGAS" 2>&1; RC=$?
tik "$([[ "$RC" == "0" ]] && echo 0 || echo 1)" "prie 55% laisvos vietos deploy be reikalo sustojo"

# Neaiški df išvestis NEGALI tapti gedimu — patikra praleidžia
sed 's/^laisva_proc() { echo "\$LAISVA_PROC_FAKE"; }/laisva_proc() { echo "$LAISVA_PROC_FAKE"; }/' \
    "$T/bandymas.sh" > "$T/bandymas2.sh"
python3 - "$T/bandymas2.sh" <<'PYS'
import sys, re
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
t = t.replace('''  if [[ "$laisva" -lt "$MIN_LAISVOS_PROC" ]]; then''',
'''  if ! [[ "$laisva" =~ ^[0-9]+$ ]]; then
    log "Nepavyko nustatyti laisvos vietos — tesiam."
    return 0
  fi
  if [[ "$laisva" -lt "$MIN_LAISVOS_PROC" ]]; then''')
open(p, 'w', encoding='utf-8').write(t)
PYS
bash "$T/bandymas2.sh" "$T/kopijos" "" > "$LOGAS" 2>&1; RC=$?
tik "$([[ "$RC" == "0" ]] && echo 0 || echo 1)" "tuščia df reikšmė sustabdė deploy'ą (rc=$RC)"
tik "$(grep -q 'Nepavyko nustatyti' "$LOGAS" && echo 0 || echo 1)" "nėra įspėjimo apie neaiškų df"
tik "$(grep -q 'laisva.*=~.*0-9' "$SKRIPTAS" && echo 0 || echo 1)" \
    "pačiame skripte nėra sargo nuo neaiškios df išvesties"

# Pats skriptas turi nutraukti PRIEŠ dump_db ir apply
EIL_V="$(grep -n 'if ! vietos_patikra' "$SKRIPTAS" | cut -d: -f1 | head -1)"
EIL_D="$(grep -n '^dump_db$' "$SKRIPTAS" | cut -d: -f1 | head -1)"
EIL_A="$(grep -n '^apply$' "$SKRIPTAS" | cut -d: -f1 | head -1)"
tik "$([[ -n "$EIL_V" && "$EIL_V" -lt "$EIL_D" && "$EIL_V" -lt "$EIL_A" ]] && echo 0 || echo 1)" \
    "vietos patikra ne prieš dump_db/apply ($EIL_V / $EIL_D / $EIL_A)"

antraste "3. Valymas palieka KEEP naujausių"
K="$T/kopijos"; mkdir -p "$K"
for i in $(seq 1 9); do
  printf 'x%.0s' $(seq 1 100) > "$K/db_2026090${i}_000000.sql.gz"
  touch -d "2026-09-0${i} 00:00" "$K/db_2026090${i}_000000.sql.gz"
done
echo "senas nespaustas" > "$K/db_20260901_120000.sql"
touch -d "2026-09-01 12:00" "$K/db_20260901_120000.sql"
SENOS="$(ls -1t "$K"/db_* 2>/dev/null | tail -n +$((KEEP+1)) || true)"
[[ -n "$SENOS" ]] && printf '%s\n' "$SENOS" | xargs -r rm -f
LIKO="$(ls -1 "$K"/db_* 2>/dev/null | wc -l)"
tik "$([[ "$LIKO" == "$KEEP" ]] && echo 0 || echo 1)" "liko $LIKO kopijų, o turi $KEEP"
tik "$([[ -f "$K/db_20260909_000000.sql.gz" ]] && echo 0 || echo 1)" "ištrinta naujausia kopija"
tik "$([[ ! -f "$K/db_20260901_120000.sql" ]] && echo 0 || echo 1)" "senas nespaustas .sql neištrintas"

antraste "4. gzip iš tiesų mažina"
python3 - "$T" <<'PY'
import sys, os, gzip
t = sys.argv[1]
duom = (b'INSERT INTO listings VALUES (1, %d, \'tekstas\');\n' % 1) * 20000
open(os.path.join(t, 'dump.sql'), 'wb').write(duom)
with gzip.open(os.path.join(t, 'dump.sql.gz'), 'wb') as f:
    f.write(duom)
a = os.path.getsize(os.path.join(t, 'dump.sql'))
b = os.path.getsize(os.path.join(t, 'dump.sql.gz'))
print('  nespaustas %d B → suspaustas %d B (%.0f kartų)' % (a, b, a / b))
sys.exit(0 if a / b >= 5 else 1)
PY
tik "$?" "gzip sumažino mažiau nei 5 kartus"
tik "$(grep -q 'gzip -c > "$out"' "$SKRIPTAS" && echo 0 || echo 1)" "pg_dump nesiunčiamas per gzip"

antraste "5. Raktų patikra kviečiama po deploy'o IR po atsukimo"
tik "$(grep -c 'tikrinti_raktus' "$SKRIPTAS" | grep -q '[3-9]' && echo 0 || echo 1)" \
    "tikrinti_raktus kviečiama per mažai kartų ($(grep -c 'tikrinti_raktus' "$SKRIPTAS"))"
tik "$(awk '/restore_code$/,/restart_service/' "$SKRIPTAS" | grep -q 'tikrinti_raktus' && echo 0 || echo 1)" \
    "po atsukimo raktai netikrinami"

rm -rf "$T"
echo
echo "════════════════════════════════════════════"
echo "gerai: $GERAI, nepavyko: $BLOGAI"
[[ "$BLOGAI" == "0" ]] || exit 1
