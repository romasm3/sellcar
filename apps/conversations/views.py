from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.listings.image_validation import ImageValidationError, validate_image

from .models import Conversation, Message


# Greiti atsakymai — VIENAS sąrašas abiem ekranams (sąrašui ir pokalbiui).
# Rodomi tik ten, kur pokalbis turi skelbimą: pagalbos pokalbyje jie
# beprasmiai.
GREITI_ATSAKYMAI = [
    _('Ar dar parduodate?'),
    _('Kokia mažiausia kaina?'),
    _('Kada galima apžiūrėti?'),
    _('Ar keičiate?'),
]


def _greiti(conversation):
    return GREITI_ATSAKYMAI if (conversation and conversation.listing_id) else []


def _zinutes_json(messages, user):
    """Žinutės JSON'ui — tas pats pavidalas, kurį piešia šablonas."""
    from django.utils import timezone
    from apps.conversations.templatetags.pokalbiu_tags import dienos_zyma
    out = []
    for m in messages:
        vietine = timezone.localtime(m.created_at)
        out.append({
            'id': m.id,
            'mano': m.sender_id == user.id,
            'tekstas': m.content or '',
            'foto': m.image.url if m.image else '',
            'laikas': vietine.strftime('%H:%M'),
            'diena': str(dienos_zyma(m.created_at)),
            'perskaityta': bool(m.is_read),
        })
    return out


def _send_new_message_email(conversation, sender, recipient, content, new_message):
    """Siunčia 'new_message_notification' email per EmailScenario sistemą.

    ANTI-SPAM LOGIKA:
    Email siunčiamas TIK jei gavėjas neturi kitų neperskaitytų žinučių
    iš to paties siuntėjo šiame conversation'je. T.y. jei ši žinutė yra
    pirma "nauja partija" po to kai gavėjas perskaitė viską.
    """
    try:
        # Suskaičiuok neperskaitytas žinutes iš šio siuntėjo conversation'je,
        # EXCLUDINANT ką tik sukurtą žinutę.
        unread_from_sender = conversation.messages.filter(
            sender=sender,
            is_read=False,
        ).exclude(pk=new_message.pk).count()

        if unread_from_sender > 0:
            # Jau yra neskaitytų žinučių iš šio siuntėjo — nesiunčiam email.
            return

        # Į FONĄ: pranešimas apie žinutę — siuntėjas pašto serverio nelaukia.
        from apps.listings.emails.fone import (
            send_scenario_fone as send_scenario)

        # Sender vardas: first_name > email prefix (NE username)
        if sender.first_name:
            sender_name = sender.first_name
        elif sender.email:
            sender_name = sender.email.split('@')[0]
        else:
            sender_name = 'Someone'

        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        conversation_url = f'{site_url}/conversations/?conv={conversation.pk}'

        listing_title = ''
        listing_url = ''
        if conversation.listing:
            listing_title = str(conversation.listing)
            try:
                listing_url = f'{site_url}{conversation.listing.get_absolute_url()}'
            except Exception:
                listing_url = f'{site_url}/listings/{conversation.listing.pk}/'
        else:
            # Support pokalbis (be listing'o) — pažymim email'e
            listing_title = '🎧 AutoLeft Support'

        # Jei žinutė tik su foto (be teksto) — rodom emoji email'e
        display_content = content if content else '📎 [Photo attachment]'

        send_scenario(
            code='new_message_notification',
            to_email=recipient.email,
            to_user=recipient,
            context={
                'sender_name': sender_name,
                'message_content': display_content,
                'listing_title': listing_title,
                'listing_url': listing_url,
                'conversation_url': conversation_url,
                'site_url': site_url,
            },
        )
    except Exception as e:
        print(f"[new_message_notification] Failed: {e}")


