#!/usr/bin/env bash
# deploy-agent.sh — deploy su SNAPSHOT rollback'u.
# Eiga: redaguoji kodą serveryje -> paleidi šitą. Git atsukimui NENAUDOJAMAS.
#
# Kaip veikia "old/new":
#   last_good/  = paskutinės VEIKIANČIOS versijos kodo kopija (tai "old").
#   APP_DIR/    = dabartinis (ką tik redaguotas) kodas (tai "new").
#   Deploy: migrate+collectstatic -> restart -> testas.
#     OK   -> last_good atnaujinamas į naują versiją.
#     FAIL -> kodas atkeičiamas iš last_good (grįžtam į old) + restart.
#   DB nudempinamas prieš deploy (kodo atsukimas automatinis, DB — rankinis).

set -euo pipefail

### ---- KONFIGŪRACIJA ----
APP_DIR="/root/autoleft"
VENV="${APP_DIR}/venv"
SERVICE="gunicorn.service"
GUNICORN_SOCK="/run/gunicorn.sock"
HEALTH_HOST="autoleft.com"               # turi būti ALLOWED_HOSTS sąraše
HEALTH_PATH="/"                          # arba /health/ jei turėsi
LAST_GOOD="/root/autoleft_last_good"     # "old" kodo kopija
BACKUP_DIR="/root/autoleft_backups"      # DB dumpai
KEEP_DB_DUMPS=5                          # laikom paskutines 5 (buvo 10)
MIN_LAISVOS_PROC=20                      # mažiau — deploy nutrūksta
### -----------------------

TS="$(date +%Y%m%d_%H%M%S)"
cd "$APP_DIR"
log() { echo "[$(date '+%H:%M:%S')] $*"; }

# ── FAILAI, KURIE GYVENA TIK SERVERYJE ───────────────────────────────
# Jų nėra git'e ir jų negalima nei įsidėti į snapshot'ą, nei atsukti:
# `restore_code` naudoja `rsync --delete`, tad failas, atsiradęs PO
# paskutinio snapshot'o, atsukimo metu būtų IŠTRINTAS. Būtent taip
# 2026-09 dingo google-translate-key.json ir nustojo veikti vertimas.
#
# VIENAS sąrašas: iš jo daromi ir rsync išskyrimai, ir patikra po deploy'o.
SAUGOMI_FAILAI=(
  '.env'
  'google-translate-key.json'
)

# Ko NEkopijuojam į/iš snapshot'o (kad neužtrintų venv, media, secretų, paties skripto)
EXCLUDES=(
  --exclude 'venv/'
  --exclude 'media/'       --exclude 'staticfiles/'
  --exclude '.git/'        --exclude '__pycache__/'
  --exclude '*.pyc'        --exclude '*.log'
  --exclude '*.swp'        --exclude 'deploy-agent.sh'
  --exclude 'deploy-from-git.sh'    --exclude 'deploy/'
)
for _f in "${SAUGOMI_FAILAI[@]}"; do EXCLUDES+=( --exclude "$_f" ); done

# ── AR SERVERIO RAKTAI VIETOJE ───────────────────────────────────────
# Kviečiama po kiekvieno deploy'o IR po atsukimo. Grąžina 1, jei bent
# vieno nebėra; žurnale — ryškus įspėjimas, ne tyli eilutė.
tikrinti_raktus() {
  local truksta=0 f
  for f in "${SAUGOMI_FAILAI[@]}"; do
    if [[ -e "${APP_DIR}/${f}" ]]; then
      log "Raktai: ${f} — vietoje."
    else
      truksta=1
      log "🔴 DINGO SERVERIO FAILAS: ${APP_DIR}/${f}"
      log "🔴 Jo nėra git'e — deploy jo neatstatys. Reikia įdėti ranka."
      [[ "$f" == 'google-translate-key.json' ]] && \
        log "🔴 Be jo NEVEIKIA vertimas pokalbiuose (docs/vertimo-raktas.md)."
      [[ "$f" == '.env' ]] && \
        log "🔴 Be jo svetainė NEPAKILS."
    fi
  done
  return "$truksta"
}

