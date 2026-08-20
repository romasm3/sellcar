# apps/listings/brands.py
# ═══════════════════════════════════════════════════════════
# VIENAS MARKIŲ ŠALTINIS visiems paviršiams.
#
# Create forma, greitoji panelė, šoninė filtrų juosta ir išplėstinė
# paieška privalo kviesti TIK šias funkcijas. Naujas markių sąrašas
# kategorijai nekuriamas — pridedama šeima (BrandScope) arba markė
# prijungiama prie esamos šeimos.
# ═══════════════════════════════════════════════════════════
import unicodedata

from django.db.models import Count, Q

from apps.listings import brand_registry as reg
from apps.listings.models import Brand, BrandScope

TOP_LIMIT = 12


def normalize(text):
    """Paieškos raktas: be diakritikų, be skyriklių, mažosiomis.

    Naudojamas TIK paieškai sąraše — pavadinimai DB nekeičiami.
    „Skoda", „SKODA" ir „Škoda" surandami tuo pačiu įvedimu.
    """
    s = unicodedata.normalize('NFKD', text or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('ß', 'ss').replace('ł', 'l').replace('Ł', 'L')
    return ''.join(c for c in s.lower() if c.isalnum())


def scope_for(vehicle_type_slug=None, subcategory_slug=None, rent_type=None):
    return reg.scope_for(vehicle_type_slug, subcategory_slug, rent_type)


def brands_qs(scope_key):
    """Šeimos markės. Nežinoma šeima → tuščias qs, ne visos markės."""
    if not scope_key:
        return Brand.objects.none()
    return Brand.objects.filter(scopes__key=scope_key).order_by('name')


def has_models(scope_key):
    """Ar šeimai rodoma modelių kaskada (kaip autogide)."""
    scope = BrandScope.objects.filter(key=scope_key).first()
    return bool(scope and scope.has_models)


def brand_rows(scope_key, counts=None):
    """Eilutės widget'ui: [{id, name, slug, count, is_top, search}].

    ``counts`` — {brand_id: skelbimų kiekis}; jei paduota, „Top markės"
    renkamos pagal jį, kitaip pagal Brand.is_top / order.
    """
    rows = []
    for b in brands_qs(scope_key).only('id', 'name', 'slug', 'is_top', 'order'):
        rows.append({
            'id': b.id,
            'name': b.name,
            'slug': b.slug,
            'count': (counts or {}).get(b.id, 0),
            'is_top': b.is_top,
            'search': normalize(b.name),
        })
    return rows


def split_top(rows, limit=TOP_LIMIT):
    """(top, visos) — top pagal skelbimų kiekį, kaip autogide."""
    with_counts = [r for r in rows if r['count']]
    if with_counts:
        top = sorted(with_counts, key=lambda r: (-r['count'], r['name']))[:limit]
    else:
        top = [r for r in rows if r['is_top']][:limit]
    return top, rows


def listing_counts(scope_key, listings_qs, field='brand_id'):
    """{brand_id: kiekis} iš paduoto skelbimų queryset'o."""
    return {
        row[field]: row['n']
        for row in listings_qs.values(field).annotate(n=Count('id'))
        if row[field]
    }


def find(scope_key, text):
    """Markė pagal vartotojo įvestą tekstą (rašybai atlaidus)."""
    text = (text or '').strip()
    if not text:
        return None
    exact = brands_qs(scope_key).filter(name__iexact=text).first()
    if exact:
        return exact
    key = normalize(text)
    for b in brands_qs(scope_key):
        if normalize(b.name) == key:
            return b
    return None


# ── „Kita" — vartotojo įvesti pavadinimai ───────────────────────────
# Sąrašas turi pildytis pagal realų poreikį: jei markės nėra, žmogus
# renkasi „Kita" ir įrašo ranka, o admin'e tai matosi kaip pasiūlymas
# su skaitikliu.
OTHER_VALUE = '__other__'
OTHER_LABEL = 'Kita'


def posted_brand(request, field, scope_key):
    """Markės reikšmė iš POST, sutvarkius „Kita".

    Jei pasirinkta „Kita", imamas laisvo teksto laukas `<field>_other`
    ir įvestas pavadinimas užregistruojamas kaip pasiūlymas admin'ui.
    """
    value = (request.POST.get(field, '') or '').strip()
    if value != OTHER_VALUE:
        return value
    typed = (request.POST.get(f'{field}_other', '') or '').strip()[:100]
    if typed:
        record_suggestion(scope_key, typed)
    return typed


def record_suggestion(scope_key, name):
    """Įsimena per „Kita" įvestą pavadinimą. Grąžina BrandSuggestion arba None."""
    from apps.listings.models import BrandScope, BrandSuggestion

    name = (name or '').strip()[:100]
    if not name or not scope_key:
        return None
    # Jei markė jau yra šeimoje (žmogus tiesiog nerado sąraše) —
    # pasiūlymo nekuriam.
    if find(scope_key, name):
        return None
    scope = BrandScope.objects.filter(key=scope_key).first()
    if scope is None:
        return None

    existing = None
    key = normalize(name)
    for row in BrandSuggestion.objects.filter(scope=scope):
        if normalize(row.name) == key:
            existing = row
            break
    if existing is None:
        return BrandSuggestion.objects.create(scope=scope, name=name)
    existing.times_used += 1
    existing.save(update_fields=['times_used', 'last_seen'])
    return existing


def approve_suggestion(suggestion):
    """Pasiūlymas → tikra markė šeimoje. Idempotentiška."""
    from django.utils.text import slugify

    from apps.listings.models import Brand, BrandSuggestion

    if suggestion.status == BrandSuggestion.STATUS_APPROVED and suggestion.approved_brand:
        return suggestion.approved_brand

    brand = Brand.objects.filter(name=suggestion.name).first()
    if brand is None:
        slug = slugify(suggestion.name) or 'brand'
        base, i = slug, 2
        while Brand.objects.filter(slug=slug).exists():
            slug = f'{base}-{i}'
            i += 1
        brand = Brand.objects.create(name=suggestion.name, slug=slug)
    brand.scopes.add(suggestion.scope)

    # Kol skelbimai rodo į senąsias lenteles, markė turi atsirasti ir ten.
    _mirror_to_legacy(brand, suggestion.scope.key)

    suggestion.status = BrandSuggestion.STATUS_APPROVED
    suggestion.approved_brand = brand
    suggestion.save(update_fields=['status', 'approved_brand', 'last_seen'])
    return brand


def _mirror_to_legacy(brand, scope_key):
    from django.utils.text import slugify

    from apps.listings import brand_registry as reg
    from apps.listings import models as m

    model_name = reg.SCOPE_LEGACY_MODEL.get(scope_key)
    if not model_name:
        return
    model = getattr(m, model_name)
    field = {'MotorcycleBrand': 'legacy_moto', 'TruckBrand': 'legacy_truck',
             'GearBrand': 'legacy_gear'}[model_name]
    row = model.objects.filter(name=brand.name).first()
    if row is None:
        slug = slugify(brand.name) or 'brand'
        base, i = slug, 2
        while model.objects.filter(slug=slug).exists():
            slug = f'{base}-{i}'
            i += 1
        row = model.objects.create(name=brand.name, slug=slug)
    if getattr(brand, f'{field}_id') != row.id:
        setattr(brand, field, row)
        brand.save(update_fields=[field])
