# -*- coding: utf-8 -*-
"""
ADMINISTRACIJOS POKALBIŲ PERŽIŪRA — ginčams, grąžinimams, sukčiavimui.

    /administracija/pokalbiai/        — gijų antraštės (dalyviai, skelbimas,
                                        datos, žinučių skaičius), BE turinio
    /administracija/pokalbiai/<id>/   — GET: antraštė ir priežasties forma,
                                        turinio NĖRA; POST su priežastimi →
                                        įrašas PokalbioPerziura ir turinys
    /administracija/zurnalas/         — visos peržiūros, tik skaitymas

Teisė — Profile.gali_matyti_pokalbius (ne is_superuser). Be jos — 403.

TIK SKAITYMAS: čia nėra jokios formos žinutei siųsti, keisti ar trinti, nei
prisijungimo kitu vardu. Rodomas ORIGINALAS (Message.content); jei yra
vertimas — tik šalia, kaip pagalba. Turinys atsiunčiamas tik POST atsakyme:
perkrovus ar atsidarius nuorodą jo nebėra, kiekvienas žvilgsnis — naujas
įrašas su priežastimi.
"""
from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .models import Conversation, PokalbioPerziura

PUSLAPYJE = 50


def gali_matyti(user):
    profilis = getattr(user, 'profile', None)
    return bool(user.is_authenticated and user.is_active and profilis is not None
                and profilis.gali_matyti_pokalbius)


def _tik_su_teise(view):
    @login_required
    def apvalkalas(request, *args, **kwargs):
        if not gali_matyti(request.user):
            raise PermissionDenied(_('Neturite teisės peržiūrėti pokalbių.'))
        return view(request, *args, **kwargs)
    apvalkalas.__name__ = view.__name__
    apvalkalas.__doc__ = view.__doc__
    return apvalkalas


def _data(reiksme, pabaiga=False):
    try:
        d = datetime.strptime((reiksme or '').strip(), '%Y-%m-%d').date()
    except ValueError:
        return None
    return timezone.make_aware(datetime.combine(d, time.max if pabaiga else time.min))


def _be_puslapio(q):
    kopija = q.copy()
    kopija.pop('p', None)
    return kopija.urlencode()


def _ip(request):
    ip = (request.META.get('HTTP_X_FORWARDED_FOR') or '').split(',')[0].strip()
    return ip or request.META.get('REMOTE_ADDR') or None


@_tik_su_teise
@require_http_methods(['GET'])
def sarasas(request):
    """Gijų antraštės su paieška. Žinučių turinio — jokio."""
    q = request.GET
    qs = (Conversation.objects
          .annotate(zinuciu=Count('messages', distinct=True),
                    paskutine=Max('messages__created_at'),
                    perziuru=Count('perziuros', distinct=True))
          .select_related('listing').prefetch_related('participants')
          .order_by('-updated_at'))

    vartotojas = (q.get('vartotojas') or '').strip()
    if vartotojas:
        salyga = (Q(participants__email__icontains=vartotojas)
                  | Q(participants__username__icontains=vartotojas)
                  | Q(participants__first_name__icontains=vartotojas)
                  | Q(participants__last_name__icontains=vartotojas))
        if vartotojas.isdigit():
            salyga |= Q(participants__pk=int(vartotojas))
        qs = qs.filter(salyga)
    skelbimas = (q.get('skelbimas') or '').strip()
    if skelbimas:
        qs = qs.filter(Q(listing__pk=int(skelbimas)) if skelbimas.isdigit()
                       else Q(listing__title__icontains=skelbimas))
    nr = (q.get('nr') or '').strip()
    if nr.isdigit():
        qs = qs.filter(pk=int(nr))
    nuo, iki = _data(q.get('nuo')), _data(q.get('iki'), pabaiga=True)
    if nuo:
        qs = qs.filter(updated_at__gte=nuo)
    if iki:
        qs = qs.filter(created_at__lte=iki)

    puslapis = Paginator(qs.distinct(), PUSLAPYJE).get_page(q.get('p'))
    return render(request, 'conversations/administracija/sarasas.html', {
        'puslapis': puslapis, 'q': q,
        'filtrai': _be_puslapio(q),
    })


@_tik_su_teise
@require_http_methods(['GET', 'POST'])
def gija(request, pk):
    """GET — tik antraštė ir priežasties forma. POST su priežastimi —
    įrašas žurnale ir turinys (originalas)."""
    pokalbis = get_object_or_404(
        Conversation.objects.select_related('listing').prefetch_related('participants'), pk=pk)
    priezastys = dict(PokalbioPerziura.PRIEZASTYS)
    klaida = None
    zinutes = None
    perziura = None

    if request.method == 'POST':
        priezastis = (request.POST.get('priezastis') or '').strip()
        paaiskinimas = (request.POST.get('paaiskinimas') or '').strip()[:2000]
        if priezastis not in priezastys:
            klaida = _('Pasirinkite peržiūros priežastį — be jos pokalbis neatidaromas.')
        elif priezastis == PokalbioPerziura.KITA and not paaiskinimas:
            klaida = _('Pasirinkus „Kita", būtina parašyti paaiškinimą.')
        else:
            perziura = PokalbioPerziura.objects.create(
                perziurejo=request.user, perziurejo_el_pastas=request.user.email or request.user.username,
                pokalbis=pokalbis, pokalbio_nr=pokalbis.pk,
                priezastis=priezastis, paaiskinimas=paaiskinimas, ip=_ip(request))
            perziura.dalyviai.set(pokalbis.participants.all())
            zinutes = list(pokalbis.messages.select_related('sender')
                           .prefetch_related('translations').order_by('created_at', 'pk'))

    atsakymas = render(request, 'conversations/administracija/gija.html', {
        'pokalbis': pokalbis,
        'zinuciu': pokalbis.messages.count(),
        'priezastys': PokalbioPerziura.PRIEZASTYS,
        'klaida': klaida,
        'zinutes': zinutes,
        'perziura': perziura,
        'ankstesnes': PokalbioPerziura.objects.filter(pokalbio_nr=pokalbis.pk)[:20],
        'post': request.POST if request.method == 'POST' else {},
    }, status=400 if klaida else 200)
    atsakymas['Cache-Control'] = 'no-store'           # turinys — ne talpyklai
    return atsakymas


@login_required
@require_http_methods(['GET'])
def zurnalas(request):
    """Visos peržiūros. Tik skaitymas — trynimo ar keitimo kelio nėra.
    Mato turintys pokalbių teisę ir superadministratorius (pagalbininko
    priežiūrai)."""
    if not (gali_matyti(request.user) or request.user.is_superuser):
        raise PermissionDenied(_('Neturite teisės matyti žurnalo.'))
    qs = PokalbioPerziura.objects.prefetch_related('dalyviai')
    kas = (request.GET.get('kas') or '').strip()
    if kas:
        qs = qs.filter(perziurejo_el_pastas__icontains=kas)
    nr = (request.GET.get('nr') or '').strip()
    if nr.isdigit():
        qs = qs.filter(pokalbio_nr=int(nr))
    puslapis = Paginator(qs, PUSLAPYJE).get_page(request.GET.get('p'))
    return render(request, 'conversations/administracija/zurnalas.html', {
        'puslapis': puslapis, 'q': request.GET, 'filtrai': _be_puslapio(request.GET),
    })