# ── AR UŽTEKS VIETOS DISKE ───────────────────────────────────────────
# Tikrinam PRIEŠ kopiją ir PRIEŠ bet kokį kodo keitimą: geriau nutraukti
# deploy'ą su aiškiu pranešimu, nei užpildyti diską ir palikti serverį,
# kuriame nebeveikia niekas.
laisva_proc() { df -P "$1" | awk 'NR==2 { gsub(/%/,"",$5); print 100-$5 }'; }
laisva_zmoniskai() { df -Ph "$1" | awk 'NR==2 { print $4 }'; }

vietos_patikra() {
  mkdir -p "$BACKUP_DIR"
  local laisva; laisva="$(laisva_proc "$BACKUP_DIR" 2>/dev/null || true)"
  # Jei df atsakė netikėtai, patikra TYLI ir praleidžia. Tuščia reikšmė
  # bash'e lyginant su -lt virsta nuliu, tad be šito sargo neaiški df
  # išvestis būtų amžinai stabdžiusi deploy'ą — patikra negali tapti
  # gedimu (docs/taisykles.md 6).
  if ! [[ "$laisva" =~ ^[0-9]+$ ]]; then
    log "⚠️  Nepavyko nustatyti laisvos vietos (df: '${laisva}') — tęsiam."
    return 0
  fi
  if [[ "$laisva" -lt "$MIN_LAISVOS_PROC" ]]; then
    log "❌ STOP: diske liko tik ${laisva}% (${MIN_LAISVOS_PROC}% riba)."
    log "   Laisva: $(laisva_zmoniskai "$BACKUP_DIR"). Kopijos: ${BACKUP_DIR}"
    log "   Deploy NEVYKDOMAS — kodas nepaliestas, svetainė veikia kaip veikė."
    log "   Vietos atlaisvinti (paliekant dvi naujausias kopijas):"
    log "     ls -1t ${BACKUP_DIR}/db_* | tail -n +3 | xargs -r rm -f"
    return 1
  fi
  log "Vietos diske: ${laisva}% laisva ($(laisva_zmoniskai "$BACKUP_DIR"))."
  return 0
}

restart_service() { log "Restartinam $SERVICE"; systemctl restart "$SERVICE"; }

health_check() {
  local tries=10 delay=2
  for ((i=1; i<=tries; i++)); do
    if curl -fsS --max-time 5 --unix-socket "$GUNICORN_SOCK" \
         -H "Host: $HEALTH_HOST" "http://localhost${HEALTH_PATH}" >/dev/null 2>&1; then
      log "Health OK ($i/$tries)"; return 0
    fi
    log "Health dar ne... ($i/$tries)"; sleep "$delay"
  done
  return 1
}

snapshot_code() { mkdir -p "$LAST_GOOD"; rsync -a --delete "${EXCLUDES[@]}" "${APP_DIR}/" "${LAST_GOOD}/"; }
restore_code()  { rsync -a --delete "${EXCLUDES[@]}" "${LAST_GOOD}/" "${APP_DIR}/"; }

