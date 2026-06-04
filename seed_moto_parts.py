from apps.listings.models import Equipment

DATA = {
    'moto_trim': ['Trim strips', 'Seats / Backrests', 'Fenders', 'Spoilers'],
    'moto_electrical': ['Wiring / Electrical', 'ECU / Computer', 'Dashboard', 'Lights', 'Generator', 'Turn signals', 'Starter'],
    'moto_cooling': ['Radiator', 'Thermostat', 'Water radiator', 'Fan', 'Oil cooler', 'Water pump'],
    'moto_engine': ['Crankshaft', 'Mufflers', 'Carburetor', 'Pistons', 'Cylinders', 'Intake manifold', 'Camshafts', 'Engine', 'Cylinder head', 'Exhaust manifold', 'Gearbox'],
    'moto_chassis': ['Shock absorber', 'Axles', 'Brake discs', 'Forks', 'Swingarm', 'Levers', 'Brake calipers', 'Handlebar', 'Chains', 'Final drive', 'Hubs', 'Sprockets', 'Driveshaft', 'Frame'],
}

created = 0
for cat, names in DATA.items():
    for name in names:
        obj, c = Equipment.objects.get_or_create(name=name, category=cat)
        if c:
            created += 1

print('done — created', created, '| total moto:', Equipment.objects.filter(category__startswith='moto_').count())