# Serverio būklė

Sugeneruota: 2026-08-22 15:09:30 CEST

## Kodas

```
sukasi:      7067ca6 docs(deploy): patikros vartai prieš diegimą
origin/master: d379d56 merge: salygu sakinys mokejimo puslapyje lietuviskai
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
HTTP 301, 0.001147s
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
Aug 22 15:08:13 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Aug 22 15:09:25 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Aug 22 15:09:25 vmi3306453 autoleft-deploy[3956083]: [2026-08-22 15:09:25] === Naujų commit'ų rasta: 7067ca6 → d379d56 ===
Aug 22 15:09:25 vmi3306453 autoleft-deploy[3956100]:     d379d56 merge: salygu sakinys mokejimo puslapyje lietuviskai
Aug 22 15:09:25 vmi3306453 autoleft-deploy[3956100]:     bfb0691 fix(mokejimai): salygu sakinys mokejimo puslapyje buvo pusiau angliskas
Aug 22 15:09:25 vmi3306453 autoleft-deploy[3956083]: [2026-08-22 15:09:25] Kodas atnaujintas iki d379d56
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     ── 1/2  Šablonai: neuždarytas {# …
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:             švaru
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     ── 2/2  Puslapių testai
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     First list contains 4 additional elements.
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     First extra element 0:
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     'pagrindinis (/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …'
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     Diff is 659 characters long. Set self.maxDiff to None to see it. : Kainos rodomos doleriais, turi būti €:
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:       pagrindinis (/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:       rezultatai (/?category=cars&sidebar=1): …            <div class="ap-price" style="font-size:1.2rem;">$15900</div>                             </div>             …
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:       naršyti (/browse/): …iv>                             <div class="home-tab-price">$39</div>                         </div>                    …
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:       skelbimas (/740/): …Skelbimas | #740"> <meta property="og:description" content="$39 · TESTINIS SKELBIMAS. Sukurtas apžiūrai — realių duomenų…
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     ----------------------------------------------------------------------
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     Ran 5 tests in 4.354s
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     FAILED (failures=1)
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     
Aug 22 15:09:30 vmi3306453 autoleft-deploy[3956165]:     PATIKRA NEPRAĖJO — nediegti.
```
