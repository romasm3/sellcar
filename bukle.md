# Serverio būklė

Sugeneruota: 2026-09-01 19:56:08 CEST

## Kodas

```
sukasi:      9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
origin/master: 9f0c6aa fix(pastas): laiškai iškelti iš užklausos į foną
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
HTTP 301, 0.001757s
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
/dev/sda1       291G   44G  247G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869604]: [19:50:57] Health OK (1/10)
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869604]: [19:50:57] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869604]: [19:50:57] === Deploy OK ===
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: Sep 01 19:50:57 vmi3306453 autoleft-deploy[2869434]: [2026-09-01 19:50:57] ✅ Deploy OK — gyvai veikia 9f0c6aa
Sep 01 19:51:00 vmi3306453 autoleft-deploy[2870169]: ```
Sep 01 19:51:00 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:51:00 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:51:00 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 22.979s CPU time.
Sep 01 19:51:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:51:26 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:51:26 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:51:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.382s CPU time.
Sep 01 19:52:45 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:52:48 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:52:48 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:52:48 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.700s CPU time.
Sep 01 19:53:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:53:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:53:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:53:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.448s CPU time.
Sep 01 19:55:05 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 19:55:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 19:55:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 19:55:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.865s CPU time.
Sep 01 19:56:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