@login_required
def conversation_list(request):
    """Vartotojo pokalbių sąrašas"""
    conversations = request.user.conversations.all().prefetch_related('participants', 'messages', 'listing__images')

    conv_data = []
    for conv in conversations:
        conv_data.append({
            'conversation': conv,
            'other_user': conv.get_other_participant(request.user),
            'last_message': conv.get_last_message(),
            'unread_count': conv.unread_count(request.user),
            'is_support': conv.listing is None,
        })

    # Pasirinktas pokalbis
    selected_conv = None
    selected_messages = []
    selected_other_user = None

    conv_pk = request.GET.get('conv')
    if conv_pk:
        try:
            selected_conv = request.user.conversations.get(pk=conv_pk)
            selected_conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
            selected_messages = selected_conv.messages.all()
            selected_other_user = selected_conv.get_other_participant(request.user)
        except:
            pass

    # Jei paspaustas SEND iš /conversations/?conv=XX (list view)
    if request.method == 'POST' and selected_conv:
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        if image:
            try:
                validate_image(image)
            except ImageValidationError as exc:
                django_messages.error(request, str(exc))
                return redirect(f'/conversations/?conv={selected_conv.pk}')
        if content or image:
            new_msg = Message.objects.create(
                conversation=selected_conv,
                sender=request.user,
                content=content,
                image=image,
            )
            selected_conv.save()

            other_user = selected_conv.get_other_participant(request.user)
            if other_user and getattr(other_user, 'profile', None) \
                    and getattr(other_user.profile, 'email_notifications', True):
                _send_new_message_email(selected_conv, request.user, other_user, content, new_msg)

            return redirect(f'/conversations/?conv={selected_conv.pk}')

    context = {
        'conv_data': conv_data,
        'selected_conv': selected_conv,
        'selected_messages': selected_messages,
        'selected_other_user': selected_other_user,
        'greiti_atsakymai': _greiti(selected_conv),
    }
    return render(request, 'conversations/conversation_list.html', context)


@login_required
def conversation_detail(request, pk):
    """Pokalbio detalės ir žinučių siuntimas"""
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)

    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        if image:
            try:
                validate_image(image)
            except ImageValidationError as exc:
                # NB: `messages` šitoje funkcijoje yra lokalus kintamasis
                # (conversation.messages.all()), tad naudojam alias'ą.
                django_messages.error(request, str(exc))
                return redirect(f'/conversations/?conv={conversation.pk}')
        if content or image:
            new_msg = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
                image=image,
            )
            conversation.save()

            other_user = conversation.get_other_participant(request.user)
            if other_user and getattr(other_user, 'profile', None) \
                    and getattr(other_user.profile, 'email_notifications', True):
                _send_new_message_email(conversation, request.user, other_user, content, new_msg)

            return redirect(f'/conversations/?conv={conversation.pk}')

    messages = conversation.messages.all()
    other_user = conversation.get_other_participant(request.user)

    context = {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
        'greiti_atsakymai': _greiti(conversation),
    }
    return render(request, 'conversations/conversation_detail.html', context)


@login_required
def start_conversation(request, listing_id):
    """Pradėk pokalbį dėl skelbimo"""
    from apps.listings.models import Listing

    listing = get_object_or_404(Listing, pk=listing_id)

    if listing.seller == request.user:
        return redirect('listing_detail', pk=listing_id)

    existing = Conversation.objects.filter(
        listing=listing,
        participants=request.user
    ).filter(
        participants=listing.seller
    ).first()

    if existing:
        return redirect(f'/conversations/?conv={existing.pk}')

    conversation = Conversation.objects.create(listing=listing)
    conversation.participants.add(request.user, listing.seller)

    return redirect(f'/conversations/?conv={conversation.pk}')


@login_required
def start_support_conversation(request):
    """Pradėk arba tęsk pokalbį su AutoLeft support'u"""
    SUPPORT_EMAIL = 'romasm3@gmail.com'

    support_user = User.objects.filter(email=SUPPORT_EMAIL).first()
    if not support_user:
        from django.contrib import messages as flash
        flash.error(request, 'Support sistema laikinai neprieinama.')
        return redirect('/')

    # Jei pats support'as bando rašyti sau — redirect į inbox
    if request.user == support_user:
        return redirect('/conversations/')

    # Ieškom egzistuojančio support pokalbio (be listing, su abiem dalyviais)
    existing = Conversation.objects.filter(
        listing__isnull=True,
        participants=request.user
    ).filter(
        participants=support_user
    ).first()

    if existing:
        return redirect(f'/conversations/?conv={existing.pk}')

    # Sukuriam naują support conversation (BE listing'o)
    conversation = Conversation.objects.create(listing=None)
    conversation.participants.add(request.user, support_user)

    return redirect(f'/conversations/?conv={conversation.pk}')


