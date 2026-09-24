# -*- coding: utf-8 -*-
"""
SKELBIMO KONTAKTAI — VIENA VIETA VISOMS FORMOMS.

Kontaktų blokas šablonuose jau seniai vienas
(`templates/listings/partials/contact_block.html`), o jo įrašymas buvo
išbarstytas po dvidešimt vaizdų. Todėl telefoną įrašydavo visi, o
el. paštą — niekas: laukas formoje buvo, bet POST reikšmė niekur
nenugulėdavo ir po perkrovimo grįždavo paskyros paštas.

Naudojimas vaizde, ten pat, kur įrašomas telefonas:

    from .kontaktai import issaugok_pasta
    issaugok_pasta(target, request)

WheelListing turi savo `contact_email` stulpelį ir savo POST vardą, tad
jam paduodam `laukas='contact_email'`.

TELEFONAS — tas pats. Iki 2026-09-15 jis gulėjo TIK paskyroje
(`profile.phone_number`), tad buvo vienas visiems žmogaus skelbimams:
pakeitus numerį viename, jis tyliai pasikeisdavo visuose kituose.
Dabar kiekvienas skelbimas turi savo `contact_phone`, o paskyros
numeris naudojamas tik kaip PRADINĖ reikšmė naujam skelbimui.
"""


def pastas_is_posto(request, laukas='email'):
    """POST reikšmė be tarpų. Trūkstamas laukas — tuščia eilutė."""
    return (request.POST.get(laukas, '') or '').strip()


def issaugok_pasta(listing, request, laukas='email'):
    """Įrašo skelbimo kontaktinį paštą iš POST.

    Tuščias laukas NIEKO netrina: dalis formų kontaktų bloko nerodo
    (redagavimo žingsniai, greitieji išsaugojimai), o tyliai išvalytas
    paštas atrodytų kaip dingęs kontaktas.

    Įrašo tik į objektą — `save()` lieka vaizdo reikalas.
    """
    reiksme = pastas_is_posto(request, laukas)
    if reiksme:
        listing.contact_email = reiksme
    return getattr(listing, 'contact_email', '')


def pasto_reiksme(listing, user=None):
    """Ką rodyti formos lauke.

    Skelbimo paštas pirmas; paskyros — tik kai skelbimo laukas tuščias
    (naujas skelbimas). Anksčiau būdavo atvirkščiai, tad įrašyta
    reikšmė kaskart pradingdavo.
    """
    esamas = (getattr(listing, 'contact_email', '') or '').strip() if listing else ''
    if esamas:
        return esamas
    if user is not None and getattr(user, 'is_authenticated', False):
        return user.email or ''
    return ''


# ═══════════════════════════════════════════════════════════════════
# TELEFONAS — tiksliai tas pats, kaip paštas
# ═══════════════════════════════════════════════════════════════════

def telefonas_is_posto(request, laukas='phone'):
    """POST reikšmė be tarpų galuose. Trūkstamas laukas — tuščia eilutė."""
    return (request.POST.get(laukas, '') or '').strip()


def issaugok_telefona(listing, request, laukas='phone'):
    """Įrašo skelbimo kontaktinį telefoną iš POST.

    Tuščias laukas NIEKO netrina — lygiai kaip su paštu: dalis formų
    kontaktų bloko nerodo (redagavimo žingsniai, greitieji išsaugojimai),
    o tyliai išvalytas numeris atrodytų kaip dingęs kontaktas.

    PASKYROS NELIEČIA. Anksčiau kiekvienas vaizdas rašydavo numerį į
    profilio lauką, ir tai buvo visos bėdos šaltinis: vieno skelbimo
    redagavimas perrašydavo kontaktą visuose.

    Įrašo tik į objektą — `save()` lieka vaizdo reikalas.
    """
    if listing is None:
        return ''
    reiksme = telefonas_is_posto(request, laukas)
    if reiksme:
        listing.contact_phone = reiksme
    return getattr(listing, 'contact_phone', '')


def telefono_reiksme(listing, user=None):
    """Ką ĮRAŠYTI į formos lauką.

    TIK skelbimo numeris. Paskyros numerio čia NEBĖRA sąmoningai: kai jis
    būdavo įrašomas į `value`, žmogui nieko nepakeitus jis nugulėdavo
    skelbime kaip to skelbimo kontaktas. Taip paskyros savininko asmeninis
    numeris atsidūrė svetimų pardavėjų skelbimuose (#827).

    Paskyros numeris dabar tik SIŪLOMAS — kaip placeholder, žr.
    `siulomas_telefonas()` ir contact_block.html parametrą
    `siulomas_telefonas`. Placeholder į POST nepatenka.

    `user` paliktas parašo suderinamumui ir sąmoningai nenaudojamas.
    """
    return (getattr(listing, 'contact_phone', '') or '').strip() if listing else ''


def siulomas_telefonas(user=None):
    """Paskyros numeris — tik kaip užuomina tuščiam formos laukui.

    Rodomas placeholder'iu, todėl matomas, bet neišsisaugo, kol žmogus
    jo pats neįveda.
    """
    profilis = getattr(user, 'profile', None) if user is not None else None
    return (getattr(profilis, 'phone_number', '') or '').strip()
