# Serverio būklė

Sugeneruota: 2026-08-27 17:19:14 CEST

## Kodas

```
sukasi:      715a34c feat(žemėlapis): skelbimai naujame skirtuke, telefone — su grįžimu atgal
origin/master: 715a34c feat(žemėlapis): skelbimai naujame skirtuke, telefone — su grįžimu atgal
šaka:        master
DĖMESIO: darbo katalogas nešvarus —
   M apps/listings/models.py
   M apps/listings/templatetags/contact_block_tags.py
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
HTTP 301, 0.001432s
```

## Skelbimų būsenos

```

Listing — iš viso 35
  active        22   MATOMAS
  draft          9   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      13
  iš jų pasibaigę (expires_at praeityje): 4
  aktyvūs, baigsis per 7 d.: 4
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
/dev/sda1       291G   18G  273G   7% /
```

## Paskutinis auto-deploy

```
Aug 27 17:11:07 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.206s CPU time.
Aug 27 17:12:10 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:12:12 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:12:12 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:12:12 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.009s CPU time.
Aug 27 17:13:13 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:13:14 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:13:14 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:14:18 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:14:20 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:14:20 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:14:20 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.103s CPU time.
Aug 27 17:15:28 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:15:29 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:15:29 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:15:29 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.052s CPU time.
Aug 27 17:16:57 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:16:59 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:16:59 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:16:59 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.042s CPU time.
Aug 27 17:17:59 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 27 17:18:02 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Aug 27 17:18:02 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 27 17:18:02 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.328s CPU time.
Aug 27 17:19:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
