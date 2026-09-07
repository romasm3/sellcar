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
