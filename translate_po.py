"""
Auto-translate Django .po files using Google Translate API.

USAGE:
    # Dry-run (parodo kiek bus išversta, NIEKO nedaro):
    python translate_po.py --dry-run

    # Test ant vienos kalbos (Lietuvių):
    python translate_po.py --lang lt

    # Paleisti VISOM kalbom (po vieną kalbą po kito):
    python translate_po.py --all

    # Konkrečios kalbos:
    python translate_po.py --lang lt es de

REIKIA:
    pip install google-cloud-translate polib
    google-translate-key.json projekto šaknyje
"""
import os
import sys
import time
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# SETUP — credentials BEFORE importing google.cloud
# ═══════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent
CREDS_PATH = BASE_DIR / 'google-translate-key.json'

if not CREDS_PATH.exists():
    print(f"❌ ERROR: {CREDS_PATH} not found!")
    sys.exit(1)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(CREDS_PATH)

import polib
from google.cloud import translate_v2 as translate

# ═══════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════

LOCALE_DIR = BASE_DIR / 'locale'

# Map: Django locale folder → Google Translate language code
LANGUAGE_MAP = {
    'lt': 'lt',           # Lithuanian
    'lv': 'lv',           # Latvian
    'et': 'et',           # Estonian
    'pl': 'pl',           # Polish
    'de': 'de',           # German
    'ru': 'ru',           # Russian
    'fr': 'fr',           # French
    'es': 'es',           # Spanish
    'zh_Hans': 'zh-CN',   # Chinese Simplified
    'vi': 'vi',           # Vietnamese
    'ar': 'ar',           # Arabic
    'ko': 'ko',           # Korean
    # 'en' praleidžiame — tai source language
}

# These strings should NEVER be translated (language names stay native)
SKIP_STRINGS = {
    'English', 'Lietuvių', 'Latviešu', 'Eesti', 'Polski',
    'Deutsch', 'Русский', 'Français', 'Español', '中文',
    'Tiếng Việt', 'العربية', '한국어',
    'SellCar',  # brand name
}


# ═══════════════════════════════════════════════════════════
# TRANSLATION
# ═══════════════════════════════════════════════════════════

def translate_text(client, text, target_lang):
    """Translate single text via Google Translate API."""
    if not text or not text.strip():
        return text
    if text in SKIP_STRINGS:
        return text

    try:
        result = client.translate(
            text,
            target_language=target_lang,
            source_language='en',
            format_='text',
        )
        return result['translatedText']
    except Exception as e:
        print(f"  ⚠️  Translate error for '{text[:50]}...': {e}")
        return ''


def translate_po_file(po_path, target_lang, dry_run=False):
    """Translate a single .po file."""
    print(f"\n{'═' * 60}")
    print(f"📂 {po_path.relative_to(BASE_DIR)}")
    print(f"🌐 Target language: {target_lang}")

    if not po_path.exists():
        print(f"  ❌ File not found, skipping")
        return

    po = polib.pofile(str(po_path))

    total = len(po)
    already_translated = 0
    will_translate = 0
    skipped_strings = 0

    # Pirmas pass — suskaičiuojam kas reikia versti
    entries_to_translate = []
    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgstr.strip():
            already_translated += 1
            continue
        if entry.msgid in SKIP_STRINGS:
            entries_to_translate.append((entry, entry.msgid))  # palikti kaip yra
            skipped_strings += 1
            continue
        if not entry.msgid.strip():
            continue
        will_translate += 1
        entries_to_translate.append((entry, None))

    print(f"  📊 Total entries: {total}")
    print(f"  ✓ Already translated: {already_translated}")
    print(f"  ⏭  Skip (language names): {skipped_strings}")
    print(f"  → Will translate: {will_translate}")

    if dry_run:
        print(f"  🔍 DRY-RUN: skipping actual translation")
        return

    if will_translate == 0:
        print(f"  ✓ Nothing to translate, all done!")
        return

    # Antras pass — verčiam
    client = translate.Client()
    translated_count = 0
    error_count = 0
    start_time = time.time()

    for entry, preset_value in entries_to_translate:
        if preset_value is not None:
            # SKIP_STRINGS — nustatom tą patį tekstą
            entry.msgstr = preset_value
            continue

        translated = translate_text(client, entry.msgid, target_lang)
        if translated:
            entry.msgstr = translated
            translated_count += 1
        else:
            error_count += 1

        # Progress bar
        if translated_count % 25 == 0 and translated_count > 0:
            elapsed = time.time() - start_time
            rate = translated_count / elapsed if elapsed > 0 else 0
            eta = (will_translate - translated_count) / rate if rate > 0 else 0
            print(f"    Progress: {translated_count}/{will_translate} "
                  f"({translated_count*100//will_translate}%) "
                  f"~{rate:.1f}/sec  ETA: {eta:.0f}s")

        # Rate limiting — saugu nuo API throttling
        time.sleep(0.05)

    # Save
    po.save(str(po_path))
    elapsed = time.time() - start_time

    print(f"  ✅ Done in {elapsed:.1f}s — translated: {translated_count}, errors: {error_count}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Auto-translate Django .po files')
    parser.add_argument('--dry-run', action='store_true', help='Show what will be done, no actual translation')
    parser.add_argument('--lang', nargs='+', help='Specific languages to translate (e.g. --lang lt es de)')
    parser.add_argument('--all', action='store_true', help='Translate ALL languages')
    args = parser.parse_args()

    if not args.dry_run and not args.lang and not args.all:
        print("❌ Specify --dry-run, --lang <code>, or --all")
        print(__doc__)
        sys.exit(1)

    # Pasirinkti kurias kalbas versti
    if args.all or args.dry_run:
        languages = list(LANGUAGE_MAP.keys())
    else:
        languages = []
        for lang in args.lang:
            if lang not in LANGUAGE_MAP:
                print(f"⚠️  Unknown language: {lang}. Available: {list(LANGUAGE_MAP.keys())}")
                continue
            languages.append(lang)

    if not languages:
        print("❌ No valid languages specified")
        sys.exit(1)

    print(f"╔{'═' * 58}╗")
    print(f"║  Django .po Auto-Translator (Google Translate API)       ║")
    print(f"╚{'═' * 58}╝")
    print(f"Languages: {', '.join(languages)}")
    if args.dry_run:
        print(f"Mode: DRY-RUN (no actual translation)")

    overall_start = time.time()

    for django_lang in languages:
        google_lang = LANGUAGE_MAP[django_lang]
        po_path = LOCALE_DIR / django_lang / 'LC_MESSAGES' / 'django.po'
        translate_po_file(po_path, google_lang, dry_run=args.dry_run)

    total_elapsed = time.time() - overall_start
    print(f"\n{'═' * 60}")
    print(f"🎉 ALL DONE in {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    print(f"{'═' * 60}")
    print(f"\nNext step:")
    print(f"  python manage.py compilemessages")


if __name__ == '__main__':
    main()