# ── PO ATSUKIMO DARBINIS KATALOGAS TURI LIKTI ŠVARUS ─────────────────
# restore_code perrašo sekamus failus sena versija, o git HEAD lieka rodyti
# į naują (blogą) commit'ą. Tada `git status` pilnas pakeitimų, ir kitas
# `git pull` nulūžta su „local changes would be overwritten by merge":
# taimeris sukasi, bet nieko nebeparsiunčia, ir atrodo, kad jis mirė.
#
# deploy-from-git.sh tai jau daro (git reset --hard "$LOCAL"), BET tik
# tada, kai deploy-agent.sh paleistas per jį. Paleidus agentą tiesiogiai
# — o taip daroma rankiniu būdu — niekas git istorijos nesutvarkydavo.
#
# Į kurią versiją grąžinti, žinom iš pačios atsuktos kopijos: restore_code
# parneša ir last_good/VERSIJA su TA PAČIA sha, kurią atitinka failai.
sutvarkyti_po_atsukimo() {
  if ! git -C "$APP_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    log "Darbinis katalogas ne git — tvarkyti nėra ko."
    return 0
  fi

  # Nieko netrinam be pėdsako: jei kas nors buvo redagavęs kodą serveryje,
  # pataisa lieka atsargoje, o ne dingsta.
  if ! git -C "$APP_DIR" diff --quiet HEAD 2>/dev/null; then
    mkdir -p "$BACKUP_DIR"
    local pataisa="${BACKUP_DIR}/pries_reset_${TS}.patch"
    git -C "$APP_DIR" diff HEAD > "$pataisa" 2>/dev/null || true
    log "Darbinio katalogo pakeitimai išsaugoti: $pataisa"
  fi

  local sha=""
  if [[ -f "${LAST_GOOD}/VERSIJA" ]]; then
    sha="$(tr -d "[:space:]" < "${LAST_GOOD}/VERSIJA")"
  fi
  if [[ -z "$sha" || "$sha" == "nezinoma" ]]; then
    log "DĖMESIO: nežinau, į kurią versiją grąžinti git — nėra ${LAST_GOOD}/VERSIJA."
    log "         Darbinis katalogas liko nešvarus; kitas git pull nulūš."
    log "         Rankomis: git -C ${APP_DIR} log --oneline -3"
    log "                   git -C ${APP_DIR} reset --hard <veikianti-sha>"
    return 0
  fi

  if ! git -C "$APP_DIR" cat-file -e "${sha}^{commit}" 2>/dev/null; then
    log "DĖMESIO: commit'as ${sha} nerastas — git nenustatytas."
    return 0
  fi

  if git -C "$APP_DIR" reset --hard "$sha" >/dev/null 2>&1; then
    log "git reset --hard ${sha} — istorija suderinta su atsuktais failais."
  else
    log "DĖMESIO: git reset nepavyko — reikia rankinio įsikišimo."
    return 0
  fi

  # Pasitikrinam, o ne tikim: kitas pull turi praeiti.
  if [[ -z "$(git -C "$APP_DIR" status --porcelain --untracked-files=no)" ]]; then
    log "Darbinis katalogas švarus — kitas git pull veiks."
  else
    log "DĖMESIO: katalogas VIS DAR nešvarus:"
    git -C "$APP_DIR" status --short --untracked-files=no | sed "s/^/         /" \
      | while read -r e; do log "$e"; done
  fi
}

dump_db() {
  mkdir -p "$BACKUP_DIR"
  local out="${BACKUP_DIR}/db_${TS}.sql"
  local sm
  sm="$(grep -oP "DJANGO_SETTINGS_MODULE['\"]\s*,\s*['\"]\K[^'\"]+" manage.py || true)"
  [[ -z "$sm" ]] && { log "DB: nerastas settings modulis — praleidžiam dumpą."; return 0; }
  local conf
  conf="$(DJANGO_SETTINGS_MODULE="$sm" "${VENV}/bin/python" - <<'PY' 2>/dev/null || true
import django
django.setup()
from django.conf import settings
d = settings.DATABASES['default']
print('|'.join([d.get('ENGINE',''), d.get('NAME',''), str(d.get('USER','')),
                str(d.get('PASSWORD','')), str(d.get('HOST','') or 'localhost'),
                str(d.get('PORT','') or 5432)]))
PY
)"
  [[ -z "$conf" ]] && { log "DB: nepavyko nuskaityti nustatymų — praleidžiam dumpą."; return 0; }
  IFS='|' read -r engine name user pass host port <<<"$conf"
  # SUSPAUSTA. Nespaustas dumpas buvo ~2,8 GB, o po kiekvieno deploy'o
  # atsirasdavo dar vienas — per parą ~20 GB. gzip sumažina ~10 kartų.
  if [[ "$engine" == *postgresql* ]]; then
    out="${out}.gz"
    if PGPASSWORD="$pass" pg_dump -h "$host" -p "$port" -U "$user" "$name" \
         2>/dev/null | gzip -c > "$out"; then
      log "DB dumpas: $out ($(du -h "$out" | cut -f1))"
    else
      log "DB: pg_dump nepavyko — tęsiam be DB kopijos."; rm -f "$out"
    fi
  elif [[ "$engine" == *sqlite3* ]]; then
    out="${BACKUP_DIR}/db_${TS}.sqlite3.gz"
    if gzip -c "$name" > "$out"; then
      log "DB kopija: $out ($(du -h "$out" | cut -f1))"
    else
      log "DB: kopija nepavyko — tęsiam."; rm -f "$out"
    fi
  else
    log "DB: nežinomas engine ($engine) — praleidžiam."
  fi

  # Laikom paskutines KEEP_DB_DUMPS, senesnes trinam. Šablonas „db_*"
  # gaudo ir senus nespaustus .sql, ir naujus .sql.gz.
  local senos
  senos="$(ls -1t "${BACKUP_DIR}"/db_* 2>/dev/null | tail -n +$((KEEP_DB_DUMPS+1)) || true)"
  if [[ -n "$senos" ]]; then
    local kiek; kiek="$(printf '%s\n' "$senos" | wc -l)"
    printf '%s\n' "$senos" | xargs -r rm -f
    log "Senos kopijos ištrintos: ${kiek} (laikom ${KEEP_DB_DUMPS} naujausias)."
  fi
  log "Kopijos: $(ls -1 "${BACKUP_DIR}"/db_* 2>/dev/null | wc -l) vnt., "\
      "viso $(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1), "\
      "diske laisva $(laisva_zmoniskai "$BACKUP_DIR") ($(laisva_proc "$BACKUP_DIR")%)."
}

