# -*- coding: utf-8 -*-
"""
SKAITINIŲ LAUKŲ RIBOS — KAD PER DIDELĖ REIKŠMĖ DUOTŲ KLAIDĄ, O NE 500.

Kas buvo. `engine_capacity` yra DecimalField(max_digits=5,
decimal_places=1), tad daugiausia telpa 9999,9. Laukas sunkvežimių
formoje prašo LITRŲ („pvz., 12,0"), o žmogus įrašo kubinius
centimetrus — 10837. Postgres tokio skaičiaus nepriima
(NumericValueOutOfRange), Django to negaudo, ir vietoj žinutės žmogus
gauna 500, o kartu — pakibusį juodraštį su jau įkeltomis nuotraukomis
(žr. apps/listings/management/commands/valyti_juodrascius.py).

Modelio validatoriai čia nepadeda: vaizdai objektą užpildo ir iškart
kviečia `save()`, o `full_clean()` — ne. Todėl ribas tikrinam patys,
PRIEŠ įrašymą.

Ribos imamos iš paties modelio, ne iš rankomis rašyto sąrašo:

  · yra MinValue/MaxValue validatorių — imam juos;
  · DecimalField — max_digits ir decimal_places (5,1 → ±9999,9);
  · IntegerField — Postgres int4 riba (±2 147 483 647).

Tad naujas laukas apsaugotas savaime, nieko čia nepridėjus.

Naudojimas vaizde, ten kur renkamos klaidos:

    from .skaiciai import patikra
    for laukas, tekstas in patikra(target).items():
        errors.append(tekstas)        # arba errors[laukas] = tekstas
"""
from decimal import Decimal, InvalidOperation

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from . import units

# PostgreSQL integer (int4) — už jo ribų krenta pati DB.
INT_MIN = -2147483648
INT_MAX = 2147483647
BIGINT_MIN = -9223372036854775808
BIGINT_MAX = 9223372036854775807


def _validatoriu_ribos(laukas):
    apacia = virsus = None
    for v in getattr(laukas, 'validators', ()):
        if isinstance(v, MinValueValidator):
            apacia = v.limit_value
        elif isinstance(v, MaxValueValidator):
            virsus = v.limit_value
    return apacia, virsus


def ribos(laukas):
    """(mažiausia, didžiausia) reikšmė laukui arba (None, None).

    Validatorius laimi, bet TIK tą pusę, kurią nurodo: laukas su vienu
    `MinValueValidator(0)` viršaus vis tiek turi — stulpelio talpą.
    """
    apacia, virsus = _validatoriu_ribos(laukas)
    if apacia is not None and virsus is not None:
        return apacia, virsus

    talpos_apacia, talpos_virsus = _talpa(laukas)
    return (apacia if apacia is not None else talpos_apacia,
            virsus if virsus is not None else talpos_virsus)


def _talpa(laukas):
    """Ką fiziškai priima stulpelis."""
    if isinstance(laukas, models.DecimalField):
        skaitmenys = laukas.max_digits or 0
        po_kablelio = laukas.decimal_places or 0
        if not skaitmenys:
            return None, None
        # 5,1 → 999,9 + 0,1 trūkumas: didžiausia yra 9999,9
        didziausia = (Decimal(10) ** (skaitmenys - po_kablelio)
                      - Decimal(10) ** (-po_kablelio))
        return -didziausia, didziausia

    if isinstance(laukas, models.BigIntegerField):
        return BIGINT_MIN, BIGINT_MAX
    if isinstance(laukas, models.PositiveIntegerField):
        return 0, INT_MAX
    if isinstance(laukas, models.IntegerField):
        return INT_MIN, INT_MAX
    return None, None


def _skaicius(reiksme):
    if reiksme is None or reiksme == '':
        return None
    try:
        return Decimal(str(reiksme))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _vardas(laukas):
    return str(getattr(laukas, 'verbose_name', '') or laukas.name)


def _tekstas(laukas, apacia, virsus, per_didele):
    vardas = _vardas(laukas)
    if per_didele:
        return _('%(laukas)s: reikšmė per didelė (daugiausia %(riba)s)') % {
            'laukas': vardas, 'riba': _grazi(virsus)}
    return _('%(laukas)s: reikšmė per maža (mažiausia %(riba)s)') % {
        'laukas': vardas, 'riba': _grazi(apacia)}


