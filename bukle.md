# Serverio būklė

Sugeneruota: 2026-08-23 13:38:01 CEST

## Kodas

```
sukasi:      55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
origin/master: 55cc9dd feat(i18n): ETAPAS 3 - vartotojo zona angliskai
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/parts_views.py
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
HTTP 301, 0.002777s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        33   MATOMAS
  draft         11   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      14
  iš jų pasibaigę (expires_at praeityje): 3
  aktyvūs, baigsis per 7 d.: 3
  aktyvūs be pabaigos datos: 16 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   14G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:05 vmi3306453 autoleft-deploy[4147727]:   No migrations to apply.
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:06 vmi3306453 autoleft-deploy[4147732]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:06 vmi3306453 autoleft-deploy[4147711]: [13:32:06] Restartinam gunicorn.service
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147711]: [13:32:07] Health OK (1/10)
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147711]: [13:32:07] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147711]: [13:32:07] === Deploy OK ===
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: Aug 23 13:32:07 vmi3306453 autoleft-deploy[4147575]: [2026-08-23 13:32:07] ✅ Deploy OK — gyvai veikia 31ee12f
Aug 23 13:32:08 vmi3306453 autoleft-deploy[4147803]: ```
Aug 23 13:32:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:32:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:32:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 8.922s CPU time.
Aug 23 13:32:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:33:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:33:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:34:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:34:05 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:34:05 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:35:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:35:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:35:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:35:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.040s CPU time.
Aug 23 13:36:50 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 23 13:36:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 23 13:36:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 23 13:38:00 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
