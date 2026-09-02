# Serverio būklė

Sugeneruota: 2026-09-02 17:56:59 CEST

## Kodas

```
sukasi:      1d7139c feat(vertimai): patvirtinti terminai — docs/terminai.md ir .po failai
origin/master: 1d7139c feat(vertimai): patvirtinti terminai — docs/terminai.md ir .po failai
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
HTTP 301, 0.001062s
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
/dev/sda1       291G   32G  260G  11% /
```

## Paskutinis auto-deploy

```
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:11 vmi3306453 autoleft-deploy[3847733]: [17:53:11] Restartinam gunicorn.service
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:13 vmi3306453 autoleft-deploy[3847733]: [17:53:13] Health OK (1/10)
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:13 vmi3306453 autoleft-deploy[3847733]: [17:53:13] Statiniai OK: style.df8265b02e1b.css (manifestas atnaujintas)
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:13 vmi3306453 autoleft-deploy[3847733]: [17:53:13] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:14 vmi3306453 autoleft-deploy[3847733]: [17:53:14] Raktai: .env — vietoje.
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:14 vmi3306453 autoleft-deploy[3847733]: [17:53:14] Raktai: google-translate-key.json — vietoje.
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:14 vmi3306453 autoleft-deploy[3847733]: [17:53:14] === Deploy OK ===
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: Sep 02 17:53:14 vmi3306453 autoleft-deploy[3847552]: [2026-09-02 17:53:14] ✅ Deploy OK — gyvai veikia 1d7139c
Sep 02 17:53:16 vmi3306453 autoleft-deploy[3848470]: ```
Sep 02 17:53:16 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:53:16 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:53:16 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 45.317s CPU time.
Sep 02 17:53:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:53:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:53:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:53:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.338s CPU time.
Sep 02 17:54:37 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:54:39 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:54:39 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:54:39 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.376s CPU time.
Sep 02 17:55:49 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 17:55:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 17:55:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 17:55:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.577s CPU time.
Sep 02 17:56:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
