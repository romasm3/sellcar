# SellCar Design Patterns

> **Tikslas:** Surašytos standartinės UI/UX taisyklės naudojamos VISOSE kategorijose (Cars, Motorcycles, Trucks, Car-for-parts, Moto Gear, ir t.t.).
>
> **Kaip naudoti šį failą:**
> 1. Pradėdamas naują pokalbį su Claude — upload'ink šį failą.
> 2. Prieš diegiant naują UI elementą — patikrink ar jis čia jau aprašytas.
> 3. Jei pridedi naują reusable pattern'ą — papildyk šį failą.

---

## 0. ⭐ HELPER FUNCTIONS (apps/listings/listing_helpers.py)

**Visi nauji kategorijų view'ai PRIVALO naudoti šiuos helper'ius.** Tai užtikrina konsistentiškumą per VISAS kategorijas.

### Importai

```python
from .listing_helpers import (
    _int_or_none,
    _float_or_none,
    parse_common_listing_fields,
    validate_common_fields,
    apply_common_fields_to_listing,
    finalize_listing_publish,
    finalize_listing_edit,
    build_listing_title,
)
```

### Funkcijos ir kas į jas įeina

| Funkcija | Ką daro |
|----------|---------|
| `parse_common_listing_fields(request)` | Parsuoja BENDRUS POST laukus: phone, country, state, city, address, price, year, condition, description, currency, negotiable, postal_code, hide_exact_address |
| `validate_common_fields(common)` | Patikrina ar užpildyti: condition, year, price>0, phone, city, state (jei US). Grąžina errors list |
| `apply_common_fields_to_listing(listing, common)` | Užpildo BENDRUS laukus į listing objektą + state swap (US only) |
| `finalize_listing_publish(listing, phone, user)` | **PUBLISH:** save phone į profile + coords calc + save() PRIEŠ activate() + email |
| `finalize_listing_edit(listing, phone, user)` | **EDIT:** save phone į profile + coords recalc + save() |
| `build_listing_title(brand_name, model_name, year, suffix)` | Sudeda title iš dalių, praleidžia tuščias |

### CREATE view template (KOPIJUOTI naujom kategorijom)

```python
def category_create(request):
    # ... draft setup ...

    if request.method == 'POST':
        # 1. Parse fields
        common = parse_common_listing_fields(request)
        specific = _parse_category_specific_fields(request)  # ← kategorijos

        # 2. Validate
        errors = validate_common_fields(common)
        if not specific['brand_id']:
            errors.append('Brand is required')
        # ... kitos kategorijos validacijos ...

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            # 3. Apply BENDRUS
            apply_common_fields_to_listing(draft, common)

            # 4. Apply SPECIFINIUS
            _apply_category_specific_fields(draft, specific)

            # 5. Build title
            draft.title = build_listing_title(
                brand_name=draft.brand.name if draft.brand else '',
                model_name=draft.model.name if draft.model else '',
                year=draft.year,
                suffix='(suffix if needed)',
            )

            # 6. PUBLISH (viena eilutė atlieka VISKĄ)
            finalize_listing_publish(draft, common['phone'], request.user)

            return redirect('listing_success', pk=draft.pk)
```

### EDIT view — naudoti `finalize_listing_edit()` analogiškai

> ⚠️ **Niekada nerašyk save+coords+phone+activate logikos rankiniu būdu.** Visada per helper'ius. Vienas globalus pakeitimas → visos kategorijos atnaujinamos.

### 0.5 Equipment categories filtering pattern

**CARS_EQUIPMENT_CATEGORIES** konstanta `views.py` top-level:

```python
CARS_EQUIPMENT_CATEGORIES = [
    ('interior', 'Interior'),
    ('exterior', 'Exterior'),
    ('electronics', 'Electronics'),
    ('safety', 'Safety & Security'),
    ('audio_video', 'Audio, Video & Connectivity'),
    ('other', 'Other Features'),
    ('electric', 'Electric vehicle features'),
]
```

**Naudoti VISUR kur Cars formoje rodom Equipment** (quick form, advanced search):

```python
CARS_CAT_KEYS = [k for k, _ in CARS_EQUIPMENT_CATEGORIES]
cars_equipment = Equipment.objects.filter(category__in=CARS_CAT_KEYS).order_by('category', 'name')
```

**Niekada nedaryti `Equipment.objects.all()`** — leak'ina truck_*/gear į Cars formą.

Analogiškai:
- TRUCKS_EQUIPMENT_CATEGORIES = [('truck_cabin', ...), ('truck_body', ...), ...]
- MOTO_EQUIPMENT_CATEGORIES = [('gear', ...), ...] (vėliau)

### 0.6 Detail page grouped equipment (autogidas style)

**Helper:** `_build_grouped_equipment(listing)` views.py

Returns: `[{'key': cat, 'label': 'Interior', 'items': [name1, name2, ...]}, ...]`

