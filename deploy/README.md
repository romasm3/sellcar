# Auto-deploy

Serveryje sukasi systemd timeris, kuris kas minutę pasitikrina `master` šaką ir,
radęs naujų commit'ų, pats juos parsisiunčia ir paleidžia deploy'ą.

```
GitHub master  ──fetch──▶  deploy-from-git.sh  ──▶  deploy-agent.sh
                              (saugikliai)            (migrate, collectstatic,
                                                       restart, health check,
                                                       rollback jei blogai)
```

Deploy'as vyksta **tik** iš `master`. Šakos (`claude/...`) į produkciją nepatenka,
kol nesumergini jų į `master`.

## Įjungimas (vienas kartas)

```bash
cd /root/autoleft
git pull                                  # kad atsirastų deploy-from-git.sh

# 1. Įsitikink, kad git fetch veikia be klausimų (žr. „Prieiga prie GitHub" žemiau)
sudo -u root git fetch origin master && echo "fetch OK"

# 2. Įdedam systemd vienetus
ln -sf /root/autoleft/deploy/systemd/autoleft-deploy.service /etc/systemd/system/
ln -sf /root/autoleft/deploy/systemd/autoleft-deploy.timer   /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now autoleft-deploy.timer
```

Patikrinimas:

```bash
systemctl list-timers autoleft-deploy     # kada kitas paleidimas
journalctl -u autoleft-deploy -n 50       # ką darė
```

## Kasdienis naudojimas

Nieko daryti nereikia. Sumergini į `master` → per ~1–2 min pasirodo svetainėje.

Iš tų dviejų minučių pati apklausa užima iki minutės, o likusį laiką —
`deploy-agent.sh`: migracijos, `collectstatic`, gunicorn restartas ir
health check'as. Momentinio nebūna ir negali būti.

Nenori laukti:

```bash
systemctl start autoleft-deploy           # paleidžia tą pačią sekundę
```

Rankinis paleidimas su matomu žurnalu:

```bash
/root/autoleft/deploy-from-git.sh
```

## Ką daro saugikliai

| Situacija | Elgesys |
|---|---|
| Nėra naujų commit'ų | Baigia tyliai, žurnale nieko |
| Kitas deploy'as dar sukasi | Praleidžia ciklą (`flock`) |
| Serveryje nesucommit'inti pakeitimai | **Sustoja** ir nieko neliečia — kitaip deploy'as juos užtrintų |
| Serveryje iškrauta ne `master` | Sustoja |
| Fast-forward negalimas | Sustoja (niekada neperrašo istorijos) |
| Health check po deploy'o nepraeina | `deploy-agent.sh` grąžina kodą iš `last_good`, tada `git reset --hard` atsuka istoriją — failai ir git vėl sutampa |

## Serverio būklė atgal į repo

Pokalbis su Claude sukasi debesyje ir šio serverio **nemato**. Vienintelis
kanalas atgal — GitHub. Todėl `deploy-from-git.sh` po kiekvieno ciklo
paleidžia `deploy/bukle.sh`, kuris surenka trumpą būklę ir įkelia ją į
atskirą šaką **`serverio-bukle`**, failą `bukle.md`.

Kas ten patenka:

* koks commit'as sukasi ir koks yra `origin/master`;
* ar darbo katalogas švarus;
* `gunicorn`, `nginx`, `postgresql`, `autoleft-deploy.timer` būsenos;
* ar svetainė atsako per gunicorn socket'ą (HTTP kodas ir laikas);
* skelbimų kiekiai pagal būseną (`skelbimu_bukle` **be** `--user`, tad
  jokių asmens duomenų);
* vietos diske;
* paskutinės 25 auto-deploy žurnalo eilutės.

**Vienpusis kanalas:** serveris rašo, kiti skaito. Iš repo nevykdoma jokia
komanda — kitaip bet kas, gavęs prieigą prie repo, gautų root'ą produkcijoje.

Keliama tik tada, kai kas nors realiai pasikeitė (laiko žymė lyginant
praleidžiama), todėl commit'ų kas 5 min nebūna.

Rankomis:

```bash
/root/autoleft/deploy/bukle.sh
```

Perskaityti galima ir be prieigos prie serverio — GitHub'e, šakoje
`serverio-bukle`, failas `bukle.md`.

## Prieiga prie GitHub

`git fetch` turi veikti be interaktyvaus klausimo, kitaip timeris kabės.
Būklės skelbimui reikia ir **push** teisės (į šaką `serverio-bukle`); jei jos
nėra, deploy'as veiks, o būklė tiesiog nebus įkelta.
Patikrink kaip sukonfigūruotas remote:

```bash
git remote -v
```

* **SSH** (`git@github.com:...`) — reikia deploy rakto `~/.ssh/` ir įrašo
  `known_hosts` faile. Patikrinimas: `ssh -T git@github.com`.
