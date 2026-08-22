# Serverio būklė

Sugeneruota: 2026-08-22 15:12:48 CEST

## Kodas

```
sukasi:      7067ca6 docs(deploy): patikros vartai prieš diegimą
origin/master: 033a472 fix(mob): zvaigzduciu zenkliukas atgal oranzinis
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
HTTP 301, 0.003030s
```

## Skelbimų būsenos

```

Listing — iš viso 47
  active        33   MATOMAS
  draft         11   nematomas
  expired        3   nematomas
  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─
  nematomi dėl būsenos:      14
  iš jų pasibaigę (expires_at praeityje): 3
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
Aug 22 15:12:41 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 15:12:42 vmi3306453 autoleft-deploy[3956770]: [2026-08-22 15:12:42] === Naujų commit'ų rasta: 7067ca6 → 033a472 ===
Aug 22 15:12:42 vmi3306453 autoleft-deploy[3956788]:     033a472 fix(mob): zvaigzduciu zenkliukas atgal oranzinis
Aug 22 15:12:42 vmi3306453 autoleft-deploy[3956788]:     d379d56 merge: salygu sakinys mokejimo puslapyje lietuviskai
Aug 22 15:12:42 vmi3306453 autoleft-deploy[3956788]:     bfb0691 fix(mokejimai): salygu sakinys mokejimo puslapyje buvo pusiau angliskas
Aug 22 15:12:42 vmi3306453 autoleft-deploy[3956770]: [2026-08-22 15:12:42] Kodas atnaujintas iki 033a472
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     ── 1/2  Šablonai: neuždarytas {# …
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:             švaru
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     ── 2/2  Puslapių testai
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     First list contains 4 additional elements.
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     First extra element 0:
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     'pagrindinis (/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …'
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     Diff is 659 characters long. Set self.maxDiff to None to see it. : Kainos rodomos doleriais, turi būti €:
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:       pagrindinis (/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:       rezultatai (/?category=cars&sidebar=1): …            <div class="ap-price" style="font-size:1.2rem;">$15900</div>                             </div>             …
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:       naršyti (/browse/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:       skelbimas (/740/): …Skelbimas | #740"> <meta property="og:description" content="$39 · TESTINIS SKELBIMAS. Sukurtas apžiūrai — realių duomenų…
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     ----------------------------------------------------------------------
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     Ran 5 tests in 5.338s
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     FAILED (failures=1)
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     
Aug 22 15:12:48 vmi3306453 autoleft-deploy[3956869]:     PATIKRA NEPRAĖJO — nediegti.
```
