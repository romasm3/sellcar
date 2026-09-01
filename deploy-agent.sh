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
KEEP_DB_DUMPS=10
### -----------------------

TS="$(date +%Y%m%d_%H%M%S)"
cd "$APP_DIR"
log() { echo "[$(date '+%H:%M:%S')] $*"; }

# Ko NEkopijuojam į/iš snapshot'o (kad neužtrintų venv, media, secretų, paties skripto)
EXCLUDES=(
  --exclude 'venv/'        --exclude '.env'
  --exclude 'media/'       --exclude 'staticfiles/'
  --exclude '.git/'        --exclude '__pycache__/'
  --exclude '*.pyc'        --exclude '*.log'
  --exclude '*.swp'        --exclude 'deploy-agent.sh'
  --exclude 'deploy-from-git.sh'    --exclude 'deploy/'
)

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
  if [[ "$engine" == *postgresql* ]]; then
    if PGPASSWORD="$pass" pg_dump -h "$host" -p "$port" -U "$user" "$name" > "$out" 2>/dev/null; then
      log "DB dumpas: $out"
    else
      log "DB: pg_dump nepavyko — tęsiam be DB kopijos."; rm -f "$out"
    fi
  elif [[ "$engine" == *sqlite3* ]]; then
    cp -f "$name" "${BACKUP_DIR}/db_${TS}.sqlite3" && log "DB kopija: ${BACKUP_DIR}/db_${TS}.sqlite3"
  else
    log "DB: nežinomas engine ($engine) — praleidžiam."
  fi
  ls -1t "${BACKUP_DIR}"/db_* 2>/dev/null | tail -n +$((KEEP_DB_DUMPS+1)) | xargs -r rm -f
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
  log "=== Deploy OK ==="
else
  log "❌ Health FAIL — atkeičiam KODĄ į paskutinę veikiančią versiją (old)."
  restore_code
  restart_service
  if health_check; then
    log "Kodas atsuktas — sena versija vėl veikia."
    log "SVARBU: jei buvo DB migracijų, kodą atsukom, bet DB — ne."
    log "        DB atkūrimui rankiniu būdu: ${BACKUP_DIR}/db_${TS}.sql"
  else
    log "DĖMESIO: net po atsukimo FAIL. Reikia rankinio įsikišimo."
  fi
  exit 1
fi