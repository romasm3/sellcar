# Serverio būklė

Sugeneruota: 2026-09-06 12:29:31 CEST

## Kodas

```
sukasi:      c24e13f fix(vertimai): atstatyti ~2830 msgid visose 13 kalbų, iškuoptos svetimos eilutės
origin/master: c24e13f fix(vertimai): atstatyti ~2830 msgid visose 13 kalbų, iškuoptos svetimos eilutės
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M locale/ar/LC_MESSAGES/django.po
   M locale/de/LC_MESSAGES/django.po
   M locale/en/LC_MESSAGES/django.po
   M locale/es/LC_MESSAGES/django.po
   M locale/et/LC_MESSAGES/django.po
   M locale/fr/LC_MESSAGES/django.po
   M locale/ko/LC_MESSAGES/django.po
   M locale/lv/LC_MESSAGES/django.po
   M locale/pl/LC_MESSAGES/django.po
   M locale/ru/LC_MESSAGES/django.po
   M locale/vi/LC_MESSAGES/django.po
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
HTTP 301, 0.002816s
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
/dev/sda1       291G   28G  264G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 12:24:31 vmi3306453 autoleft-deploy[166787]:     c24e13f fix(vertimai): atstatyti ~2830 msgid visose 13 kalbų, iškuoptos svetimos eilutės
Sep 06 12:24:31 vmi3306453 autoleft-deploy[166774]: [2026-09-06 12:24:31] Nesucommit'inti pakeitimai serveryje:
Sep 06 12:24:31 vmi3306453 autoleft-deploy[166792]:      M docs/vertimo_uzpildymas_ataskaita.txt
Sep 06 12:24:31 vmi3306453 autoleft-deploy[166774]: [2026-09-06 12:24:31] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Sep 06 12:24:31 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Sep 06 12:24:31 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Sep 06 12:24:31 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 12:25:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 12:25:51 vmi3306453 autoleft-deploy[167652]: [2026-09-06 12:25:51] === Naujų commit'ų rasta: 2649730 → c24e13f ===
Sep 06 12:25:51 vmi3306453 autoleft-deploy[167668]:     c24e13f fix(vertimai): atstatyti ~2830 msgid visose 13 kalbų, iškuoptos svetimos eilutės
Sep 06 12:25:51 vmi3306453 autoleft-deploy[167652]: [2026-09-06 12:25:51] Nesucommit'inti pakeitimai serveryje:
Sep 06 12:25:51 vmi3306453 autoleft-deploy[167673]:      M docs/vertimo_uzpildymas_ataskaita.txt
Sep 06 12:25:51 vmi3306453 autoleft-deploy[167652]: [2026-09-06 12:25:51] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Sep 06 12:25:51 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Sep 06 12:25:51 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Sep 06 12:25:51 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 12:26:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 12:27:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 12:27:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 12:27:05 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.554s CPU time.
Sep 06 12:28:15 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 12:28:17 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 12:28:17 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 12:28:17 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.499s CPU time.
Sep 06 12:29:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
