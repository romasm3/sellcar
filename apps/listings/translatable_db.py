
# apps/listings/translatable_db.py

# DB reikšmės (SubCategory.name), kurias reikia versti.

# Šis failas niekur neimportuojamas — egzistuoja tik tam,

# kad makemessages surinktų šiuos stringus į .po failus.



from django.utils.translation import gettext_lazy as _



SUBCATEGORY_NAMES = [

    _('Buses'), _('Campers'), _('Cargo Minibuses over 3.5t'),

    _('Cargo Minibuses up to 3.5t'), _('Passenger Minibuses'),

    _('Motorcycles'), _('Moto Gear, accessories'),

    _('Trucks'), _('Vehicle Transporters'), _('Semi-Trucks / Tractors'), _('Vans'),

    _('Car Parts'), _('Moto Parts'), _('Single moto part'), _('Truck Parts'),

    _('Whole car for parts'), _('Whole moto for parts'), _('Whole truck for parts'),

    _('Single part / parts kit'),

    _('Tyres'), _('Rims'),

    _('Boats'), _('Fishing Boats'), _('Inflatable Boats'), _('Jet Skis'),

    _('Motorboats'), _('Other Watercraft'), _('Sailboats'), _('Yachts'),

    _('Boat Trailers'), _('Car Trailers'), _('Caravans'), _('Curtainsider Trailers'),

    _('Flatbed Trailers'), _('Other Trailers'), _('Refrigerator Trailers'),

    _('Semi-trailers'), _('Tipper Trailers'),

    _('Bulldozers'), _('Compactors'), _('Concrete Mixers'), _('Cranes'),

    _('Excavators'), _('Forklifts'), _('Loaders'), _('Other Construction'),

    _('Balers'), _('Combine Harvesters'), _('Cultivators'), _('Forestry Machines'),

    _('Other Agricultural'), _('Ploughs'), _('Sprayers'), _('Tractors'),

    _('Bicycles'), _('Electric Bikes'), _('Electric Scooters'),

    _('Body Repair'), _('Car Service'), _('Car Wash'), _('Diagnostics'),

    _('Painting'), _('Towing'),

    _('Airplanes'), _('Drones'), _('Helicopters'), _('Ultralight Aircraft'),

    _('Aircraft Accessories'), _('Avionics'), _('Engine Parts'),

]