apply() {
  # Versijos žymė: iš jos settings.GIT_SHA, o iš jo — <meta name="versija">
  # kiekviename puslapyje. Failas NEĮTRAUKTAS į EXCLUDES, tad keliauja su
  # snapshot'u: atsukus kodą grįžta ir sena žyma, o ne apgaulinga nauja.
  git -C "$APP_DIR" rev-parse --short=12 HEAD > "${APP_DIR}/VERSIJA" 2>/dev/null \
    || echo "nezinoma" > "${APP_DIR}/VERSIJA"
  log "Versija: $(cat "${APP_DIR}/VERSIJA")"

  # shellcheck disable=SC1091
  source "${VENV}/bin/activate"
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  deactivate
}

# ── Statinių talpyklos patikra ────────────────────────────────────────
# Kodėl: statiniai vardai turi turinio maišą (style.<maišas>.css). Jei
# collectstatic nesuveikė arba manifestas liko senas, gyvas HTML rodys į
# seną failą — lankytojas gaus seną CSS su nauju žymėjimu, t. y.
# sulaužytą puslapį, ir to nesimatys jokiame vietiniame teste.
STATINIU_MANIFESTAS="${APP_DIR}/staticfiles/staticfiles.json"

statiniu_bukle() {
  # Grąžina „<manifesto-mtime> <css-vardas-gyvame-HTML>"
  local mt html vardas
  mt="$(stat -c %Y "$STATINIU_MANIFESTAS" 2>/dev/null || echo 0)"
  # `X-Forwarded-Proto: https` BŪTINAS: produkcijoje SECURE_SSL_REDIRECT
  # įjungtas, o per soketą užklausa atrodo neapsaugota, tad Django grąžina
  # 301 su tuščiu kūnu. Be šitos antraštės patikra „nematydavo" HTML ir
  # klaidingai skelbdavo, kad maišas neveikia (2026-09-01 dėl to buvo
  # atsuktas visiškai sveikas deploy'as).
  html="$(curl -fsSL --max-time 10 --unix-socket "$GUNICORN_SOCK" \
            -H "Host: $HEALTH_HOST" -H "X-Forwarded-Proto: https" \
            "http://localhost/" 2>/dev/null || true)"
  # `|| true` BŪTINAS: skriptas sukasi su `set -euo pipefail`, o grep be
  # atitikmens grąžina 1 ir pipefail tą 1 paverčia viso priskyrimo klaida —
  # skriptas nutrūkdavo dar PRIEŠ deploy'ą. Pirmą kartą atitikmens ir
  # negali būti: senas HTML sumaišyto vardo neturi.
  vardas="$(printf '%s' "$html" | grep -oE 'style\.[a-z0-9]+\.css' | head -1 || true)"
  printf '%s %s' "$mt" "$vardas"
}

