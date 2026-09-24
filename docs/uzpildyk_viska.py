
import os, time, polib

from google.cloud import translate_v2 as translate

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "/root/autoleft/google-translate-key.json")

client = translate.Client()

GOOGLE = {"en":"en","de":"de","fr":"fr","vi":"vi","ar":"ar","ru":"ru",

          "pl":"pl","es":"es","et":"et","lv":"lv","ko":"ko","zh_Hans":"zh-CN"}

def kintam(s):

    return ("%(" in s) or ("%s" in s) or ("%d" in s) or ("{" in s) or ("%%" in s)

for lang, gc in GOOGLE.items():

    p = "locale/%s/LC_MESSAGES/django.po" % lang

    if not os.path.exists(p):

        print(lang, "nera failo"); continue

    po = polib.pofile(p)

    todo = [e for e in po if not e.obsolete and not e.msgid_plural

            and e.msgid.strip() and not e.msgstr.strip() and not kintam(e.msgid)]

    print("%s: tuscios %d" % (lang, len(todo)))

    n = 0

    for i in range(0, len(todo), 50):

        grp = todo[i:i+50]

        try:

            res = client.translate([e.msgid for e in grp], target_language=gc, format_="text")

        except Exception as ex:

            print("  klaida:", ex); time.sleep(3); continue

        for e, r in zip(grp, res):

            e.msgstr = r["translatedText"]

            if "fuzzy" in e.flags:

                e.flags.remove("fuzzy")

            n += 1

        time.sleep(0.2)

        print("  %d/%d" % (min(i+50, len(todo)), len(todo)))

    po.save(p)

    print("%s: UZPILDYTA %d" % (lang, n))

print("BAIGTA")

