# Serverio būklė

Sugeneruota: 2026-09-01 22:53:19 CEST

## Kodas

```
sukasi:      b3e737b fix(deploy): statinių patikra nebeatsuka kodo + versijos žymė
origin/master: b3e737b fix(deploy): statinių patikra nebeatsuka kodo + versijos žymė
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
HTTP 301, 0.001625s
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
/dev/sda1       291G   45G  246G  16% /
```

## Paskutinis auto-deploy

```
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/ekranai/kort-vieta-1600-salis-blokas.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/ekranai/kort-vieta-390-ilgas.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      D docs/ekranai/sonine-juosta-apacia.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      D docs/ekranai/sonine-juosta-virsus.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/ekranai/viena-salis-1600-kontaktai-de.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/ekranai/viena-salis-1600-sonine-de.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/ekranai/viena-salis-1600-sonine-sarasas.png
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/kort_vieta_playwright.js
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/salies_juosta_test.py
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      D docs/sonine_juosta_playwright.js
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      D docs/sonines_juostos_sarasas.py
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      D docs/statiniu_kesas_test.py
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/taisykles.md
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/veliavos_test.py
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M docs/viena_salis_test.py
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      D static/css/sonine_juosta.css
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M templates/base.html
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M templates/listings/emails/expired.html
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M templates/listings/emails/expiring_soon.html
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002196]:      M templates/pages/partneriai.html
Sep 01 22:50:06 vmi3306453 autoleft-deploy[3002170]: [2026-09-01 22:50:06] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Sep 01 22:50:06 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Sep 01 22:50:06 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Sep 01 22:50:06 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 01 22:53:19 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
