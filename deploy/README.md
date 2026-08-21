# Auto-deploy

Serveryje sukasi systemd timeris, kuris kas 5 min pasitikrina `master` šaką ir,
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

Nieko daryti nereikia. Sumergini į `master` → per ≤5 min pasirodo svetainėje.

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

## Prieiga prie GitHub

`git fetch` turi veikti be interaktyvaus klausimo, kitaip timeris kabės.
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
