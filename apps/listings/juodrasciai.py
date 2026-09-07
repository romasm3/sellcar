# -*- coding: utf-8 -*-
"""
JUODRAŠČIŲ SESIJA — KAD NUOTRAUKOS NEPRILIPTŲ PRIE KITO SKELBIMO.

Kas buvo. Įkėlimo formos juodraštį laiko sesijoje
(`active_trucks_draft_id` ir panašūs), o nuotraukos AJAX'u keliauja
tiesiai į tą juodraštį. Jei pateikimas nulūžta (pvz. per didelis
variklio tūris — 500), sesijos raktas lieka. Žmogus atsidaro formą iš
naujo, įkelia kitas nuotraukas — ir jos gula į TĄ PATĮ juodraštį. Taip
skelbimas #754 gavo 40 nuotraukų vietoj 20: renault-t460_*.jpg iš
pirmo bandymo ir rt460_*.jpg iš antro.

Taisyklė dabar viena: ŠVIEŽIAS FORMOS ATIDARYMAS PRADEDA ŠVARIAI.

  · tuščias senas juodraštis ištrinamas;
  · turintis turinio — atrišamas nuo sesijos ir lieka „Mano
    skelbimuose", o žmogui parodoma nuoroda jį tęsti (?tesk=<id>);
  · tęsiama tik tada, kai to paprašoma aiškiai — adresu su ?tesk=.

Pateikimas (POST) juodraščio neatriša: perkrovus formą su klaidomis
įvesti duomenys ir įkeltos nuotraukos privalo likti vietoje.

Pakibusius juodraščius, kurių niekas nebetęsia, šluoja
`python manage.py valyti_juodrascius` (cron, žr. komandos aprašą).
"""
import logging

logger = logging.getLogger(__name__)

# Adreso parametras „tęsiu tą patį juodraštį"
TESIMO_PARAMETRAS = 'tesk'


def tesiamas_id(request):
    """?tesk=<id> — žmogus aiškiai paprašė tęsti seną juodraštį."""
    try:
        return int(request.GET.get(TESIMO_PARAMETRAS) or 0) or None
    except (TypeError, ValueError):
        return None


def sviezias_atidarymas(request):
    """Ar tai naujos formos atidarymas (o ne pateikimas ar tęsimas).

    POST'as niekada nėra šviežias atidarymas: perkraunant formą su
    klaidomis juodraštis privalo išlikti.
    """
    if request.method != 'GET':
        return False
    if tesiamas_id(request):
        return False
    # Redagavimas eina savo keliu — jis su juodraščiais nesusijęs
    if request.GET.get('edit'):
        return False
    return True


def tuscias(juodrastis):
    """Ar juodraštyje nėra nieko, ko būtų gaila.

    Nuotrauka yra turinys: dėl jos juodraštis lieka, kad įkeltas darbas
    nedingtų.
    """
    if juodrastis is None:
        return True
    turi_nuotrauku = False
    try:
        turi_nuotrauku = juodrastis.images.exists()
    except Exception:                                   # noqa: BLE001
        pass
    return not (
        turi_nuotrauku
        or (juodrastis.description or '').strip()
        or (juodrastis.price or 0)
        or getattr(juodrastis, 'brand_id', None)
        or getattr(juodrastis, 'truck_brand_id', None)
        or (getattr(juodrastis, 'truck_model_text', '') or '').strip()
        or (getattr(juodrastis, 'title', '') or '').strip()
    )


def atrisk(request, sesijos_raktas, juodrastis=None):
    """Atriša juodraštį nuo sesijos. Tuščią — ištrina.

    Grąžina juodraštį, jei jis liko duomenų bazėje (turi turinio) —
    tada vaizdas gali pasiūlyti jį tęsti.
    """
    request.session[sesijos_raktas] = None
    request.session.modified = True
    if juodrastis is None:
        return None
    if tuscias(juodrastis):
        logger.info('[juodrasciai] trinam tuščią #%s', juodrastis.pk)
        try:
            juodrastis.delete()
        except Exception:                               # noqa: BLE001
            logger.exception('[juodrasciai] nepavyko ištrinti #%s', juodrastis.pk)
        return None
    logger.info('[juodrasciai] atrišam #%s (turi turinio)', juodrastis.pk)
    return juodrastis


def pradek_svariai(request, sesijos_raktas, juodrastis):
    """Šviežiam atidarymui — atriša ir grąžina (naudotinas, likęs).

    naudotinas — su kuo dirbti toliau (šviežiai atidarius: nieko);
    likęs      — senas juodraštis su turiniu, kurį galima pasiūlyti tęsti.
    """
    if not sviezias_atidarymas(request):
        return juodrastis, None
    if juodrastis is None:
        return None, None
    return None, atrisk(request, sesijos_raktas, juodrastis)


def pasiulyk_testi(request, juodrastis):
    """Žinutė su nuoroda tęsti atrištą juodraštį.

    Nieko neprarandam ir nieko neprimetam: nuotraukos ir įvesti laukai
    lieka, o žmogus pats nusprendžia, ar tęsia seną, ar pildo naują.
    """
    from django.contrib import messages
    from django.utils.html import format_html
    from django.utils.translation import gettext as _

    try:
        adresas = '%s?%s=%s' % (request.path, TESIMO_PARAMETRAS, juodrastis.pk)
        messages.info(request, format_html(
            '{} <a href="{}" class="underline font-semibold">{}</a>',
            _('Turite nebaigtą skelbimą — jis išsaugotas.'),
            adresas,
            _('Tęsti nebaigtą'),
        ))
    except Exception:                                   # noqa: BLE001
        logger.exception('[juodrasciai] nepavyko pasiūlyti tęsti')