* **HTTPS** (`https://github.com/...`) — reikia įrašyto token'o, pvz.
  `git config --global credential.helper store` ir vienas rankinis `git fetch`.

## Ko šitas deploy'as NEDARO

* **DB neatsuka.** `deploy-agent.sh` prieš deploy'ą padaro dumpą į
  `/root/autoleft_backups/`, bet jei migracija sugadino duomenis — atkurti
  reikia ranka. Kodas atsukamas automatiškai, DB — ne.
* **Netikrina testų.** Į `master` pateko = diegiama. Jei norėsi CI vartų,
  reikės GitHub Actions prieš merge.
* **Neliečia `.env`, `media/`, `venv/`, `staticfiles/`** — jie neįtraukti į
  snapshot'ą, tad rollback jų nesugadins.

## Patikra prieš diegimą

Nuo 2026-08-22 `deploy-from-git.sh` prieš liesdamas produkciją paleidžia
`scripts/patikra.sh` (šablonų nuotėkio skenavimas + Django testai). Kritus:

* migracijos, `collectstatic` ir perkrovimas net nepradedami;
* kodas grąžinamas į ankstesnį commit'ą;
* blogas commit'as įrašomas į `deploy/.blogas-commitas`, kad timeris jo
  nekartotų kas minutę — žymė nusivalo, kai `master` gauna naują commit'ą.

Nuo 2026-09-02 ta pati žymė rašoma ir tada, kai krenta **pats
`deploy-agent.sh`** (health check). Anksčiau ji buvo rašoma tik po
`patikra.sh`, todėl kritęs deploy'as buvo kartojamas kas minutę — ir kas
minutę atsukdavo kodą. 2026-09-01 taip „dingo" keturi darbai iš eilės:
taimeris nebuvo sustojęs, jis sukosi ir kas kartą viską grąžindavo atgal.

Žurnalas: `journalctl -u autoleft-deploy -n 50`

## Kai deploy'as sustojo

Požymis: `master` juda, o gyva svetainė ne. Patikra per sekundę —
versijos žymė turi sutapti su `master`:

```bash
curl -s https://autoleft.com/ | grep -o 'name="versija" content="[^"]*"'
git -C /root/autoleft rev-parse --short=12 origin/master
```

Nesutampa — tikrinam eilės tvarka:

```bash
# 1. Ar taimeris gyvas
systemctl list-timers autoleft-deploy
journalctl -u autoleft-deploy -n 80 --no-pager

# 2. Ar nėra „šito commit'o daugiau nebandom" žymės
cat /root/autoleft/deploy/.blogas-commitas 2>/dev/null

# 3. Ar darbinis katalogas švarus (nešvarus stabdo git pull)
git -C /root/autoleft status --short --untracked-files=no
```

Atkūrimas, kai žymė yra ir priežastis pašalinta:

```bash
rm -f /root/autoleft/deploy/.blogas-commitas
/root/autoleft/deploy-from-git.sh
```

Žymė nusivalo ir pati, kai `master` gauna naują commit'ą — tad įprastu
atveju pakanka iškelti pataisą.

### Būklės kanalas gali nutilti atskirai

Šaka `serverio-bukle` yra VIENINTELIS kanalas iš serverio į pokalbį.
Ji rašoma per `deploy/bukle.sh`, o tas kviečiamas iš
`deploy-from-git.sh`. Vadinasi, kanalas gali nutilti dviem visiškai
skirtingais atvejais, ir iš išorės jie atrodo vienodai:

* nutilo pats deploy'as (taimeris, `git fetch`, nešvarus katalogas);
* deploy'as sukasi, bet `bukle.sh` push'as nepavyksta (dingusi
  `/root/autoleft_bukle` darbo kopija, pasibaigęs GitHub raktas).

2026-09 abu sutapo: `serverio-bukle` paskutinį kartą rašyta 08-22, nors
deploy'ai veikė iki 09-02. Todėl, kai gyva versija atsilieka, žiūrėk ne
į šaką, o į systemd:

```bash
# viskas vienu ypu
systemctl is-active autoleft-deploy.timer
systemctl list-timers autoleft-deploy --no-pager
journalctl -u autoleft-deploy -n 60 --no-pager
cat /root/autoleft/deploy/.blogas-commitas 2>/dev/null || echo '(žymės nėra)'
git -C /root/autoleft status --short --untracked-files=no
git -C /root/autoleft log --oneline -1
git -C /root/autoleft log --oneline -1 origin/master
ls -la /root/autoleft_bukle 2>/dev/null | head -3
```

Atgaivinimas (saugu paleisti net jei viskas gerai):

```bash
systemctl enable --now autoleft-deploy.timer
rm -f /root/autoleft/deploy/.blogas-commitas
/root/autoleft/deploy-from-git.sh          # paleidžia iškart, rodo žurnalą
```
