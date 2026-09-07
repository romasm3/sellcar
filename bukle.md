# Serverio būklė

Sugeneruota: 2026-09-07 12:32:21 CEST

## Kodas

```
sukasi:      c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
origin/master: c6aa4e6 fix(nuotraukos): trynimas, pertvarkymas ir „pagrindinė" telefone; įkėlimas po vieną
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
HTTP 301, 0.433186s
```

## Skelbimų būsenos

```

Listing — iš viso 37
  active        18   MATOMAS
  expired       10   nematomas
  draft          9   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      19
  iš jų pasibaigę (expires_at praeityje): 10
  aktyvūs, baigsis per 7 d.: 5
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
/dev/sda1       291G   29G  262G  10% /
```

## Paskutinis auto-deploy

```
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/pt_BR/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/fr/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/ka/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/io/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/fi/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/sr/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/sw/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/sv/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/zh_Hant/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/gl/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/hr/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/vi/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/nl/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/sq/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/dsb/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/ckb/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083962]: File “/root/autoleft/venv/lib/python3.10/site-packages/django/contrib/sites/locale/es_MX/LC_MESSAGES/django.po” is already compiled and up to date.
Sep 07 12:32:18 vmi3306453 autoleft-deploy[1083012]: [12:32:18] Restartinam gunicorn.service
Sep 07 12:32:20 vmi3306453 autoleft-deploy[1083012]: [12:32:20] Health OK (1/10)
Sep 07 12:32:21 vmi3306453 autoleft-deploy[1083012]: [12:32:21] Statiniai OK: style.641848969862.css (manifestas atnaujintas)
Sep 07 12:32:21 vmi3306453 autoleft-deploy[1083012]: [12:32:21] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 07 12:32:21 vmi3306453 autoleft-deploy[1083012]: [12:32:21] Raktai: .env — vietoje.
Sep 07 12:32:21 vmi3306453 autoleft-deploy[1083012]: [12:32:21] Raktai: google-translate-key.json — vietoje.
Sep 07 12:32:21 vmi3306453 autoleft-deploy[1083012]: [12:32:21] === Deploy OK ===
Sep 07 12:32:21 vmi3306453 autoleft-deploy[1082841]: [2026-09-07 12:32:21] ✅ Deploy OK — gyvai veikia c6aa4e6
```
