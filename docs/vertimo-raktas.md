# Vertimas pokalbiuose — raktas ir Google konsolė

Variklis — **Google Cloud Translation API v2**. Kitų tiekėjų projekte
nebuvo ir nėra.

## Du keliai iki Google

Kodas pats pasirenka, kuriuo eiti (`apps/conversations/translate_service.py`):

| Eilė | Sąlyga | Kaip kviečiama |
|---|---|---|
| 1 | `GOOGLE_APPLICATION_CREDENTIALS` rodo į **esantį** JSON failą | per `google-cloud-translate` biblioteką |
| 2 | `.env` yra `GOOGLE_TRANSLATE_API_KEY`, o jo nesant — `GOOGLE_MAPS_API_KEY` | tiesiai į `https://translation.googleapis.com/language/translate/v2?key=…` |
| 3 | nėra nei vieno | `VertimoNera` → žurnale klaida, sąsajoje **„Vertimas neįjungtas"** |

Trečiuoju atveju originalas su sėkmės būsena NEBERODOMAS: anksčiau
žmogus matydavo savo kalbą ir manydavo, kad toks ir vertimas.

### Kodėl API raktui nenaudojam `client_options={"api_key": …}`

Patikrinta `google-cloud-translate` **3.26.0** kode:
`translate_v2/client.py` iš `client_options` skaito **tik**
`api_endpoint`, o `api_key` tyliai ignoruoja ir vis tiek eina ieškoti
numatytųjų kredencialų — todėl su vien API raktu klientas krinta
`DefaultCredentialsError`. Dėl to raktinis kelias eina tiesiai į tą patį
viešą v2 galinį tašką per `requests` (jis jau yra priklausomybėse).
Rezultatas identiškas — tas pats Google, tas pats atsakymo formatas.

## Ką padaryti Google konsolėje

1. **Įjungti Cloud Translation API tame pačiame projekte**, kuriame
   sukurtas naudojamas raktas:
   <https://console.cloud.google.com/apis/library/translate.googleapis.com>
   → *Enable*. Jei to nepadaryta, Google atsako `403` su
   „Cloud Translation API has not been used in project … before or it is
   disabled" — tas tekstas atsiduria gunicorn žurnale kaip yra.
2. **Projekte turi būti įjungtas atsiskaitymas** (Billing). Translation
   API be jo neveikia net nemokamos kvotos ribose.
3. **Rakto apribojimai.** `GOOGLE_MAPS_API_KEY` dažniausiai būna
   apribotas *API restrictions → Maps JavaScript API* ir tada Translation
   atmes. Reikia arba tame pačiame apribojimų sąraše pridėti
   **Cloud Translation API**, arba (geriau) susikurti atskirą raktą
   vertimui ir įrašyti jį kaip `GOOGLE_TRANSLATE_API_KEY`.
4. **Nuorodų (HTTP referrer) apribojimas serveriui netinka** — užklausa
   eina iš serverio, ne iš naršyklės. Jei raktas ribojamas, rinkis
   *IP addresses* ir įrašyk serverio IP.

## .env serveryje

```
# Atskiras raktas vertimui (rekomenduojama)
GOOGLE_TRANSLATE_API_KEY=AIza…
```

Jo neįrašius, imamas jau esantis `GOOGLE_MAPS_API_KEY` — tada būtinai
patikrink 3 punktą.

Po pakeitimo: `systemctl restart gunicorn`.

## Kaip patikrinti

```bash
cd /root/autoleft && source venv/bin/activate
python docs/vertimo_diagnostika.py
```

Išveda keturias eilutes: paketas · raktas · lentelė · tikras kvietimas.
Kiekvienai klaidai nurodo, ką taisyti. Tas pačias priežastis nuo šiol
mato ir naršyklė — atsakyme yra `error_type`:

| `error_type` | Reiškia |
|---|---|
| `VertimoNera` | nei JSON failo, nei API rakto |
| `ModuleNotFoundError` | `google-cloud-translate` neįdiegtas venv'e (reikalingas tik 1 keliui) |
| `DefaultCredentialsError` | JSON failas nurodytas, bet netinkamas |
| `RuntimeError: Google Translate 403…` | API neįjungtas arba raktas apribotas |
| `RuntimeError: Google Translate 429…` | viršyta kvota |
