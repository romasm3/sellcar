# Mokėjimų jungiklis

Šiuo metu **visų skelbimų įkėlimas nemokamas**. Laikinai — kol bus
įjungti mokėjimai. Mokėjimo kodas NIEKUR neištrintas.

## Jungiklis

`config/settings.py`:

```python
MOKEJIMAI_IJUNGTI = config("MOKEJIMAI_IJUNGTI", default=False, cast=bool)
PAYMENTS_ENABLED  = MOKEJIMAI_IJUNGTI and bool(STRIPE_SECRET_KEY)
```

| Reikšmė | Kas vyksta |
|---|---|
| `False` (dabar) | Skelbimas aktyvuojamas iš karto, planų puslapio nėra, piniginė ir mokami priedai paslėpti |
| `True` | Grįžta senas srautas: planų pasirinkimas, nurašymas iš piniginės |

Įjungti serveryje — į `.env` įrašyti `MOKEJIMAI_IJUNGTI=True` ir
`systemctl restart gunicorn`. Nieko kito taisyti nereikia.

Stripe raktas vienas savaime mokėjimų **nebeįjungia**: jungiklis
viršesnis. Anksčiau `PAYMENTS_ENABLED = bool(STRIPE_SECRET_KEY)` — dėl
to skelbimai kabo laukdami apmokėjimo vien todėl, kad `.env` turi raktą.

## Kur jungiklis veikia

Vietų mažai, nes visos eina per vieną tašką:

* `apps/listings/constants.py:can_create_free_listing` — **visų**
  kategorijų įkėlimo formos per jį sprendžia, publikuoti iš karto ar
  vesti į planus. Todėl nereikėjo lopyti dvidešimties
  `redirect('listing_select_plan')` vietų atskirai.
* `apps/listings/views.py:listing_activate` — skydelio „Aktyvuoti"
  ir „Pratęsti".
* `listing_select_plan` ir `listing_pay_plan` — į juos veda senos
  nuorodos ir laiškų saitai. Išjungus mokėjimus jie **neatsiduria
  aklavietėje**: aktyvuoja nemokamai ir veda į „pavyko". Mygtukų
  neslepiam — kitaip nebūtų kaip atkurti pasibaigusio skelbimo.
* `listing_services_order` / `listing_services_checkout`,
  `accounts:wallet`, `wallet_top_up`, `become_dealer` — uždaryti.
* `apps/listings/context_processors.py:mokejimai` → šablonų
  `{% if MOKEJIMAI_IJUNGTI %}`: piniginė ir prekiautojas antraštėje,
  „Užsakyti paslaugas" skydelyje.

Nemokamas publikavimas naudoja tą pačią užpildymo sąlygą kaip planų
puslapis (`_skelbimas_uzpildytas`) — pusiau tuščias juodraštis į
svetainę nepakliūva.

## Įstrigę skelbimai

Kol mokėjimai buvo įjungti, užpildytas skelbimas likdavo `draft`, kol
žmogus nusipirks planą. Tokius aktyvuoja:

```bash
cd /root/autoleft && source venv/bin/activate
python manage.py aktyvuok_istrigusius --bandymas   # tik parodo
python manage.py aktyvuok_istrigusius              # aktyvuoja
python manage.py aktyvuok_istrigusius --laiskai    # ir laiškai autoriams
```

Aktyvuojami tik **užpildyti** juodraščiai; neužpildyti lieka
juodraščiais.

## Patikra

`docs/nemokamu_skelbimu_test.py` — 51 patikra, abi jungiklio padėtys:
nemokamas srautas, grąžintas mokėjimo srautas, įstrigusių aktyvavimas ir
kad payments programa, modeliai, migracijos ir šablonai neištrinti.
