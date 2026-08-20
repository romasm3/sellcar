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
