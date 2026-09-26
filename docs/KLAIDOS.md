# AutoLeft — klaidų registras (rodyklė)

Nuo 2026-09-15 klaidos skaidomos **po kategorijas**. Šis failas — tik rodyklė.
Vieta serveryje: `/root/autoleft/docs/`

| Failas | Kas ten |
|---|---|
| `klaidos/AUTOMOBILIAI.md` | `/create/cars/quick/` — `CAR-*`, `DRAFT-01`, `TITLE-01`, `MODEL-01`, `ADD-01…03` |
| `klaidos/DALYS.md` | `/create/parts/form/`, `/create/car-for-parts/` — `PARTS-*`, `LANG-05`, `LANG-07`, `GEO-01` |
| `klaidos/PADANGOS.md` | `/create/tyres/`, `/create/rims/`, `/browse/tyres/` — `TYRE-*`, `RIM-01` |
| `klaidos/MOTO-PADANGOS.md` | tos pačios formos su `purpose=moto` — `MTYRE-*` |
| `klaidos/BENDROS.md` | visoms kategorijoms — `CUR-01`, `MOTO-01`, `GEAR-01`, `EDIT-01`, `LANG-01…04`, `CFG-*`, `ADD-04`, `ADD-05`, šaltiniai ir metodai |
| `klaidos/_ARCHYVAS-KLAIDOS-senas.md` | senas vientisas sąrašas (2026-09-14), tik istorijai |

**Kaip naudotis**
- Kiekviena klaida turi kodą (pvz. `CAR-01`). Promptuose minėk kodą.
- Būsenos: `NAUJA` · `TAISOMA` · `IŠTAISYTA` · `ATŠAUKTA`
- Ištaisius — Claude Code pats pakeičia būseną ir prirašo commit'ą.
- Nauja klaida rašoma į savo kategorijos failą, kodas niekada nenaudojamas pakartotinai.

**Nuolatiniai draudimai visiems taisymams**
- Valiutos logikos neliesti — viskas eurais (GBP/USD bus atskirai)
- Vienetų jungiklių (L/cm³, km/mi, kg/lbs) nešalinti
- Middleware nekurti
- Dizaino nekeisti
- Taisyti tik tą kodą, kuris nurodytas
- Šablonus serveryje redaguoti per SSH prijungtą redaktorių, ne per terminalo heredoc

Etalonas — **autogidas.lt**. Ko jis turi, o mes ne = trūkumas.
Ko mes turime daugiau = pranašumas, paliekam.

---

## BENDRA EILĖ — kas pirma

| # | Kodas | Kur | Kodėl pirma |
|---|---|---|---|
| 1 | `TYRE-01` + `RIM-01` | PADANGOS | Vienos eilutės klaida (`id_contact_phone` → `id_phone`) blokuoja **dvi** kategorijas visiškai |
| 2 | `PARTS-01` | DALYS | `/create/car-for-parts/` 500 — kategorija neveikia |
| 3 | `MOTO-01` + `GEAR-01` + `EDIT-01` | BENDROS | Redagavimas sulūžęs |
| 4 | `CUR-01` | BENDROS | Neteisingos kainos (automobilių formoje jau nebepasikartoja — patikrinti likusias) |
| 5 | `DRAFT-01` | AUTOMOBILIAI | Vieši „Untitled draft" |
| 6 | `PARTS-04`, `CAR-03`, `TYRE-13` | visos | Vienodas `agree_terms required` — nuima duomenų praradimą |
| 7 | `TYRE-02` | PADANGOS | Validacija rodo ne tą lauką |
| 8 | `CAR-02`, `CAR-08`, `CAR-09` | AUTOMOBILIAI | Privalomumas ir nuotraukų dubliai |
| 9 | `TYRE-05…09`, `LANG-06` | PADANGOS / AUTOMOBILIAI | Pigūs šablonų taisymai |
| 10 | `CAR-04`, `CAR-05` | AUTOMOBILIAI | Neteisingi skaičiai |
| 11 | `TYRE-03`, `TYRE-04`, `MTYRE-01`, `MTYRE-02` | PADANGOS | Dydžių sąrašai |
| 12 | `TITLE-01`, `LANG-01…04`, `CFG-*` | BENDROS | Vertimai ir konfigūracija |
| 13 | `PARTS-06`, `LANG-05` | DALYS | Dideli darbai |
| 14 | `ADD-01…05` | visos | Papildymai |

---

## VISI TESTINIAI SKELBIMAI

| ID | Kas | Kategorija |
|---|---|---|
| #762 | MAN 18.510 TGX GX 2022 | sunkusis |
| #763–765 | BMW S1000RR, Ducati Panigale, Harley Fat Boy | motociklai |
| #766 | Fendt 412 Vario | žemės ūkis |
| #767 | HJC šalmas | moto apranga |
| #768 | VW T6 Transporter 2016 | mikroautobusai |
| #769–782 | automobiliai (žr. `klaidos/AUTOMOBILIAI.md`) | automobiliai |
| #789, #791, #792, #798, #799 | neteisinga valiuta (PLN/SEK/CHF) | `CUR-01` |
| #800–809 | 10 euro zonos automobilių | automobiliai |
| #810–815 | 6 dalys (variklis, žibintas, dėžė, diskai, durys, ratlankiai) | dalys |
| #816–820 | 5 automobiliai: FI, NO, RO, CZ, BG | automobiliai |
| `/wheels/26–31/` | 6 padangų skelbimai — po vieną į kiekvieną paskirtį | padangos |
