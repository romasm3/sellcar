"""Fix broken format string placeholders in .po files.

When Google Translate translates msgid like 'Hello %(name)s', it translates
the placeholder name too, breaking the format string. Example:
    msgid:  "Selected %(year)s and %(brand)s"
    msgstr: "Pasirinktas %(metų)s ir %(prekės_ženklas)s"  <- broken

Strategy (positional restore):
    1. Extract placeholders from msgid in order: [%(year)s, %(brand)s]
    2. Extract placeholders from msgstr in order: [%(metų)s, %(prekės_ženklas)s]
    3. If counts match -> replace msgstr placeholders by position with msgid ones
    4. If counts don't match -> clear msgstr (translation lost, needs redo)

This preserves existing translations whenever possible. No re-translation needed.

Usage:
    python fix_po_placeholders.py                  # all languages
    python fix_po_placeholders.py lt ru de         # specific languages
    python fix_po_placeholders.py --dry-run        # preview only
"""
import re
import sys
from pathlib import Path
import polib

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'

# %(name)s, %(name)d, %(name)f, etc.
PERCENT_NAMED = re.compile(r'%\([^)]+\)[sdifrxoXeEgG]')
# %s, %d, %f - positional
PERCENT_POSITIONAL = re.compile(r'%[sdifrxoXeEgG]')
# {name}, {0}, {} - brace format
BRACE = re.compile(r'\{[^{}]*\}')


def extract_placeholders_in_order(text):
    """Return dict of placeholders by kind, in left-to-right order."""
    return {
        'named': PERCENT_NAMED.findall(text),
        'positional': PERCENT_POSITIONAL.findall(text),
        'brace': BRACE.findall(text),
    }


def placeholders_match(msgid, msgstr):
    """True if msgstr placeholders match msgid's exactly (same multiset)."""
    if not msgstr.strip():
        return True
    mid = extract_placeholders_in_order(msgid)
    mst = extract_placeholders_in_order(msgstr)
    return (
        sorted(mid['named']) == sorted(mst['named']) and
        sorted(mid['positional']) == sorted(mst['positional']) and
        sorted(mid['brace']) == sorted(mst['brace'])
    )


def restore_by_position(msgid, msgstr):
    """Try to restore placeholders in msgstr positionally.

    Returns (new_msgstr, status):
        'ok'       -> already correct
        'restored' -> placeholders fixed, translation kept
        'cleared'  -> count mismatch, msgstr blanked
    """
    if not msgstr.strip():
        return msgstr, 'ok'

    if placeholders_match(msgid, msgstr):
        return msgstr, 'ok'

    mid = extract_placeholders_in_order(msgid)
    mst = extract_placeholders_in_order(msgstr)

    # Counts must match for positional restore to be safe
    if (len(mid['named']) != len(mst['named']) or
        len(mid['positional']) != len(mst['positional']) or
        len(mid['brace']) != len(mst['brace'])):
        return '', 'cleared'

    new = msgstr

    # Replace named placeholders one-by-one in order using a sentinel
    SENTINEL = '\x00PH\x00'
    for original, replacement in zip(mst['named'], mid['named']):
        new = new.replace(original, SENTINEL, 1)
        new = new.replace(SENTINEL, replacement, 1)

    # Brace placeholders the same way
    for original, replacement in zip(mst['brace'], mid['brace']):
        new = new.replace(original, SENTINEL, 1)
        new = new.replace(SENTINEL, replacement, 1)

    # Positional %s/%d are identical chars, no rewrite needed.

    if not placeholders_match(msgid, new):
        # Edge case (overlap, nesting) - bail out
        return '', 'cleared'

    return new, 'restored'


def fix_po_file(po_path, dry_run=False):
    print(f"\nFile: {po_path.relative_to(BASE_DIR)}")
    if not po_path.exists():
        print("  Not found, skipping")
        return 0, 0

    po = polib.pofile(str(po_path))
    restored = 0
    cleared = 0
    lang = po_path.parent.parent.name

    for entry in po:
        if entry.obsolete:
            continue

        if entry.msgid_plural:
            # Plural entries: msgstr_plural is a dict {0: '...', 1: '...', ...}
            for idx, txt in list(entry.msgstr_plural.items()):
                source = entry.msgid_plural if idx else entry.msgid
                new_txt, status = restore_by_position(source, txt)
                if status == 'restored':
                    print(f"  RESTORE [{lang}] (plural {idx}): {source[:50]}")
                    print(f"    was: {txt[:70]}")
                    print(f"    now: {new_txt[:70]}")
                    if not dry_run:
                        entry.msgstr_plural[idx] = new_txt
                    restored += 1
                elif status == 'cleared':
                    print(f"  CLEAR   [{lang}] (plural {idx}): {source[:50]}")
                    print(f"    was: {txt[:70]}")
                    if not dry_run:
                        entry.msgstr_plural[idx] = ''
                    cleared += 1
        else:
            new_txt, status = restore_by_position(entry.msgid, entry.msgstr)
            if status == 'restored':
                print(f"  RESTORE [{lang}]: {entry.msgid[:60]}")
                print(f"    was: {entry.msgstr[:70]}")
                print(f"    now: {new_txt[:70]}")
                if not dry_run:
                    entry.msgstr = new_txt
                restored += 1
            elif status == 'cleared':
                print(f"  CLEAR   [{lang}]: {entry.msgid[:60]}")
                print(f"    was: {entry.msgstr[:70]}")
                if not dry_run:
                    entry.msgstr = ''
                cleared += 1

    if (restored + cleared) > 0 and not dry_run:
        po.save(str(po_path))
        print(f"  >> Saved: {restored} restored, {cleared} cleared")
    elif (restored + cleared) > 0:
        print(f"  >> [DRY RUN] Would save: {restored} restored, {cleared} cleared")
    else:
        print(f"  OK (no broken entries)")

    return restored, cleared


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    if dry_run:
        args.remove('--dry-run')

    if args:
        languages = args
    else:
        languages = ['lt', 'lv', 'et', 'pl', 'de', 'ru', 'fr', 'es',
                     'zh_Hans', 'vi', 'ar', 'ko']

    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'WRITE'}")
    print(f"Languages: {', '.join(languages)}")
    print('=' * 70)

    total_restored = 0
    total_cleared = 0

    for lang in languages:
        po_path = LOCALE_DIR / lang / 'LC_MESSAGES' / 'django.po'
        r, c = fix_po_file(po_path, dry_run=dry_run)
        total_restored += r
        total_cleared += c

    print('\n' + '=' * 70)
    print(f"DONE. Restored: {total_restored}  |  Cleared: {total_cleared}")
    print('=' * 70)

    if total_cleared > 0:
        print(f"\n{total_cleared} entries had unrecoverable damage and were cleared.")
        print("These will fall back to English at runtime.")
        print("Re-translate them later in Rosetta or with translate_po.py")

    if not dry_run and (total_restored + total_cleared) > 0:
        print("\nNext step:")
        print("  python manage.py compilemessages")


if __name__ == '__main__':
    main()