import os
import unicodedata

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .constants import can_create_listing, can_create_free_listing, FREE_LISTING_DAYS
from .equipment_registry import ELEC_EQUIPMENT_DEFINITION
from .image_validation import split_valid_images
from .models import (
    Listing, ListingImage, VehicleType, Equipment, ListingEquipment,
)
from .views import (
    _int_or_none,
    _float_or_none,
    get_coordinates_for_location,
    _send_listing_published_email,
    _send_saved_listing_updated_emails,
    _send_saved_listing_price_drop_emails,
    COUNTRY_FLAGS,
)
from apps.listings import brands as brand_source


# ═══════════════════════════════════════════════════════════
# VIDEO, AUDIO, NAVIGACIJOS (vehicle_type slug='electronics')
#
# Plokščia kategorija (loading-equipment / services patternas):
# subkategorijų nėra, subcategory lieka NULL, pikeris veda tiesiai čia.
#
# Etalono ypatybė: „Galingumas W" privalomas TIK kai tipas yra
# „Garsiakalbis" (patikrinta autogide — daugiau laukų nuo tipo
# nepriklauso). Tikrinam ir kliente (Alpine), ir serveryje.
#
# Pavadinimo lauko formoje nėra — generuojam iš gamintojo + modelio + tipo.
# ═══════════════════════════════════════════════════════════

ELEC_VT_SLUG = 'electronics'

# Tipas, kuriam etalonas reikalauja galingumo
POWER_REQUIRED_TYPES = ('speaker',)

ELEC_CHANNELS = list(range(1, 7))       # etalone 1..6


def _norm(value):
    value = unicodedata.normalize('NFKD', value.casefold())
    return ''.join(c for c in value if not unicodedata.combining(c))


# Markės — iš bendros Brand lentelės (šeima „electronics"). Anksčiau čia
# buvo skaitomas atskiras .txt failas; failas lieka repozitorijoje
# kaip seed'as, bet formos ir filtrai ima iš DB.
def _brand_names():
    from apps.listings import brands as brand_source
    return list(brand_source.brands_qs('electronics').values_list('name', flat=True))


class _BrandList:
    """Tingus sąrašas — DB neliečiama importo metu."""

    def _names(self):
        return _brand_names()

    def __iter__(self):
        return iter(self._names())

    def __len__(self):
        return len(self._names())

    def __contains__(self, item):
        return item in self._names()

    def __getitem__(self, idx):
        return self._names()[idx]


ELEC_BRANDS = _BrandList()


def get_elec_equipment():
    """16 ypatumų, sugrupuotų šablonui (idempotentiškai kuriamos)."""
    grouped = []
    for cat_key, cat_label, names in ELEC_EQUIPMENT_DEFINITION:
        items = [Equipment.objects.get_or_create(category=cat_key, name=n)[0]
                 for n in names]
        grouped.append({'key': cat_key, 'label': cat_label, 'items': items})
    return grouped


def _country_choices():
    # Šalys — vienas sąrašas visai svetainei (apps/listings/salys.py)
    from apps.listings import salys
    return salys.plokscias()