**listing_detail view context:**
```python
context = {
    ...
    'grouped_equipment': _build_grouped_equipment(listing),
}
```

**Template** (visose 3 šakose: truck/parts/cars):
```html
{% if grouped_equipment %}
<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <h2 class="text-xl font-semibold mb-5">Equipment & Features</h2>
    {% for cat in grouped_equipment %}
    <div>
        <h3 class="text-sm font-semibold text-gray-700 mb-3">{{ cat.label }}</h3>
        <div class="flex flex-wrap gap-2">
            {% for name in cat.items %}
            <span class="inline-block px-3 py-1.5 bg-gray-100 border border-gray-200 text-gray-700 text-xs font-medium rounded-md">{{ name }}</span>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
</div>
{% endif %}
```

---

## 1. MATAVIMO VIENETŲ PERJUNGIKLIAI (km/mi, kW/HP, L/cm³, kg/lbs, m/ft…)

**Šaltinis:** `static/js/unit_toggle.js` (įtrauktas globaliai per `base.html`).

Naujose formose JS rašyti **NEREIKIA**. Užtenka vieno atributo ant įprasto
skaitinio input'o:

```html
<div>
    <label class="block text-xs font-medium text-gray-600 mb-1">{% trans "Galia (kW)" %}</label>
    <input type="number" name="power" data-unit-field="power" min="0" step="1" placeholder="-"
           value="{% if listing.power %}{{ listing.power }}{% endif %}"
           class="w-full px-3 py-2 border border-gray-300 rounded text-sm">
</div>
```

Skriptas pats:

