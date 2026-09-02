# Terminai — patvirtinti vertimai

Šitas failas yra **vienintelis šaltinis** filtrų laukų, reikšmių,
kategorijų ir sąsajos terminams lietuvių, rusų ir anglų kalbomis.

**Vertimai patvirtinti (vartotojo sprendimas 2026-09-02). Jų nekeičiam ir
neverčiam iš naujo.** Jei kur nors kyla abejonė dėl termino, etalonas —
autogidas.lt rusiška versija (`autogidas.lt/ru/`), o ne naujas vertimas.

Į .po failus taikoma automatiškai:

    python docs/terminai_taikyti.py --bandymas    # tik parodo, ką darytų
    python docs/terminai_taikyti.py               # įrašo .po ir .mo

Skriptas skaito TIK šitą failą. Naujas terminas pridedamas čia, ne .po.

## Laukai

| Lietuviškai | По-русски | English |
|---|---|---|
| Markė | Марка | Make |
| Modelis | Модель | Model |
| Metai | Год | Year |
| Kaina | Цена | Price |
| Kuro tipas | Тип топлива | Fuel type |
| Kėbulo tipas | Тип кузова | Body type |
| Pavarų dėžė | Коробка передач | Gearbox |
| Rida | Пробег | Mileage |
| Galia, kW | Мощность, кВт | Power, kW |
| Darbinis tūris | Объём двигателя | Engine size |
| Varantieji ratai | Привод | Drive |
| Vairo padėtis | Расположение руля | Steering side |
| Defektai | Дефекты | Defects |
| Durų skaičius | Количество дверей | Doors |
| Sėdimų vietų skaičius | Количество мест | Seats |
| Spalva | Цвет | Colour |
| Euro standartas | Евростандарт | Euro standard |
| Pirmosios registracijos šalis | Страна первой регистрации | First registration country |
| Šalis | Страна | Country |
| Miestas | Город | City |
| Pardavėjo tipas | Тип продавца | Seller type |
| Ypatybės | Особенности | Features |
| Nuo / Iki | От / До | From / To |
| Visi / Visos | Все | All |

## Reikšmės

| Lietuviškai | По-русски | English |
|---|---|---|
| Benzinas | Бензин | Petrol |
| Dyzelinas | Дизель | Diesel |
| Benzinas / dujos | Бензин / газ | Petrol / LPG |
| Hibridas | Гибрид | Hybrid |
| Elektra | Электро | Electric |
| Automatinė | Автоматическая | Automatic |
| Mechaninė | Механическая | Manual |
| Sedanas | Седан | Saloon |
| Universalas | Универсал | Estate |
| Hečbekas | Хэтчбек | Hatchback |
| Visureigis / Krosoveris | Внедорожник / Кроссовер | SUV / Crossover |
| Kupė | Купе | Coupe |
| Kabrioletas | Кабриолет | Convertible |
| Vienatūris | Минивэн | MPV |
| Kairėje / Dešinėje | Слева / Справа | Left / Right |
| Priekiniai | Передний | Front |
| Galiniai | Задний | Rear |
| Visi varantys | Полный | All-wheel |
| Be defektų | Без дефектов | No defects |
| Daužtas | Битый | Damaged |
| Privatus asmuo | Частное лицо | Private seller |
| Įmonė | Компания | Dealer |

## Kategorijos

| Lietuviškai | По-русски | English |
|---|---|---|
| Automobiliai | Легковые автомобили | Cars |
| Motociklai | Мотоциклы | Motorcycles |
| Sunkvežimiai | Грузовики | Trucks |
| Vilkikai | Тягачи | Tractor units |
| Autobusai | Автобусы | Buses |
| Priekabos / Puspriekabės | Прицепы / Полуприцепы | Trailers |
| Žemės ūkio technika | Сельхозтехника | Agricultural machinery |
| Automobilių nuoma | Аренда автомобилей | Car rental |
| Ratlankiai | Диски | Wheels |
| Visos markės | Все марки | — |
| Žemės ūkio technika, padargai | Сельхозтехника, навесное оборудование | — |
| Autotraukiniai, autovežiai | Автопоезда, автовозы | — |
| Komunalinio ūkio transportas | Коммунальная техника | — |
| Limuzinų, vestuvių transportas | Лимузины, свадебный транспорт | — |

## Sąsaja

| Lietuviškai | По-русски | English |
|---|---|---|
| Skelbimai | Объявления | Listings |
| Mano paieškos | Мои поиски | My searches |
| Tik Lietuvoje | Только в Литве | Lithuania only |
| Ieškoti | Найти | Search |
| Filtruoti | Фильтровать | Filter |
| Išvalyti | Очистить | Clear |
| Keisti šalį | Сменить страну | Change country |
| Visos šalys | Все страны | All countries |
| Įkelti | Разместить | Post |
| Žinutės | Сообщения | Messages |
| Įmonės ir servisai | Компании и сервисы | Businesses and services |

Brūkšnys `—` langelyje reiškia, kad tos kalbos vertimo dar nėra ir
skriptas to langelio neliečia. Terminas nuo to netampa neteisingas —
tiesiog laukia.

## Sudėtinės eilutės

Kelios lentelės eilutės sujungia du atskirus sąsajos užrašus („Nuo / Iki"
yra du laukai, ne vienas). Sąsajoje jie gyvena atskirai, tad taikant
skaidom — vertimai TIE PATYS, tik priskirti savo eilutei.

| Lietuviškai | По-русски | English |
|---|---|---|
| Nuo | От | From |
| Iki | До | To |
| Visi | Все | All |
| Visos | Все | All |
| Kairėje | Слева | Left |
| Dešinėje | Справа | Right |
| Priekabos | Прицепы | Trailers |
| Puspriekabės | Полуприцепы | Semi-trailers |

## Kaip taikoma

* msgid'ai projekte mišrūs — dalis lietuviški, dalis dar angliški
  (senesnis kodas). Skriptas ieško **abiejų**: ir lietuviško, ir angliško
  varianto, ir nepaiso raidžių dydžio bei galinio dvitaškio.
* Patvirtinti vertimai įrašomi **be `#, fuzzy`**: fuzzy eilutė
  nekompiliuojama į .mo ir vartotojui nerodoma — pažymėjus fuzzy
  vertimas tiesiog neveiktų.
* Viskas, kas NĖRA šitame faile, lieka kaip buvo. Skriptas nieko
  neverčia savo nuožiūra.
* `.mo` failai projekte laikomi git'e, o deploy jų nekompiliuoja, todėl
  skriptas juos perrašo iš karto.

## Kas dar neišversta

    python docs/terminai_taikyti.py --sarasas ru > /tmp/ru-truksta.txt

Išveda neišverstas eilutes su kontekstu (failas ir eilutė), kad būtų
galima peržiūrėti ir išversti rankomis.
