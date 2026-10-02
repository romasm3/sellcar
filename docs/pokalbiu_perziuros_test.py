# -*- coding: utf-8 -*-
"""
ADMINISTRACIJOS POKALBIŲ PERŽIŪRA — /administracija/pokalbiai/ ir žurnalas.

Tikrinam (tik testiniai naudotojai, laikina sqlite bazė):
  • be Profile.gali_matyti_pokalbius → /administracija/pokalbiai/ 403
    (ir superadministratoriui be šios teisės — ji atskira)
  • sąrašas rodo antraštes (dalyviai, skelbimas, žinučių skaičius), bet
    NE žinučių turinį
  • gijos GET ir POST be priežasties → turinio nėra, žurnalo įrašo nėra
  • „Kita" be paaiškinimo → turinio nėra
  • POST su priežastimi → turinys (originalas) rodomas IR sukuriamas
    žurnalo įrašas (kas, kada, gija, priežastis, tekstas, dalyviai)
  • administratorius negali išsiųsti žinutės dalyvio vardu (peržiūros
    puslapyje nėra formos, /conversations/<id>/ POST → 404, žinučių
    skaičius nepasikeičia)
  • žurnalo įrašo ištrinti negalima: žurnale nėra trynimo, POST/DELETE
    → 405, Django admin trynimas → 403, ORM delete()/update() atsisako
  • Django admin nerodo žinučių turinio ir neleidžia jo keisti
  • abiem dalyviams pokalbio lange — nuolatinė juosta
  • privatumo politikoje ir taisyklėse — skyrius apie peržiūrą, 24 mėn.
  • vartotojo eksporte — jo gijų peržiūros (kiek, kada, priežastis)

Paleidimas (TIK su laikina sqlite baze, NE prieš produkcijos DB):
    PATIKRA_DB=<laikinas failas> python docs/pokalbiu_perziuros_test.py
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patikra'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import json                                          # noqa: E402

from django.conf import settings                     # noqa: E402
from django.contrib.auth import get_user_model       # noqa: E402
from django.test import Client, override_settings    # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

from apps.accounts.models import Profile             # noqa: E402
from apps.conversations.models import Conversation, Message, PokalbioPerziura  # noqa: E402
from apps.listings.models import Listing             # noqa: E402

SARASAS = '/administracija/pokalbiai/'
ZURNALAS = '/administracija/zurnalas/'
SLAPTAS = 'Slaptas-pasiulymas-4711'
BANERIS = 'Pokalbiai saugomi ir ginčo atveju gali būti peržiūrėti AutoLeft administracijos.'
gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def naudotojas(vardas, **kw):
    U = get_user_model()
    el = f'{vardas}@perziura-patikra.lt'
    u = U.objects.filter(email=el).first() or U.objects.create_user(
        username=vardas, email=el, password='x-Patikra-123')
    for k, v in kw.items():
        setattr(u, k, v)
    u.save()
    return u


def klientas(u=None):
    c = Client()
    c.cookies[settings.LANGUAGE_COOKIE_NAME] = 'lt'
    if u is not None:
        c.force_login(u)
    return c


def h(a):
    return a.content.decode('utf-8', 'replace')


@override_settings(LANGUAGE_CODE='lt')
def main():
    setup_test_environment()
    pirkejas = naudotojas('perz_pirkejas')
    pardavejas = naudotojas('perz_pardavejas')
    darbuotojas = naudotojas('perz_darbuotojas')
    superas = naudotojas('perz_superas', is_superuser=True, is_staff=True)
    Profile.objects.filter(user=darbuotojas).update(gali_matyti_pokalbius=True)
    Profile.objects.filter(user__in=[pirkejas, pardavejas, superas]).update(gali_matyti_pokalbius=False)

    l = Listing.objects.filter(status='active').first()
    conv = Conversation.objects.create(listing=l)
    conv.participants.add(pirkejas, pardavejas)
    Message.objects.create(conversation=conv, sender=pirkejas, content=f'Ar tinka {SLAPTAS}?')
    Message.objects.create(conversation=conv, sender=pardavejas, content='Tinka, susitarkim.')
    zinuciu_pries = conv.messages.count()

    print('\n— Teisė')
    for kas, u in (('paprastas naudotojas', pirkejas), ('superadministratorius be teisės', superas)):
        tikrink(klientas(u).get(SARASAS).status_code == 403, f'{kas} → 403')
        tikrink(klientas(u).get(f'{SARASAS}{conv.pk}/').status_code == 403, f'{kas} gija → 403')
    a = klientas().get(SARASAS)
    tikrink(a.status_code == 302 and '/login' in a['Location'], 'neprisijungęs → prisijungimas')

    print('\n— Sąrašas: antraštės, ne turinys')
    c = klientas(darbuotojas)
    a = c.get(SARASAS, {'vartotojas': 'perz_pirkejas'})
    t = h(a)
    tikrink(a.status_code == 200 and f'data-gija="{conv.pk}"' in t, f'200, gija #{conv.pk} rasta pagal vartotoją')
    tikrink(pirkejas.email in t and pardavejas.email in t, 'rodomi dalyviai')
    tikrink(SLAPTAS not in t and 'Tinka, susitarkim' not in t, 'žinučių turinio NĖRA')
    t = h(c.get(SARASAS, {'skelbimas': str(l.pk)}))
    tikrink(f'data-gija="{conv.pk}"' in t, 'paieška pagal skelbimą')
    t = h(c.get(SARASAS, {'vartotojas': 'nera-tokio-zmogaus'}))
    tikrink(f'data-gija="{conv.pk}"' not in t, 'paieška filtruoja')

    print('\n— Gija be priežasties')
    pries = PokalbioPerziura.objects.count()
    t = h(c.get(f'{SARASAS}{conv.pk}/'))
    tikrink('data-priezasties-forma' in t and SLAPTAS not in t, 'GET — tik priežasties forma, turinio nėra')
    a = c.post(f'{SARASAS}{conv.pk}/', {})
    tikrink(a.status_code == 400 and SLAPTAS not in h(a) and 'data-klaida' in h(a),
            f'POST be priežasties → {a.status_code}, turinio nėra, klaida rodoma')
    a = c.post(f'{SARASAS}{conv.pk}/', {'priezastis': 'kita'})
    tikrink(SLAPTAS not in h(a), '„Kita" be paaiškinimo → turinio nėra')
    a = c.post(f'{SARASAS}{conv.pk}/', {'priezastis': 'smalsumas'})
    tikrink(SLAPTAS not in h(a), 'neegzistuojanti priežastis → turinio nėra')
    tikrink(PokalbioPerziura.objects.count() == pries, 'žurnalo įrašų neatsirado')

    print('\n— Gija su priežastimi')
    a = c.post(f'{SARASAS}{conv.pk}/', {'priezastis': 'gincas', 'paaiskinimas': 'Pirkėjas teigia, kad neatsiųsta'})
    t = h(a)
    tikrink(a.status_code == 200 and SLAPTAS in t and 'data-originalas' in t, 'turinys (originalas) rodomas')
    p = PokalbioPerziura.objects.order_by('-pk').first()
    tikrink(PokalbioPerziura.objects.count() == pries + 1 and p.perziurejo == darbuotojas
            and p.pokalbio_nr == conv.pk and p.priezastis == 'gincas'
            and p.paaiskinimas == 'Pirkėjas teigia, kad neatsiųsta' and p.kada is not None,
            'žurnale: kas, kada, gija, priežastis, tekstas')
    tikrink(set(p.dalyviai.all()) == {pirkejas, pardavejas}, 'žurnale: dalyviai')
    tikrink(a.get('Cache-Control') == 'no-store', 'atsakymas netalpinamas (no-store)')
    t2 = h(c.get(f'{SARASAS}{conv.pk}/'))
    tikrink(SLAPTAS not in t2, 'vėl atidarius (GET) — turinio vėl nėra, reikia naujos priežasties')

    print('\n— Tik skaitymas')
    tikrink('name="content"' not in t and 'textarea name="content"' not in t,
            'peržiūroje nėra žinutės rašymo formos')
    a = c.post(f'/conversations/{conv.pk}/', {'content': 'Rašau dalyvio vardu'})
    tikrink(a.status_code == 404 and conv.messages.count() == zinuciu_pries
            and not Message.objects.filter(content='Rašau dalyvio vardu').exists(),
            f'POST /conversations/<id>/ → {a.status_code}, žinutė neišsiųsta')
    a = klientas(superas).post(f'/conversations/{conv.pk}/', {'content': 'Rašau dalyvio vardu'})
    tikrink(a.status_code == 404 and conv.messages.count() == zinuciu_pries,
            'superadministratorius irgi negali rašyti į svetimą pokalbį')
    s = klientas(superas)
    m = conv.messages.first()
    a = s.get(f'/admin/conversations/message/{m.pk}/change/')
    tikrink(a.status_code == 200 and SLAPTAS not in h(a) and 'name="content"' not in h(a),
            f'Django admin: žinutės turinio nerodo, redaguoti negalima ({a.status_code})')
    a = s.post(f'/admin/conversations/message/{m.pk}/change/', {'content': 'pakeista'})
    m.refresh_from_db()
    tikrink(a.status_code == 403 and SLAPTAS in m.content, f'Django admin: žinutės keitimas → {a.status_code}')
    a = s.get('/admin/conversations/message/', {'q': SLAPTAS})
    tikrink(f'/admin/conversations/message/{m.pk}/change/' not in h(a),
            'Django admin: paieška pagal žinutės turinį jos neranda (turinys neieškomas)')
    a = s.get(f'/admin/conversations/conversation/{conv.pk}/change/')
    tikrink(SLAPTAS not in h(a), 'Django admin pokalbio puslapyje turinio nėra')

    print('\n— Žurnalas: tik skaitymas')
    t = h(c.get(ZURNALAS))
    tikrink(f'data-irasas="{p.pk}"' in t and 'Pirkėjas teigia' in t, 'žurnale matomas įrašas')
    tikrink('delete' not in t.lower().split('data-perziuru-zurnalas')[1] if 'data-perziuru-zurnalas' in t else False,
            'žurnale nėra trynimo mygtukų/formų')
    tikrink(klientas(superas).get(ZURNALAS).status_code == 200, 'superadministratorius mato žurnalą (priežiūrai)')
    tikrink(klientas(pirkejas).get(ZURNALAS).status_code == 403, 'paprastas naudotojas žurnalo nemato')
    tikrink(c.post(ZURNALAS, {'delete': p.pk}).status_code == 405, 'POST į žurnalą → 405')
    tikrink(c.delete(ZURNALAS).status_code == 405, 'DELETE į žurnalą → 405')
    a = s.post(f'/admin/conversations/pokalbioperziura/{p.pk}/delete/', {'post': 'yes'})
    tikrink(a.status_code == 403 and PokalbioPerziura.objects.filter(pk=p.pk).exists(),
            f'Django admin trynimas → {a.status_code}, įrašas liko')
    a = s.post('/admin/conversations/pokalbioperziura/', {'action': 'delete_selected', '_selected_action': [p.pk], 'post': 'yes'})
    tikrink(PokalbioPerziura.objects.filter(pk=p.pk).exists(), 'Django admin masinis trynimas — įrašas liko')
    for pav, veiksmas in (('obj.delete()', lambda: p.delete()),
                          ('QuerySet.delete()', lambda: PokalbioPerziura.objects.filter(pk=p.pk).delete()),
                          ('QuerySet.update()', lambda: PokalbioPerziura.objects.filter(pk=p.pk).update(priezastis='kita')),
                          ('save() esamo', lambda: (setattr(p, 'paaiskinimas', 'x'), p.save()))):
        try:
            veiksmas()
            ok = False
        except PermissionError:
            ok = True
        tikrink(ok, f'ORM {pav} → atsisakyta')
    p2 = PokalbioPerziura.objects.get(pk=p.pk)
    tikrink(p2.priezastis == 'gincas' and p2.paaiskinimas == 'Pirkėjas teigia, kad neatsiųsta', 'įrašas nepakitęs')

    print('\n— Juosta pokalbio lange')
    for kas, u in (('pirkėjui', pirkejas), ('pardavėjui', pardavejas)):
        t = h(klientas(u).get(f'/conversations/?conv={conv.pk}', follow=True))
        tikrink(BANERIS in t and 'Niekada nemokėkite iš anksto ir nesitarkite už AutoLeft ribų.' in t,
                f'{kas} — juosta yra')

    print('\n— Privatumo politika ir taisyklės')
    for url in ('/help/privacy/', '/help/terms/'):
        t = h(klientas().get(url, follow=True))
        tikrink('data-susirasinejimo-perziura' in t and '24 mėnesius po sandorio pabaigos' in t
                and 'ginčams spręsti' in t and 'sukčiavimui' in t and 'teisinėms pareigoms' in t,
                f'{url} — skyrius apie peržiūrą, 24 mėn.')

    print('\n— Vartotojo eksportas')
    d = json.loads(klientas(pirkejas).get('/accounts/settings/mano-duomenys/').content)
    pz = d.get('pokalbiu_perziuros', {})
    # Žurnalo įrašai netrinami — ankstesni paleidimai lieka; skaičiuojam šį pokalbį
    sios = [x for x in pz.get('perziuros', []) if x['pokalbis'] == conv.pk]
    tikrink(len(sios) == 1 and sios[0]['priezastis'] == 'gincas' and sios[0]['kada']
            and pz.get('kiek_kartu') == len(pz.get('perziuros', [])),
            f'pirkėjo eksporte — šio pokalbio 1 peržiūra su data ir priežastimi ({sios})')
    tikrink('Pirkėjas teigia' not in json.dumps(d, ensure_ascii=False)
            and darbuotojas.email not in json.dumps(d, ensure_ascii=False),
            'eksporte nėra vidinio paaiškinimo ir darbuotojo el. pašto')
    d2 = json.loads(klientas(darbuotojas).get('/accounts/settings/mano-duomenys/').content)
    tikrink(not [x for x in d2['pokalbiu_perziuros']['perziuros'] if x['pokalbis'] == conv.pk],
            'nedalyvavusio eksporte šio pokalbio peržiūrų nėra')

    print('\n— Ištrynus pokalbį žurnalas lieka')
    conv_pk = conv.pk
    conv.delete()
    p3 = PokalbioPerziura.objects.filter(pokalbio_nr=conv_pk).first()
    tikrink(p3 is not None and p3.pokalbis_id is None and p3.pokalbio_nr == conv_pk,
            'įrašas liko su pokalbio numeriu')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
