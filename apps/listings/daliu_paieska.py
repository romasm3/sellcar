# -*- coding: utf-8 -*-
"""
DALIŲ TEKSTINĖ PAIEŠKA — pavadinimas, aprašymas ir detalės numeris.

Iki šiol `q` ieškojo TIK pavadinime, o detalės numerio (`oem_code`) —
niekur. Skelbimo #880 nerasdavo nei pagal „51128075031", nei pagal
„bamperis".

Detalės numeris rašomas kaip pakliuvo: „51128075031", „5112 807 5031",
„51128-075031", o viename lauke jų būna keli, atskirti „ / ". Todėl
lyginam NORMALIZUOTAS reikšmes — be tarpų, brūkšnelių ir taškų, didžiosiomis.
Pasvirasis brūkšnys PALIEKAMAS: jis skiria kodus, o jį išmetus du gretimi
kodai suliptų ir paieška rastų nesamą numerį.

Normalizacija daroma DB pusėje (`Replace`/`Upper`), todėl veikia ir su
sqlite (vietinė patikra), ir su PostgreSQL (produkcija), o indeksų
nereikia keisti.
"""
import re

from django.db.models import Q, Value
from django.db.models.functions import Replace, Upper

# Ką išmetam prieš lyginant. „/" sąmoningai NEĮTRAUKTAS.
SIUKSLES = (' ', '-', '.', '_')

# Keli kodai viename lauke atskiriami pasviruoju brūkšniu.
SKYRIKLIS = re.compile(r'\s*/\s*')


def normalizuok(tekstas):
    """„5112 807-5031" → „51128075031"."""
    tekstas = (tekstas or '').upper()
    for zenklas in SIUKSLES:
        tekstas = tekstas.replace(zenklas, '')
    return tekstas


def kodai(tekstas):
    """„A / B / C" → ['A', 'B', 'C']. Tuščias laukas → []."""
    if not tekstas:
        return []
    return [k.strip() for k in SKYRIKLIS.split(str(tekstas).strip()) if k.strip()]


def su_normalizuotu_oem(qs):
    """Prideda `_oem_norm` stulpelį — oem_code be tarpų, brūkšnelių, taškų."""
    # ?q ir ?oem kartu — antrą kartą to paties stulpelio nededam.
    if '_oem_norm' in qs.query.annotations:
        return qs
    israiska = Upper('oem_code')
    for zenklas in SIUKSLES:
        israiska = Replace(israiska, Value(zenklas), Value(''))
    return qs.annotate(_oem_norm=israiska)


def teksto_filtras(q):
    """Q dalių paieškai: pavadinimas ARBA aprašymas ARBA detalės numeris.

    Queryset'as prieš tai turi būti praleistas per `su_normalizuotu_oem`.
    """
    q = (q or '').strip()
    if not q:
        return Q()
    salyga = Q(title__icontains=q) | Q(description__icontains=q)
    kodas = normalizuok(q)
    if kodas:
        salyga |= Q(_oem_norm__contains=kodas)
    return salyga


def pagal_koda(qs, kodas):
    """Tik detalės numeris (?oem=, ?oem_code=) — be pavadinimo ir aprašymo.

    Pasvirasis brūkšnys lieka, tad „A / B" laukas atitinka ir A, ir B,
    bet ne suklijuotą „AB".
    """
    # Vien „/" (ar „ / ") atitiktų kiekvieną kelių kodų lauką — ne paieška.
    kodas = normalizuok(kodas).strip('/')
    if not kodas:
        return qs
    return su_normalizuotu_oem(qs).filter(_oem_norm__contains=kodas)


def ieskoti(qs, q):
    """Patogumo apvalkalas: anotacija + filtras vienu žingsniu."""
    q = (q or '').strip()
    if not q:
        return qs
    return su_normalizuotu_oem(qs).filter(teksto_filtras(q))
