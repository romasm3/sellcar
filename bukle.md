# Serverio būklė

Sugeneruota: 2026-09-01 17:59:59 CEST

## Kodas

```
sukasi:      3e6b957 feat(veliava): vėliava po pavadinimo ir kortelių vietos eilutėje
origin/master: 3e6b957 feat(veliava): vėliava po pavadinimo ir kortelių vietos eilutėje
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
HTTP 301, 0.000995s
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
/dev/sda1       291G   38G  253G  13% /
```

## Paskutinis auto-deploy

```
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783807]: Running migrations:
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783807]:   No migrations to apply.
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:45 vmi3306453 autoleft-deploy[2783826]: 2 static files copied to '/root/autoleft/staticfiles', 214 unmodified.
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:46 vmi3306453 autoleft-deploy[2783481]: [17:55:46] Restartinam gunicorn.service
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:47 vmi3306453 autoleft-deploy[2783481]: [17:55:47] Health OK (1/10)
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:47 vmi3306453 autoleft-deploy[2783481]: [17:55:47] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:48 vmi3306453 autoleft-deploy[2783481]: [17:55:48] === Deploy OK ===
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: Sep 01 17:55:48 vmi3306453 autoleft-deploy[2783306]: [2026-09-01 17:55:48] ✅ Deploy OK — gyvai veikia 3e6b957
Sep 01 17:55:50 vmi3306453 autoleft-deploy[2783944]: ```
Sep 01 17:55:50 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 17:55:50 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 17:55:50 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 21.426s CPU time.
Sep 01 17:56:24 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 17:56:25 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 17:56:25 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 17:56:25 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.249s CPU time.
Sep 01 17:57:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 17:57:33 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 17:57:33 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 17:57:33 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.547s CPU time.
Sep 01 17:58:54 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 01 17:58:56 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 01 17:58:56 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 17:58:56 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.446s CPU time.
Sep 01 17:59:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
