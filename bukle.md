# Serverio būklė

Sugeneruota: 2026-09-02 18:32:36 CEST

## Kodas

```
sukasi:      1d7139c feat(vertimai): patvirtinti terminai — docs/terminai.md ir .po failai
origin/master: 8387fe8 feat(vertimai): penkios kategorijų eilutės ir pataisa „Metai" → „Год"
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
HTTP 301, 0.002306s
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
Sep 02 18:31:26 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.417s CPU time.
Sep 02 18:32:30 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 02 18:32:31 vmi3306453 autoleft-deploy[3878197]: [2026-09-02 18:32:31] === Naujų commit'ų rasta: 1d7139c → 8387fe8 ===
Sep 02 18:32:31 vmi3306453 autoleft-deploy[3878217]:     8387fe8 feat(vertimai): penkios kategorijų eilutės ir pataisa „Metai" → „Год"
Sep 02 18:32:31 vmi3306453 autoleft-deploy[3878197]: [2026-09-02 18:32:31] Kodas atnaujintas iki 8387fe8
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     ----------------------------------------------------------------------
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     Traceback (most recent call last):
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:       File "/root/autoleft/apps/listings/tests.py", line 95, in test_nera_sablono_komentaru_puslapiuose
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:         self.assertEqual(atsakymas.status_code, 200, f'{pavadinimas} ({adresas})')
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     AssertionError: 404 != 200 : pagrindinis (/)
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     ----------------------------------------------------------------------
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     Ran 11 tests in 1.879s
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     FAILED (failures=1, skipped=1)
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     ── 3/3  Vertimai: /en/ be lietuvių kalbos, šablonai apvynioti
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     Found 4 test(s).
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     System check identified no issues (0 silenced).
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     ....
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     ----------------------------------------------------------------------
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     Ran 4 tests in 0.347s
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     OK
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     
Sep 02 18:32:36 vmi3306453 autoleft-deploy[3878295]:     PATIKRA NEPRAĖJO — nediegti.
```
