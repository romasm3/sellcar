# Geokodavimas — Photon + Nominatim (OpenStreetMap)

Skelbimo vietą nurodo pats pardavėjas: įrašo adresą (siūlymai rašant)
arba pasistato žymeklį žemėlapyje. Saugom adreso tekstą, koordinates,
miestą ir šalį.

## Kodėl OSM, o ne Google/Mapbox

| | Autocomplete | Geokodavimas | Ar galima **saugoti** koordinates |
|---|---|---|---|
| Google Maps | $2,83/1 000 (10 k nemokamai) | $5,00/1 000 (10 k nemokamai) | **Ne** — tik laikinas kešas |
| Mapbox | seansais | Temporary $1,70/1 000 (100 k nemokamai) · Permanent $5,00/1 000 nuo pirmos | tik per Permanent (mokama) |
| **Photon + Nominatim (OSM)** | nemokama | nemokama | **Taip** (ODbL, su nuoroda) |

Lemiamas argumentas ne kaina, o teisė laikyti lat/lng duomenų bazėje —
be to mūsų žemėlapio paieška neveiktų.

## Taisyklės, kurių laikomės

* **Nuoroda „© OpenStreetMap"** rodoma visur, kur naudojami jų duomenys:
  kūrimo formos žemėlapyje, skelbimo puslapio žemėlapyje ir žemėlapio
  paieškoje. Tai licencijos reikalavimas.
* **Nominatim riba — 1 užklausa/sek.**, programiniai srautai atgrasomi,
  todėl: atvirkštinis geokodavimas kviečiamas tik PALEIDUS žymeklį, su
  300 ms atidėjimu; atsakymai kešuojami serveryje 30 parų; siunčiam
  `User-Agent: AutoLeft/1.0 (https://autoleft.com; helpautoinfo@gmail.com)`.
* Naršyklė į OSM nesikreipia tiesiogiai — viskas eina per mūsų galus
  (`/ajax/adresai/`, `/ajax/vieta/`), todėl dažnį ir kešą valdom mes.

## Kiek užklausų išeina įvedant vieną adresą

| Veiksmas | Užklausų |
|---|---|
| Rašant adresą (Photon, 300 ms atidėjimas, ~20 ženklų) | 3–5 |
| Pasirinkus siūlymą | 0 (koordinatės ateina kartu su siūlymu) |
| Patempus žymeklį (Nominatim, tik paleidus) | 1 už kiekvieną paleidimą |
| Pakartotinai tas pats adresas / taškas | 0 (kešas 30 parų) |

Iš viso vienam skelbimui — **apie 4–6 užklausas**.

## Kada kelti Photon pas save

Photon leidžia pasikelti savo serverį (github.com/komoot/photon).
Verta tai daryti pasiekus **~2 000 skelbimų per mėnesį** (≈10 000
užklausų): tada dingsta ir viešo serverio ribos, ir priklausomybė nuo
svetimos infrastruktūros. Indeksui reikia ~200 GB disko Europai.

Tiekėjas keičiamas vienoje vietoje — `GEO_TIEKEJAS`
(`apps/listings/geokodavimas.py`).

## Jei geokodavimas neveikia

Forma veikia toliau: siūlymų nerodoma, bet adresą galima įrašyti ranka,
o žymeklį pastatyti paspaudus žemėlapį. Skelbimo kūrimas nesustoja.

## Seni skelbimai

Skelbimai, sukurti anksčiau, koordinates turi ne iš žymeklio, o pagal
miestą — jiems `koordinates_tikslios = False` ir žemėlapyje rodomas
~1,5 km apskritimas su žyma „Vieta apytikslė — pagal miestą".
Redaguojant tokį skelbimą pardavėjui rodomas kvietimas patikslinti.
