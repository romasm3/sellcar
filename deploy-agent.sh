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
  # shellcheck disable=SC1091
  source "${VENV}/bin/activate"
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  deactivate
}

### --- eiga ---
log "=== Deploy pradžia ($TS) ==="

# Pirmas paleidimas: dabartinis (veikiantis) kodas tampa baseline
if [[ ! -d "$LAST_GOOD" ]]; then
  log "Pirmas paleidimas — kuriam baseline iš dabartinio kodo."
  snapshot_code
  log "Baseline sukurtas: $LAST_GOOD"
fi

dump_db
apply
restart_service

if health_check; then
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