@login_required
def electronics_listing_create(request):
    """URL: /create/electronics/?new=1  |  ?edit=<pk>"""
    vt = VehicleType.objects.filter(slug=ELEC_VT_SLUG).first()
    if not vt:
        messages.error(request, _('Video, audio, navigacijų kategorija nesukonfigūruota.'))
        return redirect('listing_list')

    edit_pk = _int_or_none(request.GET.get('edit')) or _int_or_none(request.POST.get('edit'))
    is_edit_mode = bool(edit_pk)
    listing = None

    if is_edit_mode:
        listing = get_object_or_404(Listing, pk=edit_pk, seller=request.user)
        if not listing.vehicle_type or listing.vehicle_type.slug != ELEC_VT_SLUG:
            messages.error(request, _('Ši forma skirta tik video, audio, navigacijų skelbimams.'))
            return redirect('listing_edit_hub', pk=edit_pk)
    else:
        can_create, active_count, limit = can_create_listing(request.user)
        if not can_create:
            messages.error(
                request,
                f'You have reached your active listings limit ({active_count}/{limit}). '
                f'Upgrade your account to create more listings.',
            )
            return redirect('listing_upgrade')

    if request.method == 'POST':
        target = listing if is_edit_mode else Listing(
            seller=request.user, vehicle_type=vt, status='draft')
        old_price = float(target.price) if (is_edit_mode and target.price) else 0
        errors = []

        condition = request.POST.get('condition', '')
        if not condition:
            errors.append(_('Būklė yra privaloma'))
        else:
            target.condition = condition

        elec_type = request.POST.get('elec_type', '')
        if not elec_type:
            errors.append(_('Tipas yra privalomas'))
        target.elec_type = elec_type

        brand = brand_source.posted_brand(request, 'elec_brand_text', 'electronics')
        if not brand:
            errors.append(_('Gamintojas yra privalomas'))
        target.elec_brand_text = brand[:80]

        target.constr_model_text = (request.POST.get('constr_model_text', '') or '').strip()[:20]

        # Galingumas privalomas tik garsiakalbiams (etalonas)
        power_w = _int_or_none(request.POST.get('power_w'))
        if elec_type in POWER_REQUIRED_TYPES and not power_w:
            errors.append(_('Galingumas W yra privalomas garsiakalbiams'))
        target.power_w = power_w

        target.elec_channels = _int_or_none(request.POST.get('elec_channels'))
        target.color = request.POST.get('color', '') or ''

        price = _float_or_none(request.POST.get('price'))
        if price is None or price <= 0:
            errors.append(_('Kaina yra privaloma'))
        else:
            target.price = price
        target.open_to_trade = request.POST.get('open_to_trade') == 'on'
        target.negotiable = request.POST.get('negotiable') == 'on'

        target.description = request.POST.get('description', '') or ''
        target.video_url = request.POST.get('video_url', '') or ''

        # Metai neprivalomi; `year` yra NOT NULL, todėl tuščią keičiam einamaisiais
        year = _int_or_none(request.POST.get('year'))
        target.year = year or timezone.now().year
        target.mileage = 0

        country = request.POST.get('country', 'US')
        target.country = country
        if country == 'US':
            state = request.POST.get('state', '')
            if not state:
                errors.append(_('Valstija yra privaloma'))
            target.state = state
            target.city = request.POST.get('city', '') or '—'
        else:
            city = request.POST.get('city', '')
            if not city:
                errors.append(_('Miestas yra privalomas'))
            target.city = city
            target.state = ''
        target.address = request.POST.get('address', '') or ''

        phone_val = (request.POST.get('phone', '') or '').strip()
        if not phone_val:
            errors.append(_('Telefonas yra privalomas'))
        elif hasattr(request.user, 'profile'):
            request.user.profile.phone_number = phone_val
            request.user.profile.save(update_fields=['phone_number'])

        if not is_edit_mode and not request.POST.get('agree_terms'):
            errors.append(_('Turite sutikti su taisyklėmis'))

        # Pavadinimo lauko etalone nėra — generuojam
        parts = [p for p in (target.elec_brand_text, target.constr_model_text) if p]
        type_label = dict(Listing.ELEC_TYPE_CHOICES).get(elec_type, '')
        if type_label:
            parts.append(str(type_label))
        target.title = ' '.join(str(p) for p in parts)[:200] or 'Elektronika'

        new_images, img_errors = split_valid_images(request.FILES.getlist('images'))
        errors.extend(img_errors)

        if errors:
            for e in errors:
                messages.error(request, e)
            return _render_form(request, target, is_edit_mode, request.POST)

        target.latitude, target.longitude = get_coordinates_for_location(target.city, target.country, request.POST)

        try:
            target.save()
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return _render_form(request, target, is_edit_mode, request.POST)

        ListingEquipment.objects.filter(listing=target).delete()
        for eid in request.POST.getlist('equipment'):
            try:
                ListingEquipment.objects.create(listing=target, equipment_id=int(eid))
            except (ValueError, TypeError):
                continue

        existing = target.images.count()
        for i, image in enumerate(new_images[:36]):
            try:
                ListingImage.objects.create(
                    listing=target, image=image,
                    is_main=(existing == 0 and i == 0), order=existing + i,
                )
            except Exception as e:
                print(f"[electronics] image upload failed: {e}")

        if is_edit_mode:
            try:
                new_price = float(target.price)
                if new_price != old_price and old_price > 0:
                    if new_price < old_price:
                        _send_saved_listing_price_drop_emails(target, old_price, new_price)
                    else:
                        _send_saved_listing_updated_emails(target, 'Listing updated')
                else:
                    _send_saved_listing_updated_emails(target, 'Listing updated')
            except (ValueError, TypeError):
                pass
            messages.success(request, _('Skelbimas atnaujintas.'))
            return redirect('listing_edit_hub', pk=target.pk)

        is_free, _c, _l = can_create_free_listing(request.user)
        if is_free:
            target.activate(days=FREE_LISTING_DAYS)
            _send_listing_published_email(target, request.user)
            return redirect(
                reverse('listing_success', kwargs={'pk': target.pk}) + '?action=published')
        return redirect('listing_select_plan', pk=target.pk)

    return _render_form(request, listing, is_edit_mode, None)


def _render_form(request, listing, is_edit_mode, posted):
    user_phone = ''
    if hasattr(request.user, 'profile') and request.user.profile.phone_number:
        user_phone = request.user.profile.phone_number

    selected_equipment = []
    if listing and listing.pk:
        selected_equipment = [
            str(i) for i in listing.equipment_items.values_list('equipment_id', flat=True)]
    elif posted:
        selected_equipment = posted.getlist('equipment')

    current_type = ''
    if posted:
        current_type = posted.get('elec_type', '')
    elif listing:
        current_type = listing.elec_type or ''

    return render(request, 'listings/electronics_listing_create.html', {
        'is_edit_mode': is_edit_mode,
        'listing': listing,
        'edit_listing_id': listing.pk if (listing and listing.pk) else None,
        'type_choices': Listing.ELEC_TYPE_CHOICES,
        'current_type': current_type,
        'power_required_types': list(POWER_REQUIRED_TYPES),
        'brand_choices': ELEC_BRANDS,
        'condition_choices': [(v, l) for v, l in Listing.CONDITION_CHOICES
                              if v in ('used', 'new')],
        'color_choices': Listing.COLOR_CHOICES,
        'channel_choices': ELEC_CHANNELS,
        'equipment_by_category': get_elec_equipment(),
        'selected_equipment': selected_equipment,
        'country_choices': _country_choices(),
        'us_states': Listing.US_STATE_CHOICES,
        'user_phone': user_phone,
        'posted': posted,
    })
