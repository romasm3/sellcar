# Serverio būklė

Sugeneruota: 2026-09-02 16:02:33 CEST

## Kodas

```
sukasi:      f1886fe feat(zinutes): vertimas tapo jungikliu su išsaugoma būsena
origin/master: f1886fe feat(zinutes): vertimas tapo jungikliu su išsaugoma būsena
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
HTTP 301, 0.004690s
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
/dev/sda1       291G   50G  242G  17% /
```

## Paskutinis auto-deploy

```
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757488]: [15:58:51] === Deploy OK ===
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: Sep 02 15:58:51 vmi3306453 autoleft-deploy[3757358]: [2026-09-02 15:58:51] ✅ Deploy OK — gyvai veikia f1886fe
Sep 02 15:58:55 vmi3306453 autoleft-deploy[3758008]: ```
Sep 02 15:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:58:55 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:58:55 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 20.123s CPU time.
Sep 02 15:59:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 15:59:21 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 15:59:21 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 15:59:21 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.516s CPU time.
Sep 02 16:00:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:00:27 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:00:27 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:00:27 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.700s CPU time.
Sep 02 16:01:27 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:01:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:01:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:01:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.581s CPU time.
Sep 02 16:02:32 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
