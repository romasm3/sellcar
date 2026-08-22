"""Išsaugotų paieškų parametrų pagalbinės funkcijos.

Vieno lauko reikšmė gali būti tekstas arba SĄRAŠAS (kelios markės,
keli kuro tipai — formos leidžia rinktis po kelis). Django filtrui
sąrašo tiesiai paduoti negalima: `filter(brand_id=['8', '9'])` meta
`Field 'id' expected a number`. Todėl visos vietos, kurios naudoja
query_params (puslapis, skaitiklis antraštėje, el. laiškų komandos),
filtruoja per šias funkcijas.
"""


def sarasas(reiksme):
    """Reikšmė -> sąrašas (tuščios reikšmės išmetamos)."""
    if reiksme in (None, '', []):
        return []
    if isinstance(reiksme, (list, tuple)):
        return [str(v) for v in reiksme if v not in (None, '')]
    return [str(reiksme)]


def viena(reiksme):
    """Reikšmė -> viena reikšmė (jei sąrašas — pirmoji)."""
    s = sarasas(reiksme)
    return s[0] if s else None


def filtruoti_id(qs, laukas, reiksme, tik_skaiciai=True):
    """qs.filter(laukas=…) arba …__in=[…], atsparus sąrašams ir šiukšlėms."""
    reiksmes = sarasas(reiksme)
    if tik_skaiciai:
        reiksmes = [v for v in reiksmes if str(v).isdigit()]
    if len(reiksmes) == 1:
        return qs.filter(**{laukas: reiksmes[0]})
    if reiksmes:
        return qs.filter(**{laukas + '__in': reiksmes})
    return qs


def filtruoti_reziu(qs, filtras, reiksme):
    """Skaitinis rėžis (price__gte, year__lte…) — praleidžia netinkamas."""
    v = viena(reiksme)
    if v in (None, ''):
        return qs
    try:
        return qs.filter(**{filtras: v})
    except (ValueError, TypeError):
        return qs
