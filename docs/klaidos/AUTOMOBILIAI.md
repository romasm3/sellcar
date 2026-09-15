# Automobiliai — klaidų būsenos

Keliai: `/create/cars/quick/`, `/create/` (pilna forma), `/<id>/`.

Patikra: `python docs/kontaktu_telefono_test.py` (32 patikros).

| Nr. | Klaida | Būsena | Commit |
|-----|--------|--------|--------|
| CAR-12 | Telefono numeris saugomas prie paskyros, ne prie skelbimo: pakeitus jį viename skelbime, tyliai pasikeičia visuose kituose | IŠTAISYTA | `PLACEHOLDER` |

## CAR-12 — ką radau

`Listing` **neturėjo telefono lauko visai**. Kiekviena forma rašė

```python
request.user.profile.phone_number = phone_val
request.user.profile.save(update_fields=['phone_number'])
```

o skelbimo puslapis rodė `listing.seller.profile.phone_number`. Vienas
laukas visiems žmogaus skelbimams — todėl #821–#825 ėmė rodyti tą patį
paskutinį įrašytą numerį, nors kaina ir miestas liko savi.

Ratlankiai ir padangos (`WheelListing`) savo `contact_phone` turėjo nuo
pradžių, todėl `/wheels/26/edit/` veikė teisingai. Pagal juos ir
sutvarkytos visos kitos kategorijos.

## Kas pakeista

* `Listing.contact_phone` (migracija `0105`) ir savybė
  `kontaktinis_telefonas` — skelbimo numeris pirmas, paskyros atsarginis.
* `apps/listings/kontaktai.py`: `issaugok_telefona()` ir
  `telefono_reiksme()` — tikslūs `issaugok_pasta()` / `pasto_reiksme()`
  atitikmenys. Paskyros jos neliečia.
* Visos 21 vietos, kurios rašė numerį į paskyrą, dabar rašo į skelbimą.
* 25 kūrimo šablonai ima numerį iš skelbimo, paskyros — tik kaip pradinę
  reikšmę.
* Skelbimo puslapis ir `/<id>/telefonas/` rodo skelbimo numerį. Jungiklis
  „rodyti numerį" lieka paskyroje — jis apie žmogų, ne apie skelbimą.
* Migracija `0106` visiems esamiems skelbimams įrašo savininko paskyros
  numerį, tad rodoma reikšmė nepasikeitė.

## Patikrinta

```
#1 Biella   +39 000 000001     #2 Madridas +34 000 000002
#1 pakeistas į +33 000 000003
  → #1 = +33 000 000003
  → #2 = +34 000 000002   (nepakitęs)
  → paskyra = +370 601 00000 (nepakitusi)
paskyros numeris pakeistas į +370 699 99999
  → abu skelbimai nepakitę
```
