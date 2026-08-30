# Terminų žodynas (lt → en)

Vertimo šaltinis — lietuvių kalba. Šis sąrašas yra privalomas: tas pats
lietuviškas terminas visur verčiamas TUO PAČIU angliškuoju. Naujas terminas
pirmiausia įrašomas čia, tik paskui į `.po`.

## Užrakinti terminai

| Lietuviškai | English | Kur naudojama |
|---|---|---|
| Paslaugos | Services | įmonės kortelė, paieškos grupė, įmonės puslapis |
| Įmonės | Businesses | /imones/ skirtukas, paieškos grupė |
| Meistrai / Specialistai | Professionals | /imones/ perjungiklis (`?tipas=meistrai`) |
| Skelbimai | Listings | visa svetainė |
| Prekiautojas | Dealer | `Imone.tipas` |
| Servisas | Repair shop | `Imone.tipas` |
| Atsiliepimai | Reviews | kortelė, įmonės puslapis (3 etapas) |
| Bet kada | Any time | „Kada" laukas |
| Dabartinė vieta | Current location | „Kur" laukas |
| Slėpti žemėlapį | Hide map | /imones/ įrankių juosta |
| Ieškoti šioje srityje | Search this area | žemėlapio mygtukas |
| Žiūrėti visas | See all | burbulas, kortelė |

## Ko NEVERČIAM

Duomenų neverčiam — verčiam tik sąsają:

- markių ir modelių pavadinimai (`Škoda`, `Golf`),
- įmonių, meistrų ir jų paslaugų pavadinimai (juos rašo patys vartotojai),
- miestų ir adresų reikšmės,
- skelbimų antraštės ir aprašymai.

## Skaičiai ir kainos

Formatą duoda `apps/listings/formatai.py` (`sk`, `kaina`) pagal aktyvią kalbą:

| | lt | en |
|---|---|---|
| skaičius | `15 000` (nedalomas tarpas) | `15,000` |
| kaina | `5 000 €` (simbolis gale) | `€5,000` (simbolis priekyje) |

Django `lt` lokalė tūkstančius skirtų tašku (`5.000`), todėl skirtuką
nurodom patys — visa svetainė ima jį iš to vieno failo.

## Taisyklės

1. Šablonuose — `{% load i18n %}` + `{% trans %}` / `{% blocktrans %}`.
   Kintamasis eina per `{% blocktrans with … %}`, o ne klijuojant eilutes.
2. Modeliuose — `gettext_lazy as _`, rodiniuose — `gettext as _`.
3. JS eilučių nerašom: tekstai keliauja per `json_script`
   (žr. `apps/imones/views._js_tekstai`) arba `data-` atributus.
4. Naujas adresas — po `i18n_patterns` (`config/urls.py`);
   lietuviškas lieka be priešdėlio, angliškas gauna `/en/`.
5. Po kiekvieno teksto keitimo:
   `venv/bin/python manage.py makemessages -l en --ignore=venv` ir
   `compilemessages`. `fuzzy` žymų nepaliekam.
6. Sargybą laiko `apps/imones/tests.py` — žr. `scripts/patikra.sh`.