* prideda `kW | HP` mygtukus į etiketės eilutę (input'o plotis nesikeičia);
* nuima vienetą iš etiketės teksto — `Galia (kW)` → `Galia`, `Svoris, kg` → `Svoris`
  (`<span>*</span>` privalomumo žymė lieka);
* po lauku rodo užuominą `≈ 201 HP`;
* perjungiant perkelia `name` į sugeneruotą `<input type="hidden">`, todėl
  **serveris VISADA gauna kanoninę (metrinę) reikšmę** tuo pačiu lauko vardu;
* įsimena pasirinkimą `localStorage`'e — kitą kartą JAV pirkėjui iš karto
  atsidaro `mi`/`lbs`/`ft`.

### 1.1 Taisyklės

* **Vienetas į DB nesaugomas niekada.** Nėra jokių `power_unit` / `mileage_unit`
  laukų — perjungiklis yra tik atvaizdavimui.
* `dec` reikšmė spec'e **privalo** atitikti modelio lauko tipą:
  `IntegerField` → `dec: 0`, `DecimalField` → `dec: decimal_places`.
  Kitaip į sveikaskaitį lauką nukeliaus trupmena ir POST'as luš.
* Vienos `family` laukai persijungia kartu (visi svoriai, visi matmenys…).
* Perjungiklis nededamas ten, kur alternatyvos nėra arba ji beprasmė:
  `engine_hours` (motovalandos), `rim_size` / `tyre_width` (coliai jau yra
  pramonės standartas), `power_w` (buitinė galia vatais).

### 1.2 Naujas laukas

Viena eilutė `UNIT_SPECS` lentelėje `static/js/unit_toggle.js` + `data-unit-field`
šablone. Raktas paprastai sutampa su lauko `name`, bet neprivalo — `name` imamas
iš paties atributo, todėl galima ir taip:

```html
{# engine_capacity šioje formoje saugomas cm³, ne litrais #}
<input type="number" name="engine_capacity" data-unit-field="engine_capacity_cc" ...>
```

### 1.3 Konversijos (visos vienoje vietoje)

| Kanoninis | Alt | Santykis |
|---|---|---|
| kW | HP | `× 1.34102` |
| km, km/h | mi, mph | `× 0.62137` |
| kg | lbs | `× 2.20462` |
| L | cm³ | `× 1000` |
| cm³ | ci | `× 0.0610237` |
| m | ft | `× 3.28084` |
| mm | in | `× 0.0393701` |
| m² | ft² | `× 10.7639` |
| m³ | ft³ | `× 35.3147` |
| L | gal (US) | `× 0.264172` |
| l/100km | mpg | `235.215 /` (atvirkštinė) |

`1 kW = 1.34102 HP` naudojamas **visame projekte** — formose, paieškoje ir
skelbimo peržiūroje. Nemaišyti su `1.35962` (PS/AG).

### 1.4 Senoji rankinė sistema

Liko dvi vietos su savo kodu:

* `listing_create.html` ir `listing_create_cars_quick.html` — automobilių vedlys.
  Perjungikliai ten susipynę su autosave, `step3_partial` atkūrimu ir privalomų
  laukų validacija, todėl perkelti reikia atskiro, atidaus praėjimo.
* `trucks_listing_create.html` — savas `UNIT_CONFIG` (10 laukų). Veikia gerai;
  perkėlimas būtų tvarkymasis, ne taisymas.

**Naujose formose šio kodo nekartoti** — naudoti `data-unit-field`.

### 1.5 Testai

`node docs/unit_toggle_tests.js` (reikia `npm i jsdom`).

### ⚠️ KODĖL INLINE STYLES?

Mygtukus skriptas piešia inline stiliais, nes Tailwind `bg-primary` klasė
nesirenderina be `npm run start` (PostCSS rebuild). Inline
`style="background-color: #374151"` veikia VISADA, be CSS build'o.

---

## 2. INPUT FIELDS (be unit toggle)

### 2.1 Price input

```html
<div data-field-wrap="price">
    <label class="block text-sm font-medium text-gray-700 mb-2">
        Price ($) <span class="text-red-500">*</span>
    </label>
    <div class="relative max-w-xs">
        <span class="absolute left-3 top-2.5 text-gray-500">$</span>
        <input type="number" name="price" min="0" step="1" required
               value="{% if draft.price %}{{ draft.price|floatformat:0 }}{% endif %}"
               placeholder="0" class="w-full pl-8 pr-3 py-2.5 border border-gray-300 rounded-lg">
    </div>
    <input type="hidden" name="currency" value="USD">
</div>
```

**Taisyklės:** Tik USD `$`, `step=1` (no cents), `floatformat:0` template'e.

### 2.2 Phone input

Pre-fill iš `user.profile.phone_number`. Po publish save'inamas atgal į profile per `finalize_listing_publish()` helper'į.

```html
<input type="tel" name="phone" required value="{{ user_phone }}">
```

---

## 3. SELECT BUTTONS / LIST ITEMS

### 3.1 Button-style choice (mažam choice'ų skaičiui)

```html
<div data-field-wrap="condition">
    <label class="block text-sm font-medium text-gray-700 mb-2">
        Condition <span class="text-red-500">*</span>
    </label>
    <div class="flex flex-wrap gap-2">
        {% for value, label in form.condition.field.choices %}{% if value %}
        <button type="button" onclick="selectBtn(this, 'condition', '{{ value }}')"
                class="btn-choice px-4 py-2 border border-gray-200 rounded-lg text-sm text-gray-700 hover:border-gray-400 transition-all">{{ label }}</button>
        {% endif %}{% endfor %}
    </div>
    <input type="hidden" name="condition" id="condition_input">
</div>
```

**JS:**
```javascript
function selectBtn(btn, field, value) {
    btn.closest('div').querySelectorAll('.btn-choice').forEach(function(b) { b.classList.remove('active'); });
    btn.classList.add('active');
    document.getElementById(field + '_input').value = value;
    markFieldError(field, false);
}
```

**CSS:**
```css
.btn-choice.active {
    border-color: #374151;
    color: #ffffff;
    background-color: #374151;
    font-weight: 500;
}
```

### 3.2 Vertical list-style choice (didesnis choice'ų skaičiui)

```html
<div class="border border-gray-200 rounded-lg overflow-y-auto" style="max-height: 180px;">
    {% for value, label in form.body_type.field.choices %}{% if value %}
    <div onclick="selectList(this, 'body_type', '{{ value }}')"
         class="list-item px-4 py-2.5 cursor-pointer hover:bg-gray-100 border-b border-gray-100 text-sm text-gray-700">{{ label }}</div>
    {% endif %}{% endfor %}
</div>
```

CSS active state: `background-color: #374151; color: #ffffff;`

---

## 4. VALIDATION & ERROR HIGHLIGHTING

### 4.1 Field error highlighting (red border + bg + label)

**HTML wrap:**
```html
<div data-field-wrap="city">
    <label>City <span class="text-red-500">*</span></label>
    <input name="city" required>
    <p class="field-error-msg hidden mt-1 text-xs text-red-600">This field is required</p>
</div>
```

**CSS:**
```css
[data-field-wrap].field-error input,
[data-field-wrap].field-error select,
[data-field-wrap].field-error textarea {
    border-color: #ef4444 !important;
    background-color: #fef2f2 !important;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15) !important;
}
[data-field-wrap].field-error label { color: #dc2626 !important; }
```

**JS:**
```javascript
function markFieldError(fieldName, hasError) {
    var wrap = document.querySelector('[data-field-wrap="' + fieldName + '"]');
    if (wrap) wrap.classList.toggle('field-error', hasError);
}
```

### 4.2 Error banner viršuje + scroll

JS pattern'as: `showStepErrors(N, errors)` + `scrollToFirstError()`.

### 4.3 Form rules

- Form'a turi `novalidate` atributą — JS perima validation
- Klaidos VIRŠUJE banner'e + ant pačių laukų
- Po pakeitimo lauke — error highlight pradingsta

### 4.4 ⚠️ Form widget vs plain HTML input

**Visada naudoti plain HTML input'us pagrindiniam contact laukam** (phone, email, city, state):

❌ NETINKA:
```html
{{ form.phone }}
{{ form.email }}
{{ form.city }}
```

✅ TINKA:
```html
<input type="tel" name="phone" required value="{{ user.profile.phone_number|default:'' }}">
<input type="email" name="email" value="{{ user.email|default:'' }}">
<input type="text" name="city" value="{{ listing.city|default:'' }}">
```

**Priežastis:** Django form widget'ai kartais nepre-fill'ina value tinkamai (initial dict
neveikia kai form.is_bound=True), o plain HTML su Django context'u veikia visada.

---

## 5. NOTIFICATIONS

### NO toast notifications — NIEKADA

```javascript
function showAutosaveStatus(msg, isError) {
    // No-op — silent saves per user request
}
```

Inline messages tik puslapio viršuje per Django messages framework.

---

## 6. UNITS & FORMATS

| Type | Format | Pavyzdys |
|------|--------|----------|
| Currency | `$` USD prefix only | `$22,222` |
| Date | `m/Y` su nuliais | `05/2026` |
| Months | `01-12` | `01, 02, ... 12` |

### 6.3 Dual-unit display detail puslapyje

Listing detail VISADA rodoma abu vienetai:
- Mileage: `150,000 km / 93,206 mi`
- Weight: `1500 kg / 3307 lbs`
- Power: `110 kW / 150 HP`
- Length: `4500 mm / 14.8 ft`

---

## 7. PHOTO UPLOAD

- AJAX immediate upload
- Drag-drop reorder
- Click-to-lightbox
- Max: 40 (Cars), 36 (kt)
- Max file: 20MB
- First photo automatiškai `is_main=True` (žalia "MAIN" badge)
- Likę: numerėliai 1, 2, 3...

Grid: `grid grid-cols-3 md:grid-cols-5 gap-3` (Cars), `md:grid-cols-6` (kt).

AJAX endpoints:
- Upload draft: `POST /ajax/upload-X-image/`
- Delete: `POST /ajax/delete-X-image/<pk>/`
- Reorder: `POST /ajax/reorder-X-images/`
- Edit (active): `POST /ajax/upload-X-edit-image/<pk>/`

### 7.1 Edit mode photo upload (NEW 2026-05-05)

Edit mode'e nuotraukos uploadinamos į esamą listing'ą per AJAX, ne kartu su Save Changes.

**AJAX endpoint'ai (Cars Edit mode):**
- Upload: `POST /ajax/upload-listing-images/<pk>/` → views.upload_listing_images_ajax
- Reorder: `POST /ajax/reorder-listing-images/<pk>/` → views.reorder_listing_images_ajax
- Rotate: `POST /ajax/rotate-listing-image/<pk>/` → views.rotate_listing_image_ajax (PIL Image, 90° cw/ccw)
- Delete: `POST /listings/image/<pk>/delete/` → image_delete (esamas)
- Set main: `POST /listings/image/<pk>/set-main/` → image_set_main (esamas)

**Frontend pattern:** addFiles() funkcija turi šaką `if (IS_EDIT_MODE) { uploadPhotosToEditListing(files); return; }`.

### 7.2 ⛔ NEVER nest <form> inside main form

Photo grid'e kiekviena `<form action="image_set_main">` ar `<form action="image_delete">`
INDIVIDUALI BUVO NUTRAUKDAVO main form'ą prie pirmojo `</form>` tag'o. Browser'is uždarydavo
quickForm anksčiau laiko, todėl phone/state/city laukai nepatekdavo į POST.

✅ **Sprendimas:** Visi photo action'ai per `<button type="button" onclick="setExistingImageMain(N)">`
+ AJAX fetch. NIEKADA nedek `<form>` formos viduje.

### 7.3 Drag & drop reorder pattern (Edit mode)

`<div class="existing-photo" draggable="true" data-existing-img-id="N">` + 5 event handlers:
dragstart/dragend/dragover/dragleave/drop. Po drop: refreshExistingPhotoBadges()
(updates MAIN/order labels) → saveExistingPhotoOrder() (POST /ajax/reorder-listing-images/).

---

## 8. CITY / LOCATION

### 8.1 City required globally — visose kategorijose

### 8.2 State pattern (US only)

- Country dropdown'as turi tik US (LT, LV, etc. paliktos ateičiai)
- State dropdown'as matomas tik kai country=US
- State required tik kai country=US
- **Naujose kategorijose:** city VISADA matomas, state matomas tik kai country=US

```javascript
function onCountryChange() {
    var country = document.getElementById('id_country');
    var stateW = document.getElementById('stateWrapper');
    if (country.value === 'US') {
        stateW.classList.remove('hidden');
    } else {
        stateW.classList.add('hidden');
    }
}
```

### 8.3 Listing detail Location card (2x2 grid + integrated map)

Žiūr.: `templates/listings/listing_detail.html` Location section.

- **Header:** Title kairėje + `[Directions] [Open in Maps]` mygtukai dešinėje
- **2x2 grid:** Country | State / City | Address (su ikonom)
- **Map:** `h-72 w-full` integruotas Location card apačioje
- **Floating coordinates card:** apatinėje kairėje su copy-to-clipboard mygtuku
- **"Approximate area only" badge:** jei `hide_exact_address`

---

## 9. EDIT MODE PATTERN

### 9.1 Single template, dual mode

Tas pats template'as veikia ir CREATE, ir EDIT. Skiriama `is_edit_mode` flag'u.

```python
# CREATE
context = {'draft': draft, ...}

# EDIT
context = {
    'listing': listing,
    'draft': listing,
    'is_edit_mode': True,
}
```

### 9.2 Mygtukų stilius

| Režimas | Spalva | Tekstas | Ikona |
|---------|--------|---------|-------|
| Create | `bg-green-600` | "Publish Listing" | `fa-check` |
| Edit (Cars) | `bg-primary` | "Save" | `fa-save` |
| Edit (kt) | `bg-blue-600` | "Save Changes" | `fa-save` |

### 9.3 Disabled fields edit mode'e

Cars edit — Brand, Model, First Registration, VIN yra read-only (disabled).

### 9.4 Year dropdown CREATE vs EDIT

⚠️ **SVARBU:** Year selektuotas TIK edit mode'e. CREATE mode'e — placeholder'is.

```html
<option value="{{ y }}" {% if is_edit_mode and draft.year == y %}selected{% endif %}>{{ y }}</option>
```

Be `is_edit_mode and` — naujas draft'as visada selektuotų `2026` (kuris saugomas DB kuriant draft'ą).

