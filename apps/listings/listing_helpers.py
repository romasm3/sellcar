from django.utils.translation import gettext as _
"""
═══════════════════════════════════════════════════════════════════════════════
AutoLeft — Listing Helper Functions
═══════════════════════════════════════════════════════════════════════════════

Bendros funkcijos VISOMS kategorijų (Cars, Motorcycles, Trucks, Car-for-parts,
Moto Gear, ir t.t.) views'ams.

Tikslas: NEKARTOTI to paties kodo 5 failuose. Vietoj to — vienoje vietoje 
suderini logiką, ir visi view'ai automatiškai gauna pakeitimus.

═══════════════════════════════════════════════════════════════════════════════
KAIP NAUDOTI
═══════════════════════════════════════════════════════════════════════════════

Kategorijos view'e (pvz. car_for_parts_views.py):

    from .listing_helpers import (
        parse_common_listing_fields,
        validate_common_fields,
        apply_common_fields_to_listing,
        finalize_listing_publish,
        finalize_listing_edit,
    )

    def my_category_create(request):
        # ... draft setup ...
        
        if request.method == 'POST':
            # 1. Parse BENDRUS laukus
            common = parse_common_listing_fields(request)
            
            # 2. Parse SPECIFINIUS laukus (kategorijos-unique)
            brand_id = request.POST.get('brand')
            modification = request.POST.get('modification')
            # ... etc
            
            # 3. Validate
            errors = validate_common_fields(common)
            # ... pridek specifines validacijas ...
            
            if not errors:
                # 4. Apply BENDRUS laukus
                apply_common_fields_to_listing(draft, common)
                
                # 5. Apply SPECIFINIUS laukus
                draft.modification = modification
                # ... etc ...
                
                # 6. Publish (viena eilute, viskas atlieka helperis)
                finalize_listing_publish(draft, common['phone'], request.user)
                
                return redirect('listing_success', pk=draft.pk)
"""


# ═══════════════════════════════════════════════════════════════════════════
# PARSE HELPERS — saugiai parse'ina POST string'us į int/float
# ═══════════════════════════════════════════════════════════════════════════

def _int_or_none(value):
    """Saugiai parse'ina string į int, arba grąžina None jei tuščia/invalid."""
    if value is None or value == '':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _float_or_none(value):
    """Saugiai parse'ina string į float, arba grąžina None jei tuščia/invalid."""
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# ═══════════════════════════════════════════════════════════════════════════
# 1. PARSE COMMON FIELDS — bendrų laukų parsavimas iš POST
# ═══════════════════════════════════════════════════════════════════════════

