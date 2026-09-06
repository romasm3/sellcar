# Serverio būklė

Sugeneruota: 2026-09-06 19:06:06 CEST

## Kodas

```
sukasi:      7cc1d46 fix(paieska): markių ir modelių skaičius be skliaustelių
origin/master: 7cc1d46 fix(paieska): markių ir modelių skaičius be skliaustelių
šaka:        master
darbo katalogas: švarus
```

## Servisai

```
gunicorn                 active
nginx                    active
postgresql               active
autoleft-deploy.timer    active
```

## Ar svetainė atsako

```
HTTP 301, 0.002144s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        16   MATOMAS
  expired       10   nematomas
  draft          9   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      19
  iš jų pasibaigę (expires_at praeityje): 10
  aktyvūs, baigsis per 7 d.: 6
  aktyvūs be pabaigos datos: 8 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   28G  263G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/nb/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/hu/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/pt/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/th/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/vi/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/hi/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/io/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/af/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/id/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/en/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/es_MX/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[430001]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/eu/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 19:06:03 vmi3306453 autoleft-deploy[429150]: [19:06:03] Restartinam gunicorn.service
Sep 06 19:06:05 vmi3306453 autoleft-deploy[429150]: [19:06:05] Health OK (1/10)
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] Raktai: .env — vietoje.
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] Raktai: google-translate-key.json — vietoje.
Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] === Deploy OK ===
Sep 06 19:06:06 vmi3306453 autoleft-deploy[428996]: [2026-09-06 19:06:06] ✅ Deploy OK — gyvai veikia 7cc1d46
```