---

## 10. CATEGORY EDIT REDIRECTS

`apps/listings/views.py` 4 funkcijos turi redirect'ų bloką pradžioje:
- `listing_edit_hub`
- `listing_edit`
- `listing_edit_section`
- `listing_edit_step`

```python
if listing.vehicle_type and listing.vehicle_type.slug == 'trucks':
    return redirect('trucks_listing_edit', pk=pk)
if listing.subcategory and listing.subcategory.slug == 'whole-car-for-parts':
    return redirect('car_for_parts_edit', pk=pk)
```

---

## 11. DRAFT SESSION PATTERN

### 11.1 Naujas listing → draft į DB

1. Sukuriamas Listing su `status='draft'`
2. Draft pk save'inamas į session: `request.session['active_X_draft_id']`
3. Visi formų autosave'ai pildo šitą draft'ą
4. Galiausiai per `finalize_listing_publish()` helper'į → status='active'

### 11.2 Session keys

- Cars: `active_cars_draft_id`
- Motorcycles: `active_moto_draft_id`
- Trucks: `active_trucks_draft_id`
- Moto Gear: `active_motogear_draft_id`
- Car-for-parts: `active_car_for_parts_draft_id`

### 11.3 `?new=1` reset rule

```python
if request.GET.get('new') == '1' and request.method == 'GET':
    request.session[SESSION_KEY] = None
```

