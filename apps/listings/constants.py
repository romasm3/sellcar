# apps/listings/constants.py

# ════════════════════════════════════════════════════════════
# ACCOUNT TYPES (used by apps.accounts.models.Profile)
# ════════════════════════════════════════════════════════════

ACCOUNT_TYPE_PRIVATE = 'private'
ACCOUNT_TYPE_DEALER = 'dealer'

ACCOUNT_TYPE_CHOICES = [
    (ACCOUNT_TYPE_PRIVATE, 'Private seller'),
    (ACCOUNT_TYPE_DEALER, 'Dealer'),
]

DEALER_STATUS_NONE = 'none'
DEALER_STATUS_PENDING = 'pending'
DEALER_STATUS_APPROVED = 'approved'
DEALER_STATUS_REJECTED = 'rejected'

DEALER_STATUS_CHOICES = [
    (DEALER_STATUS_NONE, 'None'),
    (DEALER_STATUS_PENDING, 'Pending'),
    (DEALER_STATUS_APPROVED, 'Approved'),
    (DEALER_STATUS_REJECTED, 'Rejected'),
]


# ════════════════════════════════════════════════════════════
# LISTING LIMITS
# ════════════════════════════════════════════════════════════

PRIVATE_FREE_LIMIT = 3
PRIVATE_SUB_LIMIT = 5
DEALER_LIMIT = 30
DEALER_SUBSCRIPTION_DAYS = 30
FREE_LISTING_DAYS = 30

PER_LISTING_PRICE_USD = 5
PRIVATE_SUB_PRICE_USD = 15
DEALER_SUB_PRICE_USD = 100
DEALER_SUB_PRICE_EUR = 100


# ════════════════════════════════════════════════════════════
# PAID PLANS — multi-category (Cars / Trucks / Motorcycles)
# ════════════════════════════════════════════════════════════
# Bazinės kainos pagal kategoriją.
# Skirtingos kategorijos turi skirtingas kainas:
#   - Cars        — bazinė rinka
#   - Trucks      — brangesni (ilgiau parduodami, B2B rinka)
#   - Motorcycles — pigesni (mažesnis ticket size)
#
# Visos kategorijos turi 3 plan'us: Basic / Standard / Recommended
# ════════════════════════════════════════════════════════════

PAID_PLANS_BY_CATEGORY = {
    'cars': [
        {
            'code': 'premium_90',
            'label': 'Recommended',
            'days': 90,
            'price_usd': 12,
            'boost_days': 10,
            'boost_count': 3,
            'featured_days': 1,
            'highlight_days': 14,
            'is_recommended': True,
        },
        {
            'code': 'standard_60',
            'label': 'Standard',
            'days': 60,
            'price_usd': 8,
            'boost_days': 10,
            'boost_count': 2,
            'featured_days': 0,
            'highlight_days': 7,
            'is_recommended': False,
        },
        {
            'code': 'basic_30',
            'label': 'Basic',
            'days': 30,
            'price_usd': 5,
            'boost_days': 5,
            'boost_count': 1,
            'featured_days': 0,
            'highlight_days': 0,
            'is_recommended': False,
        },
    ],
    'trucks': [
        {
            'code': 'premium_90',
            'label': 'Recommended',
            'days': 90,
            'price_usd': 20,
            'boost_days': 10,
            'boost_count': 3,
            'featured_days': 1,
            'highlight_days': 14,
            'is_recommended': True,
        },
        {
            'code': 'standard_60',
            'label': 'Standard',
            'days': 60,
            'price_usd': 14,
            'boost_days': 10,
            'boost_count': 2,
            'featured_days': 0,
            'highlight_days': 7,
            'is_recommended': False,
        },
        {
            'code': 'basic_30',
            'label': 'Basic',
            'days': 30,
            'price_usd': 8,
            'boost_days': 5,
            'boost_count': 1,
            'featured_days': 0,
            'highlight_days': 0,
            'is_recommended': False,
        },
    ],
    'motorcycles': [
        {
            'code': 'premium_90',
            'label': 'Recommended',
            'days': 90,
            'price_usd': 10,
            'boost_days': 10,
            'boost_count': 3,
            'featured_days': 1,
            'highlight_days': 14,
            'is_recommended': True,
        },
        {
            'code': 'standard_60',
            'label': 'Standard',
            'days': 60,
            'price_usd': 7,
            'boost_days': 10,
            'boost_count': 2,
            'featured_days': 0,
            'highlight_days': 7,
            'is_recommended': False,
        },
        {
            'code': 'basic_30',
            'label': 'Basic',
            'days': 30,
            'price_usd': 4,
            'boost_days': 5,
            'boost_count': 1,
            'featured_days': 0,
            'highlight_days': 0,
            'is_recommended': False,
        },
    ],
}

# Backward-compat: senas kintamasis = cars plan'ai
# (kad nieko nesulaužtų jei kažkur kitur naudojama)
PAID_PLANS = PAID_PLANS_BY_CATEGORY['cars']


# ════════════════════════════════════════════════════════════
# PRICE MULTIPLIER (FUTURE FEATURE)
# ════════════════════════════════════════════════════════════
# Kuo brangesnis listing'as → tuo brangesnis plano mokestis.
# DABAR: išjungtas (MULTIPLIER_ENABLED = False).
# Kad ĮJUNGTI: tiesiog pakeisti į True.
#
# Pavyzdžiui (kai įjungta):
#   BMW M4 už $50k → Recommended 90d = $12 × 2.0 = $24
#   VW Golf už $5k → Recommended 90d = $12 × 1.0 = $12
# ════════════════════════════════════════════════════════════

