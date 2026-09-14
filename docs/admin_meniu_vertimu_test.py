# -*- coding: utf-8 -*-
"""
ADMIN MENIU: DU PUNKTAI — DU SKIRTINGI PAVADINIMAI.

Kas buvo. Meniu po „ADMINISTRATORIUS" abu punktai rodė „Vidutiniai
vartotojai", nors veda į skirtingus puslapius:

    /admin-moderate/            → vartotojų moderavimas
    /accounts/admin/dealers/    → prekiautojų moderavimas

Msgid'ai buvo skirtingi („Moderate users" ir „Moderate dealers") — klydo
vertimas: angliškas „moderate" perskaitytas kaip būdvardis („vidutinis"),
o ne veiksmažodis („moderuoti"). Ta pati klaida buvo VISOSE kalbose:
„Moderate Benutzer", „Usuarios moderados", „Умеренные пользователи",
„中度用户"…

Paleidimas:  python docs/admin_meniu_vertimu_test.py
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

gerai = blogai = 0
def tikrink(s, k):
    global gerai, blogai
    if s:
        gerai += 1
    else:
        blogai += 1
        print('  NEPAVYKO: ' + k)
def antraste(t):
    print('\n── ' + t + ' ' + '─' * max(0, 52 - len(t)))


def vertimas(kalba, msgid):
    kelias = os.path.join(BASE, 'locale', kalba, 'LC_MESSAGES', 'django.po')
    turinys = io.open(kelias, encoding='utf-8').read()
    m = re.search(r'^msgid "%s"\nmsgstr "(.*?)"$' % re.escape(msgid),
                  turinys, re.M)
    return m.group(1) if m else None


KALBOS = sorted(k for k in os.listdir(os.path.join(BASE, 'locale'))
                if os.path.isdir(os.path.join(BASE, 'locale', k)))

# Klaidingo vertimo šaknys: „vidutinis / nuosaikus" kiekviena kalba.
BLOGOS = re.compile(
    r'vidutin|vidēj|mõõduk|moderad|modéré|umiarkowan|умерен|'
    r'среднего|trung bình|中度|中等|보통|중도|Gemäßigt|Moderate Benutzer',
    re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════
antraste('1. Msgid\'ai atskiri')

base_html = io.open(os.path.join(BASE, 'templates/base.html'),
                    encoding='utf-8').read()
tikrink(base_html.count('{% trans "Moderate users" %}') == 2,
        'meniu punktas „Moderate users" ne dviejose vietose')
tikrink(base_html.count('{% trans "Moderate dealers" %}') == 2,
        'meniu punktas „Moderate dealers" ne dviejose vietose')
tikrink("{% url 'admin_users_list' %}" in base_html
        and "{% url 'accounts:admin_dealers_list' %}" in base_html,
        'meniu nuorodos veda ne į tuos puslapius')

# Vertėjo užuomina — kad mašininis vertimas vėl nesuklystų
tikrink(base_html.count('{# Translators:') >= 2,
        'nėra vertėjo užuominos prie „Moderate …"')


# ═══════════════════════════════════════════════════════════════════
antraste('2. Kiekviena kalba: du SKIRTINGI teisingi vertimai')

for kalba in KALBOS:
    vart = vertimas(kalba, 'Moderate users')
    prek = vertimas(kalba, 'Moderate dealers')
    if vart is None and prek is None:
        continue
    tikrink(vart and prek, '%s: trūksta vertimo' % kalba)
    if not (vart and prek):
        continue
    tikrink(vart != prek,
            '%s: abu punktai vienodi — „%s"' % (kalba, vart))
    tikrink(not BLOGOS.search(vart),
            '%s: „moderate" išversta kaip „vidutinis" — „%s"' % (kalba, vart))
    tikrink(not BLOGOS.search(prek),
            '%s: „moderate" išversta kaip „vidutinis" — „%s"' % (kalba, prek))


# ═══════════════════════════════════════════════════════════════════
antraste('3. Lietuviškai — būtent tie pavadinimai')

tikrink(vertimas('lt', 'Moderate users') == 'Vartotojų moderavimas',
        'lt vartotojai: „%s"' % vertimas('lt', 'Moderate users'))
tikrink(vertimas('lt', 'Moderate dealers') == 'Prekiautojų moderavimas',
        'lt prekiautojai: „%s"' % vertimas('lt', 'Moderate dealers'))


# ═══════════════════════════════════════════════════════════════════
antraste('4. Lankytojų statistikos nuoroda meniu')

tikrink("{% url 'admin_visitors_stats' %}" in base_html,
        'meniu nėra nuorodos į lankytojų statistiką')
tikrink(base_html.count('{% trans "Lankytojų statistika" %}') == 2,
        'nuoroda ne abiejuose meniu (darbalaukio ir mobiliame)')


print('\n' + '═' * 60)
print('gerai: %d, nepavyko: %d' % (gerai, blogai))
sys.exit(1 if blogai else 0)