⚠️ **WARNING:** Be `request.method == 'GET'`, POST'as su `?new=1` URL'e išvalys session ir form'os duomenys neišsisaugos!

### 11.4 KRITIŠKA: save() PRIEŠ activate()

`activate()` naudoja `update_fields=['status', 'activated_at', ...]` ir IGNORUOJA visus kitus laukų pakeitimus!

✅ **Helper'is `finalize_listing_publish()` automatiškai daro tai.** Tu rankiniu būdu šito niekada nerašyk.

---

## 12. COLOR PALETTE

| Spalva | Hex | Use case |
|--------|-----|----------|
| Primary (dark gray) | `#374151` | Active button, focus border |
| Light gray | `#6b7280` | Inactive button text |
| Border gray | `#d1d5db` | Default border |
| Success | `#16a34a` (`bg-green-600`) | Publish, MAIN photo badge |
| Save / Info | `#2563eb` (`bg-blue-600`) | Save Changes button |
| Error | `#ef4444` (`text-red-600`) | Validation errors |
| Subtle bg | `#f9fafb` (`bg-gray-50`) | Forms, disabled fields |

> ⚠️ Jei naudoji `bg-primary`, reikalingas Tailwind rebuild (`npm run start`). Saugiau — inline `style="background-color: #374151"`.

---

## 13. CODE EDITING RULE

Find & Replace formatas Zed Editor:
- **OLD:** kodas kurį reikia pakeisti
- **NEW:** kodas kuriuo pakeisti

