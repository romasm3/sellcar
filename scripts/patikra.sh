#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# PRIVALOMA PATIKRA PRIEŠ DIEGIMĄ (ir prieš kiekvieną commit'ą — pre-commit).
#
# 1. Šablonų skenavimas: {# be #} toje pačioje eilutėje (nutekėtų į puslapį)
# 2. Django testai: puslapiai be šablono komentarų + tuščios būsenos ikonos
#
# Paleidimas rankomis:  ./scripts/patikra.sh
# ═══════════════════════════════════════════════════════════════════════
set -u
cd "$(dirname "$0")/.."
KLAIDU=0

echo "── 1/2  Šablonai: neuždarytas {# … "
RADINIAI=$(grep -rn '{#' templates/ --include='*.html' \
           | grep -v '#}' | grep -v '\.bak' || true)
if [ -n "$RADINIAI" ]; then
    echo "KLAIDA: daugiaeilis {# #} komentaras nutekės į puslapį."
    echo "        Naudok {% comment %}…{% endcomment %}:"
    echo "$RADINIAI" | sed 's/^/        /'
    KLAIDU=1
else
    echo "        švaru"
fi

echo "── 2/2  Puslapių testai "
# PIPESTATUS — kitaip tikrintume „tail" būseną, o ne testų (krito nepastebėtai)
venv/bin/python manage.py test apps.listings \
    --testrunner=config.test_runner.BeDuombazes 2>&1 | tail -14
[ "${PIPESTATUS[0]}" -ne 0 ] && KLAIDU=1

if [ "$KLAIDU" -ne 0 ]; then
    echo
    echo "PATIKRA NEPRAĖJO — nediegti."
    exit 1
fi
echo
echo "Patikra praėjo."