tikrinti_statinius() {
  local pries_mt="$1" pries_css="$2"
  local dabar mt css
  dabar="$(statiniu_bukle)"; mt="${dabar%% *}"; css="${dabar##* }"

  if [[ ! -f "$STATINIU_MANIFESTAS" ]]; then
    log "❌ Nėra ${STATINIU_MANIFESTAS} — collectstatic nesuveikė."
    return 1
  fi
  if [[ "$mt" == "$pries_mt" ]]; then
    log "❌ staticfiles.json neatsinaujino (mtime $mt) — collectstatic nieko nepadarė."
    return 1
  fi
  if [[ -z "$css" ]]; then
    log "❌ Gyvas HTML nerodo į sumaišytą style.<maišas>.css."
    log "   Patikrink STORAGES['staticfiles'] nustatymuose."
    return 1
  fi
  # Jei šablonai ar statiniai keitėsi, o CSS vardas ne — maišas
  # neperskaičiuotas, ir naršyklės liks prie senojo failo.
  if [[ -n "$pries_css" && "$css" == "$pries_css" && "$SABLONAI_KEITESI" == "1" ]]; then
    log "❌ Šablonai/statiniai keitėsi, bet CSS vardas liko $css."
    log "   Naršyklės gaus seną failą — deploy stabdomas."
    return 1
  fi
  log "Statiniai OK: $css (manifestas atnaujintas)"
  return 0
}

### --- eiga ---
log "=== Deploy pradžia ($TS) ==="

# Pirmas paleidimas: dabartinis (veikiantis) kodas tampa baseline
if [[ ! -d "$LAST_GOOD" ]]; then
  log "Pirmas paleidimas — kuriam baseline iš dabartinio kodo."
  snapshot_code
  log "Baseline sukurtas: $LAST_GOOD"
fi

# Ar šiame deploy'e keitėsi šablonai arba statiniai — tada CSS vardas
# PRIVALO pasikeisti.
SABLONAI_KEITESI=0
if [[ -d "$LAST_GOOD" ]] && ! diff -rq --no-dereference \
      "${LAST_GOOD}/templates" "${APP_DIR}/templates" >/dev/null 2>&1; then
  SABLONAI_KEITESI=1
fi
if [[ -d "$LAST_GOOD" ]] && ! diff -rq --no-dereference \
      "${LAST_GOOD}/static" "${APP_DIR}/static" >/dev/null 2>&1; then
  SABLONAI_KEITESI=1
fi
[[ "$SABLONAI_KEITESI" == "1" ]] && log "Šablonai/statiniai keitėsi — tikrinsim CSS vardą."

PRIES="$(statiniu_bukle)"
PRIES_MT="${PRIES%% *}"
PRIES_CSS="${PRIES##* }"

# Vietos patikra — PIRMA, dar nieko nepakeitus.
if ! vietos_patikra; then
  exit 2
fi

dump_db
apply
restart_service

# Gyvybės klausimas yra TIK health_check: ar puslapis atsidaro.
# Statinių maišas — pageidavimas. Anksčiau jis buvo sujungtas su health
# per `&&`, ir viena nepavykusi smulkmena atsukdavo visiškai veikiantį
# darbą. Dabar jis tik įspėja.
if health_check; then
  if tikrinti_statinius "$PRIES_MT" "$PRIES_CSS"; then
    :
  else
    log "⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi."
    log "⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės"
    log "⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:"
    log "⚠️    curl -s https://${HEALTH_HOST}/ | grep -o 'style\.[a-z0-9]*\.css'"
  fi
  log "✅ Veikia — atnaujinam 'last_good' į naują versiją."
  snapshot_code
  if tikrinti_raktus; then
    log "=== Deploy OK ==="
  else
    log "=== Deploy OK, BET TRŪKSTA SERVERIO FAILŲ (žr. 🔴 aukščiau) ==="
  fi
else
  log "❌ Health FAIL — atkeičiam KODĄ į paskutinę veikiančią versiją (old)."
  restore_code
  sutvarkyti_po_atsukimo
  # Atsukimas naudoja rsync --delete — būtent čia anksčiau dingdavo
  # serveryje gyvenantys failai. Dabar jie išskirti, o patikra tai
  # patvirtina garsiai.
  tikrinti_raktus || true
  restart_service
  if health_check; then
    log "Kodas atsuktas — sena versija vėl veikia."
    log "SVARBU: jei buvo DB migracijų, kodą atsukom, bet DB — ne."
    log "        DB atkūrimui rankiniu būdu: ${BACKUP_DIR}/db_${TS}.sql.gz"
    log "        (gunzip -c FAILAS.gz | psql -U VARTOTOJAS BAZĖ)"
  else
    log "DĖMESIO: net po atsukimo FAIL. Reikia rankinio įsikišimo."
  fi
  exit 1
fi