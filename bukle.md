# Serverio būklė

Sugeneruota: 2026-09-02 09:36:02 CEST

## Kodas

```
sukasi:      9a1bfe7 fix(deploy): kritęs deploy'as nebekartojamas kas minutę
origin/master: 9a1bfe7 fix(deploy): kritęs deploy'as nebekartojamas kas minutę
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
HTTP 301, 0.002979s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        18   MATOMAS
  draft          9   nematomas
  expired        8   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      17
  iš jų pasibaigę (expires_at praeityje): 8
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
/dev/sda1       291G   47G  245G  16% /
```

## Paskutinis auto-deploy

```
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:24 vmi3306453 autoleft-deploy[3475772]:   No migrations to apply.
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:25 vmi3306453 autoleft-deploy[3475795]: 0 static files copied to '/root/autoleft/staticfiles', 217 unmodified, 125 post-processed.
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:25 vmi3306453 autoleft-deploy[3475390]: [09:31:25] Restartinam gunicorn.service
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:27 vmi3306453 autoleft-deploy[3475390]: [09:31:27] Health OK (1/10)
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475390]: [09:31:28] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475390]: [09:31:28] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475390]: [09:31:28] === Deploy OK ===
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: Sep 02 09:31:28 vmi3306453 autoleft-deploy[3475238]: [2026-09-02 09:31:28] ✅ Deploy OK — gyvai veikia 9a1bfe7
Sep 02 09:31:31 vmi3306453 autoleft-deploy[3475929]: ```
Sep 02 09:31:31 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:31:31 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:31:31 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 23.240s CPU time.
Sep 02 09:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:32:32 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:32:32 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.251s CPU time.
Sep 02 09:33:36 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:33:38 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:33:38 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:33:38 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.558s CPU time.
Sep 02 09:34:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 09:35:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 09:35:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 09:35:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.867s CPU time.
Sep 02 09:36:02 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