@login_required
def check_new_messages(request):
    """Polling BE PERKROVIMO.

    Grąžina naujų žinučių sąrašą po nurodyto id — JS jas prideda į
    apačią. Anksčiau čia buvo tik skaičius, o šablonas darydavo
    `location.reload()`: dingdavo rašomas tekstas ir nušokdavo slinkimas.

        /conversations/check-new/?conv=12&po=345

    `conv` ir `po` neprivalomi — be jų grąžinamas tik bendras skaitiklis
    (antraštės vokui).
    """
    from django.http import JsonResponse

    unread_count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()

    atsakymas = {'unread_count': unread_count, 'zinutes': []}

    conv_pk = request.GET.get('conv')
    po = request.GET.get('po')
    if conv_pk:
        conversation = Conversation.objects.filter(
            pk=conv_pk, participants=request.user).first()
        if conversation:
            naujos = conversation.messages.all()
            if po and str(po).isdigit():
                naujos = naujos.filter(id__gt=int(po))
            naujos = list(naujos.order_by('created_at')[:50])
            atsakymas['zinutes'] = _zinutes_json(naujos, request.user)
            # Pokalbis atidarytas — svetimos žinutės iškart perskaitytos,
            # kitaip vokas antraštėje rodytų tai, ką žmogus jau mato.
            svetimos = [m.id for m in naujos if m.sender_id != request.user.id]
            if svetimos:
                Message.objects.filter(id__in=svetimos).update(is_read=True)
                atsakymas['unread_count'] = Message.objects.filter(
                    conversation__participants=request.user,
                    is_read=False).exclude(sender=request.user).count()

    return JsonResponse(atsakymas)


@login_required
def translate_conversation(request, pk):
    """AJAX endpoint — verčia visas žinutes į user'io aktyvią kalbą.

    URL: GET /conversations/<pk>/translate/
    Returns: JSON {success, target_lang, messages: [{id, original, translated, detected}]}
    """
    from django.http import JsonResponse
    from django.utils import translation as django_translation

    conversation = get_object_or_404(
        Conversation, pk=pk, participants=request.user,
    )

    # Target kalba — iš user'io aktyvios sesijos kalbos
    # (kuri ateina iš header'io language switcher'io)
    target_lang = django_translation.get_language() or 'en'
    target_lang = target_lang.split('-')[0]  # 'en-us' → 'en'

    # Optional: galima override per ?lang=de URL param
    requested_lang = request.GET.get('lang')
    if requested_lang:
        target_lang = requested_lang.lower()[:2]

    messages_qs = conversation.messages.exclude(content='').order_by('created_at')

    # Klaida turi būti MATOMA. Anksčiau servisas tyliai grąžindavo
    # originalą, o sąsaja rodydavo „išversta" — žmogus matė savo kalbą ir
    # manė, kad vertimas toks. Dabar servisas praneša, kad nepavyko, ir
    # mygtukas rodo „Nepavyko išversti".
    try:
        # Importas ČIA, kartu su kvietimu: jei google-cloud-translate
        # neįdiegtas, tai irgi „nepavyko išversti", o ne 500 su klaidos
        # puslapiu vietoj JSON.
        from .translate_service import translate_messages_for_user
        translated = translate_messages_for_user(messages_qs, target_lang)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=502)

    if translated is None:
        return JsonResponse(
            {'success': False, 'error': 'translate-unavailable'}, status=502)

    return JsonResponse({
        'success': True,
        'target_lang': target_lang,
        'messages': translated,
    })