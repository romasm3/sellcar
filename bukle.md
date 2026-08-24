# Serverio būklė

Sugeneruota: 2026-08-24 12:37:30 CEST

## Kodas

```
sukasi:      3f85319 refactor(naujumas): pašalintas nebenaudojamas new_listing_ids, dienų riba iš modelio
origin/master: 3f85319 refactor(naujumas): pašalintas nebenaudojamas new_listing_ids, dienų riba iš modelio
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
HTTP 301, 0.001490s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        23   MATOMAS
  draft          9   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      12
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 12:34:53 vmi3306453 autoleft-deploy[163646]: [2026-08-24 12:34:53] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Aug 24 12:34:53 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Aug 24 12:34:53 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Aug 24 12:34:53 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:36:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164281]: [2026-08-24 12:36:09] === Naujų commit'ų rasta: d91ce8e → cd36a44 ===
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164281]: [2026-08-24 12:36:09] Nesucommit'inti pakeitimai serveryje:
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M locale/lt/LC_MESSAGES/django.mo
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M locale/lt/LC_MESSAGES/django.po
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/home.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/admin_moderate_user.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/listing_detail.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/listing_list.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/listing_list_v2.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/moto_parts_browse.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/motorcycles_advanced_search.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/motorcycles_list.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/my_listings.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/trucks_advanced_search.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164298]:      M templates/listings/trucks_list.html
Aug 24 12:36:09 vmi3306453 autoleft-deploy[164281]: [2026-08-24 12:36:09] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Aug 24 12:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Aug 24 12:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Aug 24 12:36:09 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 12:37:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
