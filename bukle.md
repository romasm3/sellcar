# Serverio būklė

Sugeneruota: 2026-08-24 11:39:27 CEST

## Kodas

```
sukasi:      cd36a44 merge: master (išsaugotų skelbimų pastabos)
origin/master: cd36a44 merge: master (išsaugotų skelbimų pastabos)
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
HTTP 301, 0.001088s
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
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   15G  277G   5% /
```

## Paskutinis auto-deploy

```
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: Aug 24 11:33:39 vmi3306453 autoleft-deploy[145663]: 0 static files copied to '/root/autoleft/staticfiles', 140 unmodified.
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: Aug 24 11:33:39 vmi3306453 autoleft-deploy[145638]: [11:33:39] Restartinam gunicorn.service
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: Aug 24 11:33:40 vmi3306453 autoleft-deploy[145638]: [11:33:40] Health OK (1/10)
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: Aug 24 11:33:40 vmi3306453 autoleft-deploy[145638]: [11:33:40] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: Aug 24 11:33:41 vmi3306453 autoleft-deploy[145638]: [11:33:41] === Deploy OK ===
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: Aug 24 11:33:41 vmi3306453 autoleft-deploy[145558]: [2026-08-24 11:33:41] ✅ Deploy OK — gyvai veikia cd36a44
Aug 24 11:33:42 vmi3306453 autoleft-deploy[145757]: ```
Aug 24 11:33:42 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:33:42 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:33:42 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 7.967s CPU time.
Aug 24 11:34:56 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:34:58 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:34:58 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:34:58 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.022s CPU time.
Aug 24 11:36:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:36:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:36:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.027s CPU time.
Aug 24 11:37:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:37:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:37:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:38:20 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 24 11:38:22 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 24 11:38:22 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 24 11:39:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
