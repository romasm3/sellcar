# apps/listings/translatable_db.py
# ═══════════════════════════════════════════════════════════
# DB reikšmės (VehicleType.name, SubCategory.name), kurias reikia versti.
#
# Šis failas niekur neimportuojamas — egzistuoja tik tam, kad
# makemessages surinktų šiuos stringus į .po failus. Rodymo metu
# jie verčiami per {{ value|tdb }} filtrą (templatetags/i18n_db.py)
# arba gettext() view'e (pvz. get_subcategories_ajax).
# ═══════════════════════════════════════════════════════════

from django.utils.translation import gettext_lazy as _


VEHICLE_TYPE_NAMES = [
    _('Cars'), _('Minibuses, Buses & Campers'), _('Motorcycles & Moto Gear'),
    _('Trucks & Commercial'), _('Parts'), _('Tyres & Wheels'),
    _('Boats & Water Transport'), _('Trailers & Semi-trailers'),
    _('Construction & Warehouse Equipment'), _('Agricultural & Forestry'),
    _('Bicycles & Scooters'), _('Services'), _('Car Rental'), _('Planes & Aircraft'),
    _('Aircraft Parts'), _('Vilkikai'), _('Autotraukiniai, autovežiai'),
    _('Komunalinio ūkio transportas'), _('Krovimo ir sandėliavimo technika'),
    _('Automobilių supirkimas'), _('Video, audio, navigacijos'), _('Miško ūkio technika'),
    _('Turistiniai nameliai'),
]

SUBCATEGORY_NAMES = [
    _('Aircraft Accessories'), _('Airplanes'), _('Avionics'), _('Balers'), _('Bicycles'),
    _('Boat Trailers'), _('Boats'), _('Body Repair'), _('Bulldozers'), _('Buses'),
    _('Campers'), _('Car Parts'), _('Car Service'), _('Car Trailers'), _('Car Wash'),
    _('Caravans'), _('Cargo Minibuses over 3.5t'), _('Cargo Minibuses up to 3.5t'),
    _('Combine Harvesters'), _('Compactors'), _('Concrete Mixers'), _('Cranes'),
    _('Cultivators'), _('Curtainsider Trailers'), _('Diagnostics'), _('Drones'),
    _('Electric Bikes'), _('Electric Scooters'), _('Engine Parts'), _('Excavators'),
    _('Fishing Boats'), _('Flatbed Trailers'), _('Forestry Machines'), _('Forklifts'),
    _('Helicopters'), _('Inflatable Boats'), _('Jet Skis'),
    _('Limuzinų, vestuvių transporto nuoma'), _('Loaders'), _('Moto Gear, accessories'),
    _('Moto Parts'), _('Motociklų nuoma'), _('Motorboats'), _('Motorcycles'),
    # Moto gear 3rd level
    _('Helmets'), _('Jackets'), _('Pants'), _('Suits / Combinations'), _('Gloves'),
    _('Boots'), _('Protective gear'), _('Travel bags'), _('Goggles & other gear'),
    _('Other Agricultural'), _('Other Construction'), _('Other Trailers'),
    _('Other Watercraft'), _('Painting'), _('Passenger Minibuses'), _('Ploughs'),
    _('Refrigerator Trailers'), _('Rims'), _('Sailboats'), _('Semi-Trucks / Tractors'),
    _('Semi-trailers'), _('Single moto part'), _('Single part / parts kit'), _('Sprayers'),
    _('Statybinės technikos priedai'), _('Sunkiojo transporto, priekabų nuoma'),
    _('Tipper Trailers'), _('Towing'), _('Tractors'), _('Truck Parts'), _('Trucks'),
    _('Tyres'), _('Ultralight Aircraft'), _('Vans'), _('Vehicle Transporters'),
    _('Whole car for parts'), _('Whole moto for parts'), _('Whole truck for parts'),
    _('Yachts'),
]


FUEL_AND_TRANSMISSION_NAMES = [
    _('Automatic'), _('CVT'), _('Diesel'), _('Diesel / Electric (Hybrid)'),
    _('Diesel / Electric (Plug-in)'), _('Electric'), _('Ethanol'), _('LPG'), _('Manual'),
    _('Other'), _('Petrol'), _('Petrol / CNG'), _('Petrol / Electric (Hybrid)'),
    _('Petrol / Electric (Plug-in)'), _('Petrol / Electric / LPG'), _('Petrol / LPG'),
    _('Semi-automatic'),
]
