# -*- coding: utf-8 -*-
"""Vertimų skaneris registracijos/prisijungimo puslapiams.

Randa dvi problemas:
  A) {% trans %} eilutė su ANGLIŠKU msgid, kuriai lt/django.po neturi vertimo
     (arba jis pažymėtas #, fuzzy — Django tokį ignoruoja) -> lankytojas mato anglų k.
  B) matomas angliškas tekstas ŠALIA {% trans %} (neapvyniotas) -> nepasiekiamas vertėjui.

Naudojimas: venv/bin/python scan_auth_i18n.py [kalba ...]
"""
import io
import os
import re
import sys

TEMPLATES = [
    "templates/accounts/login.html",
    "templates/accounts/logout.html",
    "templates/accounts/register.html",
    "templates/accounts/password_change.html",
    "templates/accounts/password_reset.html",
    "templates/accounts/password_reset_confirm.html",
    "templates/accounts/password_reset_done.html",
    "templates/accounts/password_reset_complete.html",
    "templates/accounts/password_reset_email.html",
    "templates/accounts/password_reset_subject.txt",
    "templates/accounts/csrf_failure.html",
]

LANGS = sys.argv[1:] or ["lt", "ru", "en"]

# Lietuviškos raidės — jei msgid jų turi, jis jau lietuviškas.
LT_CHARS = set("ąčęėįšųūžĄČĘĖĮŠŲŪŽ")
CYRILLIC = re.compile(r"[Ѐ-ӿ]")


def load_po(lang):
    """{msgid: (msgstr, fuzzy)} iš locale/<lang>/LC_MESSAGES/django.po."""
    path = "locale/%s/LC_MESSAGES/django.po" % lang
    if not os.path.exists(path):
        return {}
    out = {}
    for block in io.open(path, encoding="utf-8").read().split("\n\n"):
        m = re.search(r'^msgid ((?:".*"\n?)+)', block, re.M)
        t = re.search(r'^msgstr ((?:".*"\n?)+)', block, re.M)
        if not m or not t or "msgid_plural" in block:
            continue
        def unq(raw):
            return "".join(p.replace('\\"', '"').replace("\\\\", "\\")
                           for p in re.findall(r'"((?:[^"\\]|\\.)*)"', raw))
        fuzzy = re.search(r"^#, .*fuzzy", block, re.M) is not None
        out[unq(m.group(1))] = (unq(t.group(1)), fuzzy)
    return out


def msgids(text):
    """{% trans 'x' %} / {% translate 'x' %} + {% blocktrans %}…{% endblocktrans %}."""
    found = []
    for m in re.finditer(r'{%\s*(?:trans|translate)\s+(["\'])(.*?)\1', text, re.S):
        found.append(m.group(2))
    for m in re.finditer(r"{%\s*blocktrans(?:late)?[^%]*%}(.*?){%\s*endblocktrans", text, re.S):
        found.append(m.group(1).strip())
    return found


def looks_english(s):
    """Angliškas msgid: be lietuviškų raidžių, be kirilicos, turi lotynišką žodį."""
    if CYRILLIC.search(s):
        return False
    if LT_CHARS & set(s):
        return False
    return bool(re.search(r"[A-Za-z]{3}", s))


def bare_english(text):
    """Matomas tekstas tarp > ir <, kuriame nėra šablono žymų — kandidatas į neapvyniotą."""
    out = []
    body = re.sub(r"(?s)<(script|style).*?</\1>", "", text)
    # blocktrans vidus JAU verčiamas — kitaip jo <a> tekstas duotų klaidingą pranešimą
    body = re.sub(r"(?s){%\s*blocktrans(?:late)?.*?{%\s*endblocktrans(?:late)?\s*%}", "", body)
    for m in re.finditer(r">([^<>{}]{3,})<", body):
        s = m.group(1).strip()
        if not s or not looks_english(s):
            continue
        if not re.search(r"[A-Za-z]{3}", s):
            continue
        if re.fullmatch(r"[\W\d]+", s):
            continue
        out.append(s)
    return out


def main():
    pos = {lang: load_po(lang) for lang in LANGS}
    total_a = total_b = 0
    for tpl in TEMPLATES:
        if not os.path.exists(tpl):
            print("(nėra) %s" % tpl)
            continue
        text = io.open(tpl, encoding="utf-8").read()
        ids = msgids(text)
        rows_a = []
        for mid in dict.fromkeys(ids):
            if not looks_english(mid):
                continue
            gaps = []
            for lang in LANGS:
                if lang == "en":
                    continue  # msgid jau angliškas — EN teisingas ir be vertimo
                msgstr, fuzzy = pos[lang].get(mid, ("", False))
                if not msgstr or fuzzy:
                    gaps.append(lang + (" (fuzzy)" if fuzzy and msgstr else ""))
            if gaps:
                rows_a.append((mid, gaps))
        rows_b = bare_english(text)
        if rows_a or rows_b:
            print("\n=== %s ===" % tpl)
            for mid, gaps in rows_a:
                print("  [A] be vertimo %-12s msgid: %s" % (",".join(gaps), mid))
            for s in rows_b:
                print("  [B] neapvyniota: %s" % s[:90])
        total_a += len(rows_a)
        total_b += len(rows_b)
    print("\nVISO: [A] be vertimo %d, [B] neapvyniota %d" % (total_a, total_b))


main()
