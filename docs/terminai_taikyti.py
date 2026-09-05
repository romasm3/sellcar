# -*- coding: utf-8 -*-
"""
Patvirtintus terminus iš docs/terminai.md įrašo į .po (ir .mo) failus.

    python docs/terminai_taikyti.py --bandymas     # tik parodo
    python docs/terminai_taikyti.py                # įrašo
    python docs/terminai_taikyti.py --sarasas ru   # kas dar neišversta

VIENAS ŠALTINIS — docs/terminai.md. Skriptas savo nuožiūra neverčia
nieko: ką randa lentelėse, tą ir įrašo.

msgid'ai projekte mišrūs (dalis lietuviški, dalis dar angliški), todėl
kiekvienam terminui ieškom abiejų variantų, nepaisant raidžių dydžio ir
galinio dvitaškio.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMINAI = os.path.join(BASE, 'docs', 'terminai.md')
KALBOS = ('ru', 'en', 'lt')          # kurių katalogų vertimus turim

try:
    import polib
except ImportError:
    sys.exit('Reikia polib: pip install polib')


def skaityk_terminus():
    """[(lt, ru, en)] iš visų docs/terminai.md lentelių."""
    eilutes = []
    for eil in open(TERMINAI, encoding='utf-8'):
        eil = eil.strip()
        if not eil.startswith('|') or eil.startswith('|---'):
            continue
        dalys = [d.strip() for d in eil.strip('|').split('|')]
        if len(dalys) != 3:
            continue
        if dalys[0] in ('Lietuviškai',):      # antraštė
            continue
        eilutes.append(tuple(dalys))
    return eilutes


def raktas(tekstas):
    """Palyginimui: be raidžių dydžio, be galinio dvitaškio ir tarpų."""
    return re.sub(r'\s+', ' ', str(tekstas or '')).strip().rstrip(':').lower()


def zodynas():
    """{palyginimo raktas: {'lt':…, 'ru':…, 'en':…}}

    Sudėtinės eilutės („Visi / Visos") neturi teisės užimti trumpo
    msgid'o („All"): kitaip sąsajoje atsirastų „Visi / Visos" ten, kur
    telpa vienas žodis. Todėl kiekvienai kalbai atskirai praleidžiam
    porą, kurioje msgid be „ / ", o vertimas su juo — tokį atvejį
    padengia „Sudėtinės eilutės" lentelė.
    """
    z = {}
    for lt, ru, en in skaityk_terminus():
        irasas = {'lt': lt, 'ru': ru, 'en': en}
        for variantas in (lt, en):            # msgid gali būti bet kuris
            if not variantas or variantas == '—' or variantas.startswith('~'):
                continue                      # „~" — vertimas, bet ne msgid
            r = raktas(variantas.lstrip('=').strip())
            turimas = z.setdefault(r, {})
            for kalba, reiksme in irasas.items():
                if reiksme in ('', '—') or reiksme.startswith('='):
                    continue                  # nėra vertimo arba tik msgid
                reiksme = reiksme.lstrip('~').strip()
                if kalba in turimas:
                    continue                  # pirmoji lentelė laimi
                if ' / ' in reiksme and ' / ' not in variantas:
                    continue                  # sudėtinė — praleidžiam
                turimas[kalba] = reiksme
    return z


def pagal_pavidala(msgid, vertimas):
    """Vertimas prisitaiko prie msgid pavidalo.

    Sąsajoje tas pats terminas pasitaiko ir sakinio viduryje („nuo 5 000
    iki 20 000"), ir su dvitaškiu („Kaina:"). Lentelė duoda pamatinį
    variantą, o čia grąžinam jį TOKIO PAT pavidalo, koks msgid — kitaip
    vidury sakinio atsirastų didžioji raidė, o iš „Kaina:" dingtų
    dvitaškis.
    """
    v = vertimas
    raides = [z for z in msgid if z.isalpha()]
    if raides and all(z.islower() for z in raides):
        v = v[:1].lower() + v[1:]
    elif raides and all(z.isupper() for z in raides) and len(raides) > 1:
        v = v.upper()
    if msgid.rstrip().endswith(':') and not v.rstrip().endswith(':'):
        v = v.rstrip() + ':'
    return v


def po_kelias(kalba):
    return os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')


def visi_msgid():
    """{raktas: (msgid, occurrences)} iš VISŲ katalogų.

    Katalogai nevienodo amžiaus: lietuviškas turi ~4700 eilučių, rusiškas
    ~2900. Terminas gali būti kode ir šablonuose, bet dar nepasiekęs
    rusiško .po — tada jo tiesiog nėra ką užpildyti. Iš čia sužinom, kad
    toks msgid tikras, ir pridedam jį trūkstamam katalogui.
    """
    visi = {}
    for kalba in KALBOS + ('pl', 'de', 'lv', 'et'):
        kelias = po_kelias(kalba)
        if not os.path.exists(kelias):
            continue
        for irasas in polib.pofile(kelias):
            if irasas.obsolete or irasas.msgid_plural:
                continue
            visi.setdefault(raktas(irasas.msgid), (irasas.msgid, irasas.occurrences))
    return visi


def taikyk(kalba, z, bandymas=False, tikri=None):
    kelias = po_kelias(kalba)
    if not os.path.exists(kelias):
        print('  %s — nėra katalogo' % kalba)
        return 0, 0, []
    po = polib.pofile(kelias)
    uzpildyta = pakeista = 0
    pakeitimai = []
    for irasas in po:
        if irasas.obsolete or irasas.msgid_plural:
            continue
        rastas = z.get(raktas(irasas.msgid))
        if not rastas:
            continue
        naujas = rastas.get(kalba)
        if not naujas:
            continue
        naujas = pagal_pavidala(irasas.msgid, naujas)
        senas = irasas.msgstr
        if senas == naujas and 'fuzzy' not in irasas.flags:
            continue
        if senas and senas != naujas:
            pakeista += 1
            pakeitimai.append((irasas.msgid, senas, naujas))
        elif not senas:
            uzpildyta += 1
        if not bandymas:
            irasas.msgstr = naujas
            # Patvirtintas vertimas negali likti fuzzy: tokia eilutė
            # nekompiliuojama į .mo ir vartotojui nerodoma.
            irasas.flags = [f for f in irasas.flags if f != 'fuzzy']
            irasas.previous_msgid = None
    # Terminai, kurių šitame kataloge dar nėra, bet kode jie tikri
    pridėta = 0
    turimi = {raktas(i.msgid) for i in po if not i.obsolete}
    for r, reiksmes in sorted(z.items()):
        if r in turimi or kalba not in reiksmes:
            continue
        tikras = (tikri or {}).get(r)
        if tikras and raktas(tikras[0]) == r:
            msgid, vietos = tikras
        else:
            # Kataloguose tokio msgid dar nėra. Dalis terminų ten ir
            # negali patekti: filtrų užrašai ateina per `_(f['label'])`,
            # reikšmės — iš DB, o xgettext kintamojo nemato. Sąrašas jų
            # laukia apps/listings/translatable_db.py, o iki kito
            # makemessages įrašom tiesiai.
            msgid, vietos = reiksmes['lt'], []
            if raktas(msgid) != r:
                continue
        pridėta += 1
        if not bandymas:
            po.append(polib.POEntry(
                msgid=msgid,
                msgstr=pagal_pavidala(msgid, reiksmes[kalba]),
                occurrences=vietos,
                comment='terminai.md — patvirtintas vertimas'))
    if not bandymas:
        po.save(kelias)
        po.save_as_mofile(kelias[:-3] + '.mo')
    return uzpildyta, pakeista, pakeitimai, pridėta


SRITYS = [
    ('Paieška ir filtrai', ('search_config', 'panels', 'partials/fields',
                            'search_panel', 'search_rail', 'advanced')),
    ('Skelbimo forma',     ('_create', 'listing_create', 'contact_block', 'forms.py')),
    ('Skelbimo puslapis',  ('listing_detail', '_pardavejo', 'detail')),
    ('Sąrašai ir kortelės', ('_list.html', 'listing_list', 'kort', 'browse')),
    ('Žinutės',            ('conversations',)),
    ('Paskyra ir nustatymai', ('accounts', 'profile', 'settings')),
    ('Įmonės',             ('imones',)),
    ('Mokėjimai',          ('payments', 'stripe', 'plan')),
    ('Laiškai',            ('emails', 'templates/emails')),
    ('Administravimas',    ('admin',)),
]


def sritis(irasas):
    vietos = ' '.join(f for f, _l in irasas.occurrences)
    for vardas, raktai in SRITYS:
        if any(r in vietos for r in raktai):
            return vardas
    return 'Kita'


def sarasas(kalba):
    """Neperžiūrėtos eilutės su kontekstu, sugrupuotos pagal sritį.

    Dvi dalys: visai neišverstos ir pažymėtos `#, fuzzy` (išverstos
    mašinos, bet nepatvirtintos — tokios eilutės į .mo nekompiliuojamos
    ir vartotojui nerodomos, todėl praktiškai irgi neišverstos).
    """
    po = polib.pofile(po_kelias(kalba))
    grupes = {}
    for irasas in po:
        if irasas.obsolete:
            continue
        if irasas.translated() and 'fuzzy' not in irasas.flags:
            continue
        busena = 'fuzzy' if 'fuzzy' in irasas.flags else 'tuščia'
        grupes.setdefault(sritis(irasas), []).append((busena, irasas))

    print('# NEPERŽIŪRĖTOS EILUTĖS — %s' % kalba)
    print('# msgid yra lietuviškas arba angliškas tekstas iš kodo.')
    print('# „fuzzy" = mašinos vertimas, nepatvirtintas, vartotojui NERODOMAS.')
    print('# Patvirtinti terminai — docs/terminai.md, jų čia nėra.\n')
    viso = 0
    for vardas, _r in SRITYS + [('Kita', ())]:
        eilutes = grupes.get(vardas)
        if not eilutes:
            continue
        print('\n═══ %s (%d) %s' % (vardas, len(eilutes), '═' * 20))
        for busena, irasas in sorted(eilutes, key=lambda x: x[1].msgid.lower()):
            vieta = ', '.join('%s:%s' % (f, l) for f, l in irasas.occurrences[:2])
            print('\n%s' % irasas.msgid)
            if busena == 'fuzzy':
                print('    dabar (nepatvirtinta): %s' % irasas.msgstr)
            print('    # %s' % (vieta or 'be konteksto'))
            viso += 1
    print('\n# viso neperžiūrėtų: %d (%s)' % (viso, kalba))


def main():
    if '--sarasas' in sys.argv:
        sarasas(sys.argv[sys.argv.index('--sarasas') + 1])
        return
    bandymas = '--bandymas' in sys.argv
    z = zodynas()
    print('Terminų lentelėse: %d eilutės, %d msgid variantų'
          % (len(skaityk_terminus()), len(z)))
    print('Režimas: %s\n' % ('BANDYMAS (nieko nerašom)' if bandymas else 'ĮRAŠOM'))
    tikri = visi_msgid()
    for kalba in KALBOS:
        u, p, sarasiukas, pr = taikyk(kalba, z, bandymas, tikri)
        print('%-3s užpildyta %3d | perrašyta %3d | pridėta %3d' % (kalba, u, p, pr))
        for msgid, senas, naujas in sarasiukas:
            print('      „%s": %r → %r' % (msgid, senas, naujas))
    if bandymas:
        print('\n(bandymas — failai nepaliesti)')


if __name__ == '__main__':
    main()
