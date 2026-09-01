# Serverio būklė

Sugeneruota: 2026-09-01 16:51:12 CEST

## Kodas

```
sukasi:      9d3bb12 feat(salies-juosta): „Visos šalys", vėliavėlė eilutėje, skaičiai iš to paties variklio
origin/master: 9d3bb12 feat(salies-juosta): „Visos šalys", vėliavėlė eilutėje, skaičiai iš to paties variklio
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
HTTP 301, 0.040679s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        19   MATOMAS
  draft          9   nematomas
  expired        7   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      16
  iš jų pasibaigę (expires_at praeityje): 7
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
/dev/sda1       291G   36G  256G  13% /
```

## Paskutinis auto-deploy

```
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:48 vmi3306453 autoleft-deploy[2731678]: Running migrations:
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:48 vmi3306453 autoleft-deploy[2731678]:   No migrations to apply.
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:48 vmi3306453 autoleft-deploy[2731701]: 3 static files copied to '/root/autoleft/staticfiles', 213 unmodified.
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:49 vmi3306453 autoleft-deploy[2731357]: [16:46:49] Restartinam gunicorn.service
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:51 vmi3306453 autoleft-deploy[2731357]: [16:46:51] Health OK (1/10)
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:51 vmi3306453 autoleft-deploy[2731357]: [16:46:51] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:51 vmi3306453 autoleft-deploy[2731357]: [16:46:51] === Deploy OK ===
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: Sep 01 16:46:51 vmi3306453 autoleft-deploy[2731204]: [2026-09-01 16:46:51] ✅ Deploy OK — gyvai veikia 9d3bb12
Sep 01 16:46:53 vmi3306453 autoleft-deploy[2731829]: ```
Sep 01 16:46:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 16:46:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 16:46:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 22.441s CPU time.
Sep 01 16:47:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 16:47:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 16:47:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 16:47:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.455s CPU time.
Sep 01 16:48:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 16:48:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 16:48:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 16:48:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.434s CPU time.
Sep 01 16:50:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 16:50:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 16:50:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 16:50:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 2.332s CPU time.
Sep 01 16:51:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