VENGTI Markdown ` ``` ` blokų — sugadina indentaciją kopijuojant.

---

## 14. FILE LOCATIONS

- Project root: `C:\Users\user\Desktop\programos\sellcar\`
- Listings app: `apps/listings/`
- Templates: `templates/listings/`
- Helpers: `apps/listings/listing_helpers.py`
- VPS: `45.14.194.139`

---

## 15. KATEGORIJŲ MAP

| Kategorija | Vehicle Type slug | Subcategory slug | View prefix | Template | Layout |
|-----------|-------------------|------------------|-------------|----------|--------|
| Cars | `cars` | NULL ar subcategory | `listing_*` | `listing_create.html` | 7-step wizard'as su autosave |
| Motorcycles | `motorcycles` | NULL | `motorcycle_*` | `motorcycle_listing_create.html` | Single page |
| Moto Gear | `motorcycles` | helmets/boots/etc. | `motogear_*` | `motogear_listing_create.html` | Single page |
| Trucks | `trucks` | NULL | `trucks_*` | `trucks_listing_create.html` | Single page (autoplius 8x4) |
| Car for parts | `parts` | `whole-car-for-parts` | `car_for_parts_*` | `car_for_parts_create.html` | Single page (autogidas style) |

---

## 17. PENDING / FUTURE PATTERNS

- [ ] Unified Stripe payment integration
- [ ] Dark mode (variant B)
- [ ] Pricing plans (3 packages: 30d/60d/90d)
- [ ] Add-ons (iškėlimas $0.99/$1.99)
- [ ] Reminder cron via Windows Task Scheduler
- [ ] Cars-for-parts browse page (atskira `/browse/cars-for-parts/`)
- [ ] **Refactor'inti Cars/Trucks/Motorcycles/Moto Gear views į helper'ius** (dabar tik car-for-parts naudoja)

---

## 18. ⭐ ADVANCED SEARCH — MULTI BRAND+MODEL PATTERN (2026-05-06)

> **Šaltinis:** `templates/listings/advanced_search.html` Cars sekcija.
>
> **Tikslas:** Vartotojas gali filtruoti pagal kelias Brand+Model poras vienu metu. Naudoti VISOMS kategorijoms (Cars, Motorcycles, Trucks, Boats, Vans).

### 18.1 Layout — autogidas-style 3-column grid

```html
<div class="adv-grid3">  <!-- grid-template-columns: 1fr 1fr 1fr -->
    <!-- Row 1: Brand + Model + "+ Add more" link -->
    <div class="adv-field">
        <label>Brand</label>
        <div id="bmRowsContainer">
            <select class="adv-select bm-brand" onchange="bmLoadModels(this, 0)">
                <option value="">All</option>
                {% for brand in brands %}
                <option value="{{ brand.id }}" data-name="{{ brand.name }}">{{ brand.name }}</option>
                {% endfor %}
            </select>
        </div>
    </div>
    <div class="adv-field">
        <label>Model</label>
        <select class="adv-select bm-model" disabled>
            <option value="">All</option>
        </select>
    </div>
    <div class="adv-field" style="justify-content:center; padding-top:18px;">
        <a class="bm-add-link" onclick="bmAddRow()" style="padding-top:0;">
            <i class="fas fa-plus" style="font-size:0.65rem;"></i> Add more brands/models
        </a>
    </div>

    <!-- Extra brand/model rows go here (display:contents = grid items flow into parent grid) -->
    <div id="bmExtraRows" style="grid-column: 1 / -1; display: contents;"></div>

    <!-- ⚠️ KRITIŠKA: Year MUST start from column 1 to break grid auto-flow -->
    <div class="adv-field" style="grid-column-start: 1;">
        <label>Year</label>
        ...
    </div>
    <!-- ... kiti laukai ... -->
</div>
```

### 18.2 JS — bmAddRow funkcija (PIRMA EILĖ + EXTRA EILĖS)

**3 grid items per extra row:** Brand (col 1) + Model (col 2) + × Remove (col 3 — paslėptas iš dešinės)

```javascript
var bmRowCounter = 1;