def _grazi(riba):
    """Riba žmogui: 9999.9 → „9999,9", 2147483647 → „2147483647"."""
    if riba is None:
        return ''
    tekstas = format(Decimal(str(riba)).normalize(), 'f')
    return tekstas.replace('.', ',')


def patikra(objektas, laukai=None):
    """{lauko vardas: klaidos tekstas} toms reikšmėms, kurios netelpa.

    Tikrinam TIK užpildytus skaitinius laukus. Tušti (None) praleidžiami
    — ar laukas privalomas, sprendžia pati forma.
    """
    klaidos = {}
    for laukas in objektas._meta.concrete_fields:
        if not isinstance(laukas, (models.IntegerField, models.DecimalField,
                                   models.FloatField)):
            continue
        if isinstance(laukas, models.AutoField) or laukas.primary_key:
            continue
        if laukai and laukas.name not in laukai:
            continue
        reiksme = _skaicius(getattr(objektas, laukas.attname, None))
        if reiksme is None:
            continue
        apacia, virsus = ribos(laukas)
        if virsus is not None and reiksme > Decimal(str(virsus)):
            klaidos[laukas.name] = _tekstas(laukas, apacia, virsus, True)
        elif apacia is not None and reiksme < Decimal(str(apacia)):
            klaidos[laukas.name] = _tekstas(laukas, apacia, virsus, False)
    return klaidos


def netelpa(objektas, laukai=None):
    """Klaidų tekstų sąrašas — vaizdams, kurie kaupia `errors` sąrašą."""
    return list(patikra(objektas, laukai).values())


def patikra_posto(modelis, post, laukai=None):
    """Tas pats, tik iš POST — kai vaizdas tikrina PRIEŠ objekto surinkimą.

    Tikrinam kiekvieną POST raktą, kuris sutampa su modelio skaitiniu
    lauku. Formos laukų vardai su modelio laukais sutampa (kontaktų ir
    kiti blokai vardus ima iš modelio), tad naujas laukas apsaugotas
    savaime.

    Kablelis paverčiamas tašku: telefone lietuviška klaviatūra siūlo
    „12,0", o `Decimal('12,0')` neatpažįsta ir reikšmė tyliai dingtų.
    """
    klaidos = {}
    for laukas in modelis._meta.concrete_fields:
        if not isinstance(laukas, (models.IntegerField, models.DecimalField,
                                   models.FloatField)):
            continue
        if laukas.primary_key or (laukai and laukas.name not in laukai):
            continue
        if laukas.name not in post:
            continue
        # Ne visi kvietėjai paduoda žalią POST'ą: listing_helpers
        # .parse_common_listing_fields `year` ir `price` jau paverčia
        # skaičiais (_int_or_none / _float_or_none), o tada .strip()
        # nebeturi į ką atsiremti — buvo 500 vos atsiuntus galiojantį
        # skaičių (/create/car-for-parts/ su price=33).
        reiksme_is_posto = post.get(laukas.name)
        tekstas = ('' if reiksme_is_posto is None
                   else str(reiksme_is_posto).strip())
        if not tekstas:
            continue

        # NORMALIZUOJAM PIRMA, TIKRINAM PASKUI. Reikšmė gali atkeliauti
        # ne saugojimo vienetu — kurio, sako `<laukas>_unit`
        # (apps/listings/units.py). Su pasirinktais cm³ tas pats 10837
        # yra 10,8 l ir turi būti priimtas.
        vienetas = units.vienetas_is_posto(post, laukas.name)
        reiksme = units.i_saugojima(laukas.name, tekstas, vienetas)
        if reiksme is None:
            continue                  # ne skaičius — atskira formos bėda

        # Dalykinė riba (variklis iki 30 l) — žinutėje įvardijam vienetą
        dalykine = units.per_didele(laukas.name, reiksme, vienetas)
        if dalykine:
            klaidos[laukas.name] = dalykine
            continue

        apacia, virsus = ribos(laukas)
        if virsus is not None and reiksme > Decimal(str(virsus)):
            klaidos[laukas.name] = _tekstas(laukas, apacia, virsus, True)
        elif apacia is not None and reiksme < Decimal(str(apacia)):
            klaidos[laukas.name] = _tekstas(laukas, apacia, virsus, False)
    return klaidos
