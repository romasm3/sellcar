# Visos 13 kalbų — kaip užpildyti iki galo

## Kur kas gyvena

| Dalykas | Failas |
|---|---|
| Jungiklis ir kalbų sąrašas | `config/settings.py` → `LANGUAGES` (13) |
| Patvirtinti terminai | `docs/terminai.md` (viršesnis už mašiną) |
| Terminų taikymas | `docs/terminai_taikyti.py` |
| Masinis užpildymas | `docs/vertimo_uzpildymas.py` |
| Kintamųjų sargyba | `docs/kintamuju_patikra.py` |
| Ataskaita „kiek išversta" | `docs/kalbu_skeneris.py` |

## Eiga (serveryje — ten yra Google raktas)

```bash
cd /root/autoleft && source venv/bin/activate

# 1. Katalogai iki naujausio kodo (visos 13 kalbų iš karto)
python manage.py makemessages --no-obsolete \
  -l lt -l en -l ru -l lv -l et -l pl -l de -l es -l fr \
  -l zh_Hans -l vi -l ar -l ko \
  --ignore=venv --ignore=staticfiles --ignore=node_modules --ignore=docs

# 2. Patvirtinti terminai — PIRMA, kad mašina jų nebeliestų
python docs/terminai_taikyti.py

# 3. Masinis užpildymas (visos kalbos, be lt — ji šaltinis)
python docs/vertimo_uzpildymas.py            # arba: … ru de pl
#    Paketai po 100, 200 ms pauzė, kritęs paketas praleidžiamas.
#    Naujos eilutės žymimos „#, fuzzy" — kol neperžiūrėtos, nerodomos.

# 4. Sargyba: kintamieji ir HTML žymės
python docs/kintamuju_patikra.py --zymek

# 5. Kompiliuojam ir tikrinam
python manage.py compilemessages
for f in locale/*/LC_MESSAGES/django.po; do msgfmt --check -o /dev/null "$f" || echo "BLOGAS: $f"; done

# 6. Ataskaita
python docs/kalbu_skeneris.py
```

Sucommitink **`.po`** — `.mo` į repo nebepatenka (žr. `.gitignore`).
Juos pagamina deploy'as: `deploy-agent.sh` po `collectstatic` paleidžia
`compilemessages`. Vietoje `.mo` vis tiek reikia — be jų vietinis
serveris rodys neišverstą tekstą.

## Ką sargyba daro

`docs/kintamuju_patikra.py` pažymi fuzzy tas eilutes, kuriose vertimas
sulaužė kintamąjį. Tris atvejus mašina daro nuolat:

| Originalas | Bloga mašina | Kodėl lūžta |
|---|---|---|
| `Found %(count)s listings` | `Найдено %(количество) объявлений` | išverstas kintamojo vardas |
| `{n} days` | `{ن} يومًا` | išverstas skliaustinio kintamojo vardas |
| `%(pct)s%% vs last week` | `与上周相比` | kintamasis dingo visai |

Fuzzy eilutė į `.mo` nepatenka, tad vartotojas mato originalą — lygiai
tą patį, ką matė iki tol. Nieko neištrinam.

## Ko mašina NEVERČIA

* **`lt`** — šaltinio kalba. Tuščias `msgstr` rodo patį `msgid`, o jis jau
  lietuviškas. Vertimas iš lietuvių į lietuvių tik sugadintų tekstą.
* **Daugiskaita** (`msgid_plural`) — rusiškai šitas katalogas reikalauja
  KETURIŲ formų, mašina duoda vieną. Tokios eilutės surašomos į
  `docs/vertimo_uzpildymas_ataskaita.txt` žmogui.
* **`docs/terminai.md` terminai** — patvirtinti, neperrašomi.

## Kalbų kodai

Django katalogas `zh_Hans`, o Google laukia `zh-CN`. Vertimas žinomas
`docs/vertimo_uzpildymas.py` → `GOOGLE_KODAS`.

## Raktas

Tik serveryje: `/root/autoleft/google-translate-key.json`
(`GOOGLE_APPLICATION_CREDENTIALS`). Debesies konteineryje jo nėra, tad
3 žingsnis ten neįvykdomas — visa kita daroma ir ten.