function bmAddRow(brandIdToSelect, modelIdToSelect) {
    var container = document.getElementById('bmExtraRows');
    if (!container) return;
    var idx = bmRowCounter++;

    // Brand wrap (column 1 — gridColumnStart force'inamas)
    var brandWrap = document.createElement('div');
    brandWrap.className = 'adv-field bm-extra-pair';
    brandWrap.dataset.rowIdx = idx;
    brandWrap.style.gridColumnStart = '1';

    // Model wrap (column 2)
    var modelWrap = document.createElement('div');
    modelWrap.className = 'adv-field bm-extra-pair';
    modelWrap.dataset.rowIdx = idx;
    modelWrap.style.gridColumnStart = '2';

    // Remove × wrap (column 3) — paslėptas dešinėje
    var removeWrap = document.createElement('div');
    removeWrap.className = 'adv-field bm-extra-pair';
    removeWrap.dataset.rowIdx = idx;
    removeWrap.style.gridColumnStart = '3';
    removeWrap.style.display = 'flex';
    removeWrap.style.alignItems = 'flex-end';
    removeWrap.style.justifyContent = 'flex-start';

    var firstSelect = document.querySelector('.bm-brand');
    var brandOptionsHtml = firstSelect ? firstSelect.innerHTML : '<option value="">All</option>';

    brandWrap.innerHTML =
        '<label>Brand</label>' +
        '<select class="adv-select bm-brand" onchange="bmLoadModels(this, ' + idx + ')">' + brandOptionsHtml + '</select>';

    modelWrap.innerHTML =
        '<label>Model</label>' +
        '<select class="adv-select bm-model" disabled>' +
            '<option value="">All</option>' +
        '</select>';

    removeWrap.innerHTML =
        '<button type="button" onclick="bmRemoveExtraRow(' + idx + ')" title="Remove" ' +
        'style="background:none;border:none;color:#dc2626;cursor:pointer;font-size:1.5rem;line-height:36px;padding:0 8px;height:36px;font-weight:700;">×</button>';

    container.appendChild(brandWrap);
    container.appendChild(modelWrap);
    container.appendChild(removeWrap);

    // Pre-select brand+model jei restoring iš URL
    if (brandIdToSelect) {
        var brandSel = brandWrap.querySelector('.bm-brand');
        brandSel.value = brandIdToSelect;
        var modelSel = modelWrap.querySelector('.bm-model');
        modelSel.disabled = false;
        fetch('/ajax/get-models/?brand_id=' + brandIdToSelect)
            .then(function(r) { return r.json(); })
            .then(function(data) {
                modelSel.innerHTML = '<option value="">All</option>';
                data.forEach(function(item) {
                    if (item.type !== 'model') return;
                    var opt = document.createElement('option');
                    opt.value = item.model_id;
                    opt.textContent = item.name;
                    opt.dataset.name = item.name;
                    if (modelIdToSelect && String(item.model_id) === String(modelIdToSelect)) opt.selected = true;
                    modelSel.appendChild(opt);
                });
            });
    }
}

function bmRemoveExtraRow(idx) {
    document.querySelectorAll('.bm-extra-pair[data-row-idx="' + idx + '"]').forEach(function(el) {
        el.remove();
    });
}

function bmLoadModels(brandSel, rowIdx) {
    var modelSel;
    if (rowIdx === 0 || brandSel.parentElement.id === 'bmRowsContainer') {
        // First row — model is sibling at top of grid
        modelSel = document.querySelector('.adv-grid3 > .adv-field .bm-model');
        if (!modelSel) modelSel = document.querySelector('.bm-model');
    } else {
        // Extra row — find by data-row-idx
        var pair = document.querySelector('.bm-extra-pair[data-row-idx="' + rowIdx + '"] .bm-model');
        if (pair) modelSel = pair;
    }
    var brandId = brandSel.value;
    if (!modelSel) return;
    modelSel.innerHTML = '<option value="">All</option>';
    if (!brandId) {
        modelSel.disabled = true;
        return;
    }
    modelSel.disabled = false;
    fetch('/ajax/get-models/?brand_id=' + brandId)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            data.forEach(function(item) {
                if (item.type !== 'model') return;
                var opt = document.createElement('option');
                opt.value = item.model_id;
                opt.textContent = item.name;
                opt.dataset.name = item.name;
                modelSel.appendChild(opt);
            });
        });
}
```

### 18.3 prepareSubmit() — surinkti pair= URL params

```javascript
function prepareSubmit() {
    var bmInputs = document.getElementById('bmInputs');
    if (bmInputs) {
        bmInputs.innerHTML = '';
        // First row
        var firstBrand = document.querySelector('#bmRowsContainer .bm-brand');
        var firstModel = document.querySelector('.adv-grid3 > .adv-field .bm-model');
        if (firstBrand && firstBrand.value) {
            var brandId = firstBrand.value;
            var brandName = firstBrand.selectedOptions[0].dataset.name || firstBrand.selectedOptions[0].textContent;
            var modelId = (firstModel && firstModel.value) ? firstModel.value : '';
            var modelName = modelId ? (firstModel.selectedOptions[0].dataset.name || firstModel.selectedOptions[0].textContent) : '';
            var inp = document.createElement('input');
            inp.type = 'hidden'; inp.name = 'pair';
            inp.value = brandId + '|' + brandName + '|' + modelId + '|' + modelName;
            bmInputs.appendChild(inp);
        }
        // Extra rows
        var extraIndices = new Set();
        document.querySelectorAll('.bm-extra-pair').forEach(function(el) {
            extraIndices.add(el.dataset.rowIdx);
        });
        extraIndices.forEach(function(idx) {
            var brandSel = document.querySelector('.bm-extra-pair[data-row-idx="' + idx + '"] .bm-brand');
            var modelSel = document.querySelector('.bm-extra-pair[data-row-idx="' + idx + '"] .bm-model');
            if (!brandSel || !brandSel.value) return;
            var brandId = brandSel.value;
            var brandName = brandSel.selectedOptions[0].dataset.name || brandSel.selectedOptions[0].textContent;
            var modelId = (modelSel && modelSel.value) ? modelSel.value : '';
            var modelName = modelId ? (modelSel.selectedOptions[0].dataset.name || modelSel.selectedOptions[0].textContent) : '';
            var inp = document.createElement('input');
            inp.type = 'hidden'; inp.name = 'pair';
            inp.value = brandId + '|' + brandName + '|' + modelId + '|' + modelName;
            bmInputs.appendChild(inp);
        });
    }
}
```

### 18.4 ⚠️ KRITIŠKOS pamokos (be šitų NEVEIKS)

1. **`display: contents` ant `bmExtraRows` div'o** — kitaip extra pair items neflow'ina į parent grid'ą.

2. **`gridColumnStart: 1/2/3` force'inamas kiekvienam wrapper'iui** — be to, naujos eilutės užima random pozicijas grid'e.

3. **Year (ir bet kuris laukas po `bmExtraRows`) MUST `grid-column-start: 1`** — kitaip įsisprūsta į laisvas paskutinio extra row pozicijas.

4. **Remove × wrapper'is — `display: flex; align-items: flex-end`** — kad × sutaptų vertikaliai su select'o apačia.

5. **× mygtukas: `font-size: 1.5rem; line-height: 36px; height: 36px`** — kad × būtų vertikaliai centras 36px aukščio mygtuke.

6. **"+ Add more" link wrapper'is — `justify-content: center; padding-top: 18px`** — pakelia link'ą iki select'o vidurio linijos (label height + gap kompensacija).

### 18.5 CSS reikalingas

```css
.adv-grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px 20px; }
@media (max-width: 768px) { .adv-grid3 { grid-template-columns: 1fr; } }

