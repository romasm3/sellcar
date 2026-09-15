# Bendros klaidos — būsenos

Liečia daugiau nei vieną kategoriją.

| Nr. | Klaida | Būsena | Commit |
|-----|--------|--------|--------|
| CFG-01 | Skelbime rodomas portalo palaikymo adresas `helpautoinfo@gmail.com` vietoj pardavėjo | IŠTAISYTA | `43cb054d6d95` |

## CFG-01 — ką radau

`helpautoinfo@gmail.com` kode yra vienoje vietoje kaip reikšmė:

```python
# config/settings.py
DEFAULT_FROM_EMAIL = config("EMAIL_USER", default="helpautoinfo@gmail.com")
```

Jokia kodo eilutė jo į `Listing.contact_email` nerašo — perėjau visus
`contact_email` priskyrimus. Pati `kontaktinis_pastas` savybė tvarkinga:
skelbimo laukas pirmas, paskyros — atsarginis; portalo adresas joje
neminimas.

Vadinasi, į skelbimą jis galėjo patekti tik kaip DUOMENYS (įvestas ar
įkeltas), o ne per kodą. Iš šio konteinerio produkcijos DB nematau, tad
patvirtinti, kaip būtent jis ten atsirado, negaliu.

## Kas padaryta

1. **Išvaloma.** Migracija `0106_kontaktai_i_skelbima` ištrina
   `contact_email`, jei jis sutampa su `DEFAULT_FROM_EMAIL`. Ištuštėjęs
   laukas reiškia, kad `kontaktinis_pastas` grąžins paskyros adresą.
2. **Neatsiras iš naujo.** Paštas, kaip ir telefonas, dabar rašomas tik į
   skelbimą iš to, ką atsiuntė forma; paskyros reikšmė naudojama tik kaip
   pradinė.
3. **Prižiūrima.** `docs/kontaktu_telefono_test.py` tikrina, kad nė
   viename skelbime nėra `DEFAULT_FROM_EMAIL`.

Jei adresas gyvai atsirastų dar kartą — tai reikštų įvedimo kelią, kurio
nerandu kode; tada reikės produkcijos DB įrašo ir laiko žymės.
