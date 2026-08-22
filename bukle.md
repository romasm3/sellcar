# Serverio būklė

Sugeneruota: 2026-08-22 14:48:36 CEST

## Kodas

```
sukasi:      0b62625 feat(deploy): autodiegimas tikrina testus prieš liesdamas produkciją
origin/master: 7067ca6 docs(deploy): patikros vartai prieš diegimą
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
HTTP 301, 0.001091s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        32   MATOMAS
  draft         11   nematomas
  expired        4   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      15
  iš jų pasibaigę (expires_at praeityje): 4
  aktyvūs, baigsis per 7 d.: 1
  aktyvūs be pabaigos datos: 16 (pvz. testiniai)
Truck: skelbimų nėra.
WheelListing: skelbimų nėra.

Viešame sąraše matomi tik status="active" (+ neseniai parduoti).
Jei tavo seni skelbimai yra "expired" — juos reikia aktyvuoti iš naujo,
o ne taisyti kode.
```

## Vietos diske

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       291G   14G  278G   5% /
```

## Paskutinis auto-deploy

```
Aug 22 14:48:08 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 14:48:08 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 4.727s CPU time.
Aug 22 14:48:31 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 14:48:31 vmi3306453 autoleft-deploy[3951164]: [2026-08-22 14:48:31] === Naujų commit'ų rasta: 0b62625 → 7067ca6 ===
Aug 22 14:48:31 vmi3306453 autoleft-deploy[3951176]:     7067ca6 docs(deploy): patikros vartai prieš diegimą
Aug 22 14:48:31 vmi3306453 autoleft-deploy[3951164]: [2026-08-22 14:48:31] Kodas atnaujintas iki 7067ca6
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     ── 1/2  Šablonai: neuždarytas {# …
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:             švaru
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     ── 2/2  Puslapių testai
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     First list contains 4 additional elements.
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     First extra element 0:
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     'pagrindinis (/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …'
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     Diff is 659 characters long. Set self.maxDiff to None to see it. : Kainos rodomos doleriais, turi būti €:
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:       pagrindinis (/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:       rezultatai (/?category=cars&sidebar=1): …            <div class="ap-price" style="font-size:1.2rem;">$15900</div>                             </div>             …
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:       naršyti (/browse/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:       skelbimas (/740/): …Skelbimas | #740"> <meta property="og:description" content="$39 · TESTINIS SKELBIMAS. Sukurtas apžiūrai — realių duomenų…
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     ----------------------------------------------------------------------
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     Ran 5 tests in 4.405s
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     FAILED (failures=1)
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     
Aug 22 14:48:36 vmi3306453 autoleft-deploy[3951210]:     PATIKRA NEPRAĖJO — nediegti.
```