MULTIPLIER_ENABLED = False  # Kai bus pasiruošta — pakeisti į True

PRICE_MULTIPLIERS = [
    # (min_price, max_price, multiplier)
    (0,      5000,    1.0),  # Tier 1: pigus auto
    (5000,   20000,   1.2),  # Tier 2: vidutinis
    (20000,  50000,   1.5),  # Tier 3: geras
    (50000,  100000,  2.0),  # Tier 4: brangus
    (100000, 999999999, 2.5),  # Tier 5: luxury
]


def get_price_multiplier(listing_price):
    """Grąžina multiplier'į pagal listing.price.
    Jei MULTIPLIER_ENABLED = False, visada grąžina 1.0."""
    if not MULTIPLIER_ENABLED:
        return 1.0
    if not listing_price or listing_price <= 0:
        return 1.0

    price = float(listing_price)
    for min_p, max_p, mult in PRICE_MULTIPLIERS:
        if min_p <= price < max_p:
            return mult
    return 1.0


def get_plans_for_category(category_slug, listing_price=None):
    """Grąžina plan'us pagal kategoriją su preskaičiuotom kainom (jei multiplier įjungtas).

    Args:
        category_slug: 'cars' / 'trucks' / 'motorcycles' / etc.
        listing_price: listing.price (Decimal/float) — naudojamas kai MULTIPLIER_ENABLED=True

    Returns:
        list of plan dicts su 'final_price_usd' lauku
    """
    plans = PAID_PLANS_BY_CATEGORY.get(category_slug)
    if not plans:
        # Fallback: jei kategorija nepalaikoma (vans/boats/etc) → naudoja cars kainas
        plans = PAID_PLANS_BY_CATEGORY['cars']

    multiplier = get_price_multiplier(listing_price)

    result = []
    for p in plans:
        plan_copy = dict(p)
        plan_copy['final_price_usd'] = round(p['price_usd'] * multiplier, 2)
        plan_copy['multiplier_applied'] = multiplier
        result.append(plan_copy)

    return result


def get_plan_by_code(code, category_slug='cars', listing_price=None):
    """Grąžina vieną plan'ą pagal code + kategoriją + kainą.

    Args:
        code: 'basic_30' / 'standard_60' / 'premium_90'
        category_slug: 'cars' / 'trucks' / 'motorcycles' / etc.
        listing_price: listing.price (Decimal/float) — multiplier'iui

    Returns:
        plan dict su 'final_price_usd' arba None
    """
    plans = get_plans_for_category(category_slug, listing_price)
    for p in plans:
        if p['code'] == code:
            return p
    return None


# ════════════════════════════════════════════════════════════
# ADD-ON SERVICES (kainos NEMULTIPLIKUOJAMOS — flat per visus)
# ════════════════════════════════════════════════════════════

ADDON_RENEW = {
    'code': 'extra_stars',
    'label': 'Top Spot Stars',
    'icon': '★',
    'price_per_unit_usd': 1.00,  # per star per day
    'max_count': 20,  # max stars per purchase
    'max_days': 42,
}

ADDON_FEATURED = {
    'code': 'extra_featured',
    'label': 'Featured on homepage',
    'icon': '☆',
    'price_per_day_usd': 0.30,
    'max_days': 42,
}


# ════════════════════════════════════════════════════════════
# LIMIT HELPERS
# ════════════════════════════════════════════════════════════

def can_create_listing(user):
    """All-paid model: anyone authenticated can create drafts.
    Payment happens at publish time (select-plan flow), not at create."""
    if not user.is_authenticated:
        return (False, 0, 0)

    from .models import Listing
    active_count = Listing.objects.filter(seller=user, status='active').count()

    # No limit — return huge number for compatibility
    return (True, active_count, 99999)


def mokejimai_ijungti():
    """Ar mokėjimai įjungti. VIENAS jungiklis visai svetainei.

    Kol `MOKEJIMAI_IJUNGTI = False`, kiekvienas skelbimas nemokamas ir
    publikuojamas iš karto. Mokėjimo kodas vietoje — tik apeinamas.
    """
    from django.conf import settings
    return bool(getattr(settings, 'MOKEJIMAI_IJUNGTI', False))


def can_create_free_listing(user):
    """Pirmi PRIVATE_FREE_LIMIT aktyvūs skelbimai — nemokami (auto-publish).
    Nuo (PRIVATE_FREE_LIMIT + 1) — reikia mokamo plano.

    Išjungus mokėjimus nemokami VISI: čia vienas taškas, per kurį
    sprendžia visų kategorijų įkėlimo formos, tad jungiklio užtenka
    vieno — nereikia lopyti dvidešimties `redirect('listing_select_plan')`.

    Returns:
        (is_free, active_count, free_limit)
    """
    if not user.is_authenticated:
        return (False, 0, 0)

    from .models import Listing
    active_count = Listing.objects.filter(seller=user, status='active').count()
    if not mokejimai_ijungti():
        return (True, active_count, 99999)
    is_free = active_count < PRIVATE_FREE_LIMIT
    return (is_free, active_count, PRIVATE_FREE_LIMIT)