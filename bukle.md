# Serverio būklė

Sugeneruota: 2026-09-06 10:27:14 CEST

## Kodas

```
sukasi:      7a71bd0 vertimai: uzpildyti, sugadinti pazymeti fuzzy
origin/master: 7a71bd0 vertimai: uzpildyti, sugadinti pazymeti fuzzy
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
HTTP 301, 0.001332s
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
/dev/sda1       291G   28G  264G  10% /
```

## Paskutinis auto-deploy

```
Sep 06 10:22:45 vmi3306453 autoleft-deploy[84641]: [2026-09-06 10:22:45] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Sep 06 10:22:45 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Sep 06 10:22:45 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Sep 06 10:22:45 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 10:23:47 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85327]: [2026-09-06 10:23:47] === Naujų commit'ų rasta: e9f575f → 35faba5 ===
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85341]:     35faba5 docs(deploy): būklės kanalas gali nutilti atskirai nuo deploy'o
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85341]:     c5903bc feat(kalbos): visos 13 kalbų paruoštos užpildymui + pašto patikra visiems laukams
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85341]:     889dff0 fix(kalbos): „Registruotis" verčiasi, o perjungiklis veikia ir su ?next=
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85341]:     13295a4 feat(mokejimai): visų skelbimų įkėlimas nemokamas per vieną jungiklį
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85327]: [2026-09-06 10:23:47] Nesucommit'inti pakeitimai serveryje:
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85346]:      M docs/vertimo_uzpildymas_ataskaita.txt
Sep 06 10:23:47 vmi3306453 autoleft-deploy[85327]: [2026-09-06 10:23:47] ❌ Darbo katalogas nešvarus — deploy'as sustabdytas. Sutvarkyk ranka.
Sep 06 10:23:47 vmi3306453 systemd[1]: autoleft-deploy.service: Main process exited, code=exited, status=1/FAILURE
Sep 06 10:23:47 vmi3306453 systemd[1]: autoleft-deploy.service: Failed with result 'exit-code'.
Sep 06 10:23:47 vmi3306453 systemd[1]: Failed to start AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 10:24:58 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 10:25:09 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 10:25:09 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 10:25:09 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 3.842s CPU time.
Sep 06 10:26:03 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
Sep 06 10:26:06 vmi3306453 systemd[1]: autoleft-deploy.service: Deactivated successfully.
Sep 06 10:26:06 vmi3306453 systemd[1]: Finished AutoLeft — deploy iš git, kai master gauna naujų commit'ų.
Sep 06 10:26:06 vmi3306453 systemd[1]: autoleft-deploy.service: Consumed 1.735s CPU time.
Sep 06 10:27:14 vmi3306453 systemd[1]: Starting AutoLeft — deploy iš git, kai master gauna naujų commit'ų...
```
