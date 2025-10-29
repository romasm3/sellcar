# SellCar - Automobilių pardavimo platforma

Django projektas automobilių, motociklų ir kitos technikos pardavimui.

## Funkcionalumas

- ✅ Vartotojų registracija ir autentifikacija
- ✅ Skelbimų kūrimas su nuotraukomis
- ✅ Išsami paieška ir filtravimas
- ✅ Google Maps integracija
- ✅ Paieška žemėlapyje su popup langais
- ✅ Išsaugotų skelbimų funkcija
- ✅ Vartotojo profilio valdymas
- ✅ Admin panelė skelbimų valdymui

## Technologijos

- Python 3.10+
- Django 5.0
- PostgreSQL / SQLite
- Bootstrap 5
- Google Maps API
- Font Awesome

## Įdiegimas

### 1. Klonuoti projektą
```bash
cd C:\Users\user\Desktop\programos\sellcar
```

### 2. Sukurti virtualią aplinką
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Įdiegti priklausomybes
```bash
pip install -r requirements.txt
```

### 4. Sukonfigūruoti aplinkos kintamuosius

Sukurti `.env` failą projekto šakniniame kataloge:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - default SQLite)
DB_NAME=sellcar
DB_USER=sellcar
DB_PASSWORD=sellcar
DB_HOST=localhost
DB_PORT=5432

# Google Maps API Key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### 5. Sukurti duomenų bazę
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Sukurti superuser
```bash
python manage.py createsuperuser
```

### 7. Užpildyti pradinius duomenis (optional)
```bash
python manage.py populate_data
```

### 8. Paleisti serverį
```bash
python manage.py runserver
```

Atidaryti naršyklėje: `http://127.0.0.1:8000`

## Admin Panel

Pasiekiamas: `http://127.0.0.1:8000/admin`

## Projekto struktūra
```
sellcar/
├── sellcar/              # Pagrindinis projekto aplankas
│   ├── settings.py       # Nustatymai
│   ├── urls.py           # URL maršrutai
│   └── wsgi.py
├── accounts/             # Vartotojų aplikacija
│   ├── models.py         # UserProfile modelis
│   ├── views.py          # Vartotojų vaizdai
│   └── forms.py          # Formos
├── listings/             # Skelbimų aplikacija
│   ├── models.py         # Listing, Brand, Model ir kt.
│   ├── views.py          # Skelbimų vaizdai
│   ├── forms.py          # Skelbimų formos
│   └── filters.py        # Filtrai
├── templates/            # HTML šablonai
├── static/               # Statiniai failai
├── media/                # Įkeltos nuotraukos
├── requirements.txt      # Python priklausomybės
└── manage.py
```

## Google Maps API Setup

1. Eiti į [Google Cloud Console](https://console.cloud.google.com/)
2. Sukurti naują projektą
3. Įjungti **Maps JavaScript API** ir **Places API**
4. Sukurti API raktą
5. Įdėti raktą į `.env` failą

## Pagrindinės komandos
```bash
# Sukurti migrations
python manage.py makemigrations

# Pritaikyti migrations
python manage.py migrate

# Sukurti superuser
python manage.py createsuperuser

# Rinkti static failus
python manage.py collectstatic

# Paleisti development serverį
python manage.py runserver

# Sukurti pradinius duomenis
python manage.py populate_data
```

## Pagrindiniai URL maršrutai

- `/` - Pagrindinis puslapis
- `/listings/` - Skelbimų sąrašas
- `/listings/create/` - Naujo skelbimo kūrimas
- `/listings/<slug>/` - Skelbimo peržiūra
- `/listings/map/` - Paieška žemėlapyje
- `/accounts/login/` - Prisijungimas
- `/accounts/register/` - Registracija
- `/accounts/profile/` - Vartotojo profilis
- `/admin/` - Admin panelė

## Kontaktai

Email: info@sellcar.lt
