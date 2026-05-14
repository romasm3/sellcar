"""
Pakeičia visus tipografinius ir tiesius apostrofus FR vertimuose į saugias alternatyvas.
Saugu: keičia TIK msgstr eilutes, NE msgid.

Naudojimas:
    python fix_french_apostrophes.py

Failas: locale/fr/LC_MESSAGES/django.po
"""

import re
from pathlib import Path

PO_PATH = Path("locale/fr/LC_MESSAGES/django.po")

# Pakeitimai: dažniausi FR apostrofų contraction'ai → versijos be apostrofo
REPLACEMENTS = [
    # apostrofas + samogarsiai (l', d', n', s', m', t', j', c', qu')
    ("l'année", "année"),
    ("L'année", "Année"),
    ("l'annonce", "annonce"),
    ("L'annonce", "Annonce"),
    ("l'adresse", "adresse"),
    ("L'adresse", "Adresse"),
    ("l'État", "État"),
    ("l'État", "État"),
    ("l'utilisateur", "utilisateur"),
    ("l'option", "option"),
    ("l'accueil", "accueil"),
    ("l'a", "a"),
    ("l'i", "i"),
    ("l'o", "o"),
    ("l'u", "u"),
    ("l'e", "e"),

    ("d'utiliser", "utiliser"),
    ("d'abord", "préalablement"),
    ("d'aide", "aide"),
    ("d'effacement", "effacement"),
    ("d'autres", "autres"),
    ("d'occasion", "occasion"),
    ("d'entretien", "entretien"),
    ("d'avoir", "avoir"),
    ("d'un", "un"),
    ("d'une", "une"),
    ("d'expédition", "expédition"),

    ("n'a", "na"),
    ("n'avez", "avez"),
    ("n'est", "est"),
    ("n'hésitez", "hesitez"),
    ("N'hésitez", "Hesitez"),

    ("s'inscrire", "inscrire"),
    ("S'inscrire", "Inscrire"),
    ("s'abonner", "abonner"),
    ("S'abonner", "Abonner"),

    ("j'accepte", "je accepte"),
    ("J'accepte", "Je accepte"),

    ("c'est", "cest"),
    ("C'est", "Cest"),

    ("qu'on", "que on"),
    ("qu'il", "que il"),
    ("qu'elle", "que elle"),
    ("Qu'on", "Que on"),

    ("Jusqu'à", "Maximum"),
    ("jusqu'à", "jusque"),

    ("aujourd'hui", "ce jour"),

    # Bendras safety net: bet koks `'` po raidės pakeičiamas į ` `
    # Tai paskutinė linija — jei kažką praleidome, vis tiek FR JS neluš.
]


def fix_msgstr_block(msgstr_text: str) -> str:
    """Pakeičia apostrofus tik msgstr turinyje."""
    fixed = msgstr_text
    for old, new in REPLACEMENTS:
        fixed = fixed.replace(old, new)

    # Safety net: bet koks likęs apostrofas (' arba ') tarp raidžių
    # pakeičiamas į tarpą. Tai garantuoja kad JS niekada nelūš.
    fixed = re.sub(r"(?<=\w)['\u2019](?=\w)", " ", fixed)
    fixed = re.sub(r"(?<=\w)['\u2019]", "", fixed)
    fixed = re.sub(r"['\u2019](?=\w)", "", fixed)

    return fixed


def process_po_file(path: Path) -> int:
    """Apdoroja .po failą. Grąžina pakeistų msgstr eilučių skaičių."""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    fixed_count = 0

    new_lines = []
    for line in lines:
        # Tik msgstr eilutės su tekstu kabutėse
        if line.startswith('msgstr "') or (line.startswith('"') and len(new_lines) > 0
                                            and (new_lines[-1].startswith('msgstr')
                                                 or new_lines[-1].startswith('"'))):
            # Patikrinam ar paskutinė įrašyta eilutė buvo msgstr arba continuation
            is_msgstr_continuation = False
            for prev in reversed(new_lines):
                if prev.startswith("msgstr"):
                    is_msgstr_continuation = True
                    break
                if prev.startswith("msgid") or prev.strip() == "":
                    break

            if line.startswith('msgstr "') or is_msgstr_continuation:
                original = line
                fixed = fix_msgstr_block(line)
                if original != fixed:
                    fixed_count += 1
                new_lines.append(fixed)
                continue

        new_lines.append(line)

    new_content = "\n".join(new_lines)

    # Backup
    backup = path.with_suffix(".po.backup")
    backup.write_text(content, encoding="utf-8")
    print(f"Backup sukurtas: {backup}")

    path.write_text(new_content, encoding="utf-8")
    return fixed_count


if __name__ == "__main__":
    if not PO_PATH.exists():
        print(f"KLAIDA: {PO_PATH} nerastas. Paleisk script'ą iš projekto root'o.")
        exit(1)

    count = process_po_file(PO_PATH)
    print(f"Pakeista {count} eilučių faile {PO_PATH}")
    print("\nDabar paleisk:")
    print("  django-admin compilemessages")
    print("\nTada restart Django server + Ctrl+Shift+R browser'yje.")