# Serverio būklė

Sugeneruota: 2026-09-06 18:24:01 CEST

## Kodas

```
sukasi:      cfc8091 fix(paieska): markės ir modeliai su „(0)" rodomi tokiu pat ryškiu tekstu
origin/master: cfc8091 fix(paieska): markės ir modeliai su „(0)" rodomi tokiu pat ryškiu tekstu
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
HTTP 301, 0.001958s
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
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/hr/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/uk/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/ca/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/da/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/hy/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/ne/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/ar_DZ/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/gd/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/hi/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/io/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/tt/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[402105]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/es/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 06 18:23:58 vmi3306453 autoleft-deploy[401338]: [18:23:58] Restartinam gunicorn.service
Sep 06 18:24:00 vmi3306453 autoleft-deploy[401338]: [18:24:00] Health OK (1/10)
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] Raktai: .env — vietoje.
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] Raktai: google-translate-key.json — vietoje.
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401338]: [18:24:01] === Deploy OK ===
Sep 06 18:24:01 vmi3306453 autoleft-deploy[401140]: [2026-09-06 18:24:01] ✅ Deploy OK — gyvai veikia cfc8091
```