.adv-field { display: flex; flex-direction: column; gap: 4px; }
.adv-field label { font-size: 0.72rem; color: #6b7280; font-weight: 500; }

.adv-select, .adv-input {
    padding: 0.5rem 0.65rem;
    background: #fff;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-size: 0.82rem;
    width: 100%;
}

.bm-add-link {
    color: #f97316;          /* oranžinis (autogidas style) */
    cursor: pointer;
    font-size: 0.78rem;
    font-weight: 500;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding-top: 4px;
}
.bm-add-link:hover { color: #ea580c; }
```

### 18.6 Naujom kategorijom — kaip pritaikyti

1. **Pakeisk prefix'ą:** `bm` → `mc` (motorcycles), `tr` (trucks), `bt` (boats), `vn` (vans).
2. **Pakeisk container ID:** `bmRowsContainer` → `mcRowsContainer`, `bmExtraRows` → `mcExtraRows`.
3. **Pakeisk klasių prefix'us:** `.bm-brand` → `.mc-brand`, `.bm-model` → `.mc-model`, `.bm-extra-pair` → `.mc-extra-pair`.
4. **Pakeisk URL parametrą:** `pair` → `mc_pair` arba `tr_pair`.
5. **Brands AJAX endpoint'as:** kategorijoms su atskirom DB lentelėm (Motorcycles, Trucks) gali reikti atskiro `/ajax/get-motorcycle-models/` endpoint'o.

### 18.7 ⚠️ Pamoka: × dabartinis sprendimas vs alternatyvos

**Bandyta 3 sprendimai (per ilgą iteracijų:**

❌ × **viduje Model wrap'o** kaip `position: absolute; right: -28px` — × buvo už grid kraštų, jei Model trumpas; × išsidėstyti netvarkingai
❌ **Atskira 3-čia kolona su `align-items: flex-end + paddingTop: 18px`** — × sutapdavo per žemai, vizualiai blogai
✅ **3-čia kolona su `align-items: flex-end + height: 36px + line-height: 36px`** — × natūraliai sutampa su select bottom

**Naudoti SPRENDIMĄ #3** — testuotas ir veikia.

---

## 19. ⭐ VIN HISTORY REPORT BUTTON (2026-05-06)

> **Tikslas:** Listing detail puslapyje šalia VIN rodyti mygtuką "History report" — užveda į carfaxreport.eu su pre-filled VIN.
>
> **Cross-promotion:** SellCar lankytojai → carfaxreport.eu SaaS. Pajamų šaltinis + trust signal pirkėjams.

### 19.1 Naudoti VISOSE kategorijose

Cars, Trucks, Motorcycles, Car-for-parts, Vans, Boats — visur kur listing turi VIN lauką.

### 19.2 HTML pattern (minimalistinis — Option C)

Šalia VIN value, tame pačiame eilutėj:

```html
{% if listing.vin %}
<div class="flex justify-between py-3 border-b border-gray-200">
    <span class="text-gray-600">VIN</span>
    <span class="font-medium text-gray-900 inline-flex items-center gap-2 flex-wrap justify-end">
        {{ listing.vin }}
        <a href="https://carfaxreport.eu/?vin={{ listing.vin }}&ref=sellcar"
           target="_blank"
           rel="noopener"
           class="inline-flex items-center gap-1 px-2.5 py-1 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-medium rounded-md border border-blue-200 transition-colors"
           title="Get vehicle history report from Carfaxreport.eu">
            <i class="fas fa-shield-alt text-xs"></i>
            History report
        </a>
    </span>
</div>
{% endif %}
```

### 19.3 URL formatas