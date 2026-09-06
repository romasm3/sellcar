# Serverio būklė

Sugeneruota: 2026-09-06 19:08:26 CEST

## Kodas

```
sukasi:      7cc1d46 fix(paieska): markių ir modelių skaičius be skliaustelių
origin/master: 7cc1d46 fix(paieska): markių ir modelių skaičius be skliaustelių
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
HTTP 301, 0.001261s
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
/dev/sda1       291G   28G  263G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:05 vmi3306453 autoleft-deploy[429150]: [19:06:05] Health OK (1/10)
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ❌ Šablonai/statiniai keitėsi, bet CSS vardas liko style.df8265b02e1b.css.
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06]    Naršyklės gaus seną failą — deploy stabdomas.
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️  ĮSPĖJIMAS: statinių maišas neatsinaujino, kaip tikėtasi.
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] Raktai: .env — vietoje.
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] Raktai: google-translate-key.json — vietoje.
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[429150]: [19:06:06] === Deploy OK ===
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: Sep 06 19:06:06 vmi3306453 autoleft-deploy[428996]: [2026-09-06 19:06:06] ✅ Deploy OK — gyvai veikia 7cc1d46
Sep 06 19:06:08 vmi3306453 autoleft-deploy[430159]: ```
Sep 06 19:06:08 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 19:06:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 19:06:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1min 10.380s CPU time.
Sep 06 19:06:08 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 19:06:10 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 19:06:10 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 19:06:10 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.440s CPU time.
Sep 06 19:07:16 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 19:07:18 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 19:07:18 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 19:07:18 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.473s CPU time.
Sep 06 19:08:26 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