def parse_common_listing_fields(request):
    """
    Parsuoja BENDRUS laukus kurie kartojasi VISOSE kategorijose.
    
    Grąžina dict su standartiniais raktais:
    - condition, year, price, currency, negotiable
    - description
    - phone, email
    - country, state, city, address, postal_code, hide_exact_address
    
    Specifiniai kategorijos laukai (brand, body_type, modification, etc.) 
    parse'inami atskirai pačiame view'e.
    """
    return {
        # Pagrindiniai
        'condition': request.POST.get('condition', '').strip(),
        'year': _int_or_none(request.POST.get('year')),
        'price': _float_or_none(request.POST.get('price')),
        'currency': request.POST.get('currency', 'USD').strip() or 'USD',
        'negotiable': request.POST.get('negotiable') in ('on', 'true', '1'),
        
        # Aprašymas
        'description': request.POST.get('description', '').strip(),
        
        # Kontaktai
        'phone': request.POST.get('phone', '').strip(),
        'email': request.POST.get('email', '').strip(),
        
        # Lokacija
        'country': request.POST.get('country', 'US').strip() or 'US',
        'state': request.POST.get('state', '').strip(),
        'city': request.POST.get('city', '').strip(),
        'address': request.POST.get('address', '').strip(),
        'postal_code': request.POST.get('postal_code', '').strip(),
        'hide_exact_address': request.POST.get('hide_exact_address') in ('on', 'true', '1'),

        # Vieta žemėlapyje — koordinatės iš žymeklio (partials/_vietos_blokas.html).
        # Miestas ir šalis iš geokodavimo naudojami tik tada, kai laukai tušti:
        # ranka įvestas miestas svarbesnis už atspėtą.
        'latitude': _float_or_none(request.POST.get('latitude')),
        'longitude': _float_or_none(request.POST.get('longitude')),
        'vietos_miestas': request.POST.get('vietos_miestas', '').strip(),
        'vietos_salis': request.POST.get('vietos_salis', '').strip(),

        # Sutikimas su taisyklėmis (tik CREATE)
        'agree_terms': request.POST.get('agree_terms') in ('on', 'true', '1'),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. VALIDATE COMMON FIELDS — bendrų laukų validacija
# ═══════════════════════════════════════════════════════════════════════════

def validate_common_fields(common_data, require_condition=True, require_year=True,
                           require_terms=False):
    """
    Validuoja BENDRUS required laukus. Grąžina errors list (tuščias = ok).

    Optional flags:
    - require_condition: ar Condition required (default True)
    - require_year: ar Year required (default True)
    - require_terms: ar sutikimas su taisyklėmis required (tik CREATE)
    """
    errors = []

    if require_terms and not common_data.get('agree_terms'):
        errors.append(_('Turite sutikti su taisyklėmis'))

    if require_condition and not common_data['condition']:
        errors.append(_('Būklė yra privaloma'))
    
    if require_year and not common_data['year']:
        errors.append(_('Metai yra privalomi'))
    
    if not common_data['price'] or common_data['price'] <= 0:
        errors.append(_('Kaina yra privaloma'))
    
    if not common_data['phone']:
        errors.append(_('Telefonas yra privalomas'))
    
    if not common_data['city']:
        errors.append(_('Miestas yra privalomas'))
    
    if common_data['country'] == 'US' and not common_data['state']:
        errors.append(_('Valstija yra privaloma'))
    
    return errors


# ═══════════════════════════════════════════════════════════════════════════
# 3. APPLY COMMON FIELDS TO LISTING — bendrų laukų užpildymas į listing
# ═══════════════════════════════════════════════════════════════════════════

def apply_common_fields_to_listing(listing, common_data):
    """
    Užpildo BENDRUS laukus į listing objektą.
    NEPADAROMA save() — tai daro finalize_listing_publish() arba 
    finalize_listing_edit().
    
    Specifinius laukus (brand, model, body_type, etc.) view'as turi pats 
    užpildyti po šios funkcijos.
    """
    listing.condition = common_data['condition']
    if common_data['year']:
        listing.year = common_data['year']
    listing.price = common_data['price']
    listing.currency = common_data['currency']
    listing.negotiable = common_data['negotiable']
    listing.description = common_data['description']
    
    # Country/State swap logic — state TIK kai US
    listing.country = common_data['country']
    listing.state = common_data['state'] if common_data['country'] == 'US' else ''
    
    listing.city = common_data['city'] or common_data.get('vietos_miestas', '')
    listing.address = common_data['address']
    listing.postal_code = common_data['postal_code']
    listing.hide_exact_address = common_data['hide_exact_address']

    # Koordinatės iš žemėlapio žymeklio — tikslesnės už miesto centrą,
    # todėl perrašo tai, ką vėliau spėtų get_coordinates_for_location().
    if common_data.get('latitude') is not None and common_data.get('longitude') is not None:
        listing.latitude = common_data['latitude']
        listing.longitude = common_data['longitude']
        listing.koordinates_tikslios = True


# ═══════════════════════════════════════════════════════════════════════════
# 4. FINALIZE PUBLISH — paskutiniai žingsniai prieš publish (CREATE)
# ═══════════════════════════════════════════════════════════════════════════

def finalize_listing_publish(listing, phone, user, send_email=True, days=None):
    """
    Standartinis PUBLISH workflow VISOMS kategorijoms.
    
    Atlieka:
    1. Phone save į user profile
    2. Coordinates calculation (lat/lng iš city/country)
    3. CRITICAL: listing.save() PRIEŠ activate() — kad nepradangtų laukai
    4. Activate (status='active', set activated_at)
    5. Send "listing published" email
    
    Args:
        listing: Listing objektas (jau su user'io užpildytais laukais)
        phone: Telefono numeris
        user: request.user
        send_email: Ar siųsti published email (default True)
        days: Kiek dienų aktyvus (default Listing.DEFAULT_ACTIVE_DAYS)
    """
    # Importas viduje, kad išvengti cyclic imports
    from .models import Listing
    from .views import get_coordinates_for_location
    
    # 1. Phone save į user profile
    if phone and hasattr(user, 'profile'):
        user.profile.phone_number = phone
        user.profile.save(update_fields=['phone_number'])
    
    # 2. Coordinates — tik jei žmogus nepasižymėjo vietos žemėlapyje.
    # Žymeklio koordinatės tikslios, miesto centras — apytikslis.
    if listing.latitude is None or listing.longitude is None:
        if listing.city and listing.country:
            lat, lng = get_coordinates_for_location(listing.city, listing.country)
            listing.latitude = lat
            listing.longitude = lng
    
    # 3. CRITICAL: save() PRIEŠ activate()
    # activate() naudoja update_fields=['status', 'activated_at', ...] 
    # ir IGNORUOS visus kitus field changes jei jų nesave'insim pirma!
    listing.save()
    
    # 4. Activate
    if days is None:
        days = Listing.DEFAULT_ACTIVE_DAYS
    listing.activate(days=days)
    
    # 5. Email
    if send_email:
        try:
            from .views import _send_listing_published_email
            _send_listing_published_email(listing, user)
        except (ImportError, AttributeError):
            # Email funkcija gali neegzistuoti senose versijose — silent fail
            pass


# ═══════════════════════════════════════════════════════════════════════════
# 5. FINALIZE EDIT — paskutiniai žingsniai prieš save (EDIT)
# ═══════════════════════════════════════════════════════════════════════════

def finalize_listing_edit(listing, phone, user, recalc_coordinates=True):
    """
    Standartinis EDIT workflow VISOMS kategorijoms.
    
    Atlieka:
    1. Phone save į user profile (jei pasikeitė)
    2. Recalculate coordinates (jei city/country pasikeitė)
    3. listing.save()
    
    Args:
        listing: Listing objektas (jau su pakeistais laukais)
        phone: Telefono numeris
        user: request.user
        recalc_coordinates: Ar perskaičiuoti koordinates (default True)
    """
    from .views import get_coordinates_for_location
    
    # 1. Phone save į profile
    if phone and hasattr(user, 'profile'):
        user.profile.phone_number = phone
        user.profile.save(update_fields=['phone_number'])
    
    # 2. Recalculate coordinates
    if recalc_coordinates and listing.city and listing.country:
        lat, lng = get_coordinates_for_location(listing.city, listing.country)
        listing.latitude = lat
        listing.longitude = lng
    
    # 3. Save
    listing.save()


# ═══════════════════════════════════════════════════════════════════════════
# 6. BUILD TITLE — bendras titulo formavimas
# ═══════════════════════════════════════════════════════════════════════════

def build_listing_title(brand_name='', model_name='', year=None, suffix=''):
    """
    Sudeda title iš dalių. Praleidžia tuščias dalis.
    
    Examples:
        build_listing_title('BMW', 'M5', 2024)              → 'BMW M5 2024'
        build_listing_title('AC', 'Cobra', 2026, '(dalimis)') → 'AC Cobra 2026 (dalimis)'
        build_listing_title('Honda', '', 2023)              → 'Honda 2023'
    """
    parts = []
    if brand_name:
        parts.append(str(brand_name))
    if model_name:
        parts.append(str(model_name))
    if year:
        parts.append(str(year))
    if suffix:
        parts.append(str(suffix))
    return ' '.join(parts)

# ═══════════════════════════════════════════════════════════════════════════
# APMOKĖTO PLANO PRITAIKYMAS
# ═══════════════════════════════════════════════════════════════════════════

def pritaikyti_apmoketa_plana(
    listing, *, plan_days,
    plan_boost_days=0, plan_boost_count=0,
    plan_featured_days=0, plan_highlight_days=0,
    renew_count=0, renew_days=0, addon_featured_days=0,
    send_email=True, pratesimas=False,
):
    """Aktyvuoja skelbimą ir uždeda visas apmokėto plano paslaugas.

    VIENINTELĖ vieta, kur tai daroma. Kviečia du keliai:
      • Stripe webhook'as (apps/accounts/views.py), kai apmokėta kortele;
      • listing_pay_plan, kai po nuolaidos suma tapo 0 ir Stripe nedalyvauja.

    Anksčiau ši logika gulėjo tik webhook'e, todėl 100 % nuolaidos atveju
    skelbimas nebūtų aktyvuotas iš viso.

    Nieko nedaro, jei skelbimas jau aktyvus — webhook'as gali ateiti du kartus.
    Išimtis: pratesimas=True — tada aktyvus skelbimas PRATĘSIAMAS (dienos
    pridedamos prie likusio galiojimo), o „paskelbta" laiškas nesiunčiamas.
    Grąžina True, jei aktyvavo arba pratęsė.
    """
    from datetime import timedelta
    from django.utils import timezone

    if listing.status == 'active' and not pratesimas:
        return False

    now = timezone.now()
    if pratesimas:
        listing.pratesti(days=plan_days)
        send_email = False
    else:
        listing.activate(days=plan_days)

    if send_email:
        try:
            from .views import _send_listing_published_email
            _send_listing_published_email(listing, listing.seller)
        except Exception as email_err:          # el. laiškas nekliudo aktyvavimui
            print(f'[planas] listing_published email failed: {email_err}')

    # „Atnaujinta" žymė, jei planas turi boost'ą arba pirkta žvaigždučių
    if plan_boost_days > 0 or renew_count > 0:
        listing.last_boosted_at = now
        listing.save(update_fields=['last_boosted_at'])

    # Žvaigždutės — plano ir priedo suma; trukmė ilgesnioji iš dviejų
    final_star_count = plan_boost_count + renew_count
    final_star_days = max(plan_boost_days, renew_days)
    if final_star_count > 0:
        listing.star_level = 1
        listing.star_count = final_star_count
        if final_star_days > 0:
            if listing.star_expires_at and listing.star_expires_at > now:
                listing.star_expires_at += timedelta(days=final_star_days)
            else:
                listing.star_expires_at = now + timedelta(days=final_star_days)
        listing.save(update_fields=['star_level', 'star_count', 'star_expires_at'])

    # Reklama pagrindiniame — planas + priedas
    total_featured = plan_featured_days + addon_featured_days
    if total_featured > 0:
        if listing.featured_until and listing.featured_until > now:
            listing.featured_until += timedelta(days=total_featured)
        else:
            listing.featured_until = now + timedelta(days=total_featured)
        listing.save(update_fields=['featured_until'])

    # Paryškinimas — tik iš plano
    if plan_highlight_days > 0:
        if listing.highlight_until and listing.highlight_until > now:
            listing.highlight_until += timedelta(days=plan_highlight_days)
        else:
            listing.highlight_until = now + timedelta(days=plan_highlight_days)
        listing.save(update_fields=['highlight_until'])

    return True
