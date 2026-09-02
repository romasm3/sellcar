# Serverio būklė

Sugeneruota: 2026-09-02 16:52:13 CEST

## Kodas

```
sukasi:      15d2b7f fix(deploy): serverio raktai nebedingsta, kopijos nebeėda disko
origin/master: 15d2b7f fix(deploy): serverio raktai nebedingsta, kopijos nebeėda disko
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
HTTP 301, 0.010781s
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
/dev/sda1       291G   34G  257G  12% /
```

## Paskutinis auto-deploy

```
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] ⚠️  Kodas NEATSUKAMAS — svetainė veikia. Lankytojų naršyklės
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] ⚠️  gali kurį laiką rodyti seną CSS; patikrink rankiniu būdu:
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] ⚠️    curl -s https://autoleft.com/ | grep -o 'style\.[a-z0-9]*\.css'
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] ✅ Veikia — atnaujinam 'last_good' į naują versiją.
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] Raktai: .env — vietoje.
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] Raktai: google-translate-key.json — vietoje.
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797318]: [16:48:48] === Deploy OK ===
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: Sep 02 16:48:48 vmi3306453 autoleft-deploy[3797142]: [2026-09-02 16:48:48] ✅ Deploy OK — gyvai veikia 15d2b7f
Sep 02 16:48:51 vmi3306453 autoleft-deploy[3798180]: ```
Sep 02 16:48:51 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:48:51 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:48:51 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 44.206s CPU time.
Sep 02 16:48:51 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:48:53 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:48:53 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:48:53 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.464s CPU time.
Sep 02 16:49:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:49:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:49:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:49:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.549s CPU time.
Sep 02 16:51:09 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 16:51:11 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 02 16:51:11 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 02 16:51:11 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.519s CPU time.
Sep 02 16:52:12 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
