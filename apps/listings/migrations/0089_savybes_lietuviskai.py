"""Savybės — lietuviški pavadinimai ir etalono grupavimas.

Pervadinam VIETOJE (ne kuriam naujų eilučių), todėl visi esami skelbimų
pažymėjimai išlieka — M2M nuorodos rodo į tą patį įrašą. Dublikatų
pažymėjimai perkeliami į kanoninę eilutę, o pati eilutė iškeliama į
„legacy" kategoriją: NIEKO NETRINAM, tik nebeberodom automobilių formoje.
"""
from django.db import migrations

AUTO_KAT = ['interior', 'exterior', 'electronics', 'safety',
            'audio_video', 'other', 'electric']

PERVADINTI = {'Auto heater': ('Autonominis šildymas', 'interior'), 'Cargo cover': ('Bagažinės uždangalas', 'interior'), 'Multi-function steering': ('Daugiafunkcinis vairas', 'interior'), 'Memory seats': ('Elektra valdomos sėdynės su atmintimi', 'interior'), 'Massage seats': ('Masažinės sėdynės', 'interior'), 'Heated steering wheel': ('Šildomas vairas', 'interior'), 'Sport seats': ('Sportinės sėdynės', 'interior'), 'Tinted windows': ('Tamsinti stiklai', 'interior'), 'Velour interior': ('Veliūro salonas', 'interior'), 'Electric windows': ('El. langai', 'interior'), 'Electric seats': ('Elektra valdomos sėdynės', 'interior'), 'Climate control': ('Klimato kontrolė', 'interior'), 'Leather interior': ('Odinis salonas', 'interior'), 'Air conditioning': ('Oro kondicionierius', 'interior'), 'Heated seats': ('Šildomos sėdynės', 'interior'), 'Ventilated seats': ('Ventiliuojamos sėdynės', 'interior'), 'Auto-folding mirrors': ('Automatiškai užsilenkiantys veidrodėliai', 'exterior'), 'Soft-close doors': ('Durelių pritraukimas', 'exterior'), 'Tow hitch': ('Kablys', 'exterior'), 'LED daytime lights': ('LED dienos žibintai', 'exterior'), 'LED headlights': ('LED žibintai', 'exterior'), 'Alloy wheels': ('Lengvo lydinio ratlankiai', 'exterior'), 'Matrix lights': ('Matriciniai žibintai', 'exterior'), 'Panoramic roof': ('Panoraminis stogas', 'exterior'), 'Headlight washer': ('Priekinių žibintų plovimo įtaisas', 'exterior'), 'Fog lights': ('Rūko žibintai', 'exterior'), 'Roof rails': ('Stogo bagažinės laikikliai', 'exterior'), 'Summer tire set': ('Vasarinių padangų komplektas', 'exterior'), 'Xenon headlights': ('Žibintai „Xenon“', 'exterior'), 'Winter tire set': ('Žieminių padangų komplektas', 'exterior'), 'Sunroof': ('Stoglangis', 'exterior'), 'Auto lights': ('Automatiškai įsijungiantys žibintai', 'electronics'), 'Wireless phone charging': ('Bevielis telefono krovimas', 'electronics'), 'Electric mirrors': ('El. reguliuojami veidrodėliai', 'electronics'), 'Adjustable steering': ('Elektra reguliuojama vairo padėtis', 'electronics'), 'Heated windshield': ('Elektra šildomas priekinis stiklas', 'electronics'), 'Electric trunk': ('Elektra valdomas bagažinės dangtis', 'electronics'), 'Rain sensor': ('Kritulių jutiklis', 'electronics'), 'LCD screen': ('LCD ekranas', 'electronics'), 'Touchscreen': ('Liečiamas ekranas', 'electronics'), 'Navigation / GPS': ('Navigacija/GPS', 'electronics'), 'Paddle shifters': ('Pavarų perjungimas prie vairo', 'electronics'), 'Auto-dimming mirror': ('Pritemstantis veidrodėlis', 'electronics'), 'Head-up display (HUD)': ('Projekcinis ekranas ant stiklo (HUD)', 'electronics'), 'Heated mirrors': ('Šildomi veidrodėliai', 'electronics'), 'Digital dashboard': ('Skaitmeninis prietaisų skydelis', 'electronics'), 'Start-Stop system': ('Start-Stop sistema', 'electronics'), 'Virtual mirrors': ('Virtualūs veidrodėliai', 'electronics'), 'Parking sensors': ('Atstumo jutiklių sistema', 'electronics'), 'Keyless entry': ('Beraktė užvedimo sistema', 'electronics'), 'Cruise control': ('Autopilotas (kruizo kontrolė)', 'electronics'), '360° camera': ('360° vaizdo kamera', 'safety'), 'Blind spot monitor': ('Aklosios zonos stebėjimo sistema', 'safety'), 'Adaptive cruise control': ('Atstumo palaikymo sistema', 'safety'), 'Auto parking': ('Automatinio parkavimo sistema', 'safety'), 'Emergency brake (ABS)': ('Avarinio stabdymo sistema', 'safety'), 'Dynamic cornering lights': ('Dinaminis posūkių apšvietimas', 'safety'), 'Hill-hold assist': ('Įkalnės stabdis', 'safety'), 'ISOFIX (child seats)': ('ISOFIX (vaiko kėdutės tvirtinimo taškai)', 'safety'), 'Lane keeping assist': ('Juostos palaikymo sistema', 'safety'), 'Traffic sign recognition': ('Kelio ženklų atpažinimo sistema', 'safety'), 'Night vision assistant': ('Naktinio matymo asistentas', 'safety'), 'Fatigue alert': ('Nuovargio įspėjimo sistema', 'safety'), 'Tire pressure monitoring': ('Padangų slėgio stebėjimo sistema', 'safety'), 'Emergency call (eCall)': ('Pagalbos iškvietimo sistema (eCall)', 'safety'), 'Front camera': ('Priekinio vaizdo kamera', 'safety'), 'Collision prevention': ('Susidūrimo prevencijos sistema', 'safety'), 'Long-range light assist': ('Tolimųjų šviesų asistentas', 'safety'), 'Traction control system': ('Traukos kontrolės sistema', 'safety'), 'Rear camera': ('Galinio vaizdo kamera', 'safety'), 'Airbags': ('Oro pagalvės', 'safety'), 'Alarm / Immobilizer': ('Signalizacija/Imobilaizeris', 'safety'), 'ESP (Stability Control)': ('ESP (stabilumo kontrolės sistema)', 'safety'), 'Apple CarPlay / Android Auto': ('Apple CarPlay / Android Auto', 'audio_video'), 'Audio player': ('Audio grotuvas', 'audio_video'), 'AUX port': ('AUX jungtis', 'audio_video'), 'Bluetooth': ('Bluetooth', 'audio_video'), 'CD player': ('CD grotuvas', 'audio_video'), 'CD changer': ('CD keitiklis', 'audio_video'), 'DVD player': ('DVD grotuvas', 'audio_video'), 'HiFi audio system': ('HiFi audio sistema', 'audio_video'), 'Hands-free system': ('Laisvų rankų įranga', 'audio_video'), 'MP3 player': ('MP3 grotuvas', 'audio_video'), 'Premium audio system': ('Papildoma audio įranga', 'audio_video'), 'TV screen': ('TV ekranas', 'audio_video'), 'USB port': ('USB jungtis', 'audio_video'), 'USB Type-C port': ('USB Type-C jungtis', 'audio_video'), 'Subwoofer': ('Žemų dažnių garsiakalbis', 'audio_video'), 'Spare tire': ('Atsarginis ratas', 'other'), 'From USA': ('Automobilis iš Amerikos', 'other'), 'Warranty': ('Garantija', 'other'), 'Extra key set': ('Keli raktų komplektai', 'other'), 'Remote start': ('Nuotolinis užvedimas', 'other'), 'Increased engine power': ('Padidinta variklio galia', 'other'), 'For sale on leasing': ('Parduodama lizingu', 'other'), 'Sport-prepared': ('Paruoštas autosportui', 'other'), 'Air suspension': ('Pneumatinė pakaba', 'other'), 'Disabled access': ('Pritaikytas neįgaliems', 'other'), 'Service book': ('Serviso knygelė', 'other'), 'Listing with VIN': ('Skelbimas su VIN', 'other'), 'APVA grant unused': ('APVA kompensacija nepanaudota', 'electric'), 'Battery warranty': ('Baterijos garantija', 'electric'), 'Bidirectional charging': ('Dvipusis energijos perdavimas', 'electric'), 'Fast charging': ('Greitasis krovimas', 'electric'), 'Heat pump': ('Šilumos siurblys', 'electric'), 'Three-phase charging': ('Trifazis krovimas', 'electric')}

SULIETI = {'Leather seats': 'Odinis salonas', 'Navigation': 'Navigacija/GPS', 'LED lights': 'LED žibintai', 'Tow hook': 'Kablys', 'Xenon lights': 'Žibintai „Xenon“', 'Blind-spot monitoring': 'Aklosios zonos stebėjimo sistema', 'Lane assist': 'Juostos palaikymo sistema', 'Follow assist': 'Atstumo palaikymo sistema', 'ESP': 'ESP (stabilumo kontrolės sistema)', 'ABS': 'Avarinio stabdymo sistema', 'Airbag (driver)': 'Oro pagalvės', 'Airbag (passenger)': 'Oro pagalvės', 'Side airbags': 'Oro pagalvės', 'Android Auto': 'Apple CarPlay / Android Auto', 'Apple CarPlay': 'Apple CarPlay / Android Auto', 'Premium sound system': 'Papildoma audio įranga', 'USB': 'USB jungtis', 'Start/Stop': 'Start-Stop sistema', 'Not used as taxi': 'Lietuvoje neeksploatuotas'}

PARKUOTI = ['4x4', 'AWD']

NAUJI = [('Valdymas balsu', 'electronics'), ('Palydovinė sekimo sistema', 'safety'), ('Lietuvoje neeksploatuotas', 'other')]


def pirmyn(apps, schema_editor):
    Equipment = apps.get_model('listings', 'Equipment')
    ListingEquipment = apps.get_model('listings', 'ListingEquipment')

    # 1. Pervadinam ir pergrupuojam esamas eilutes
    for senas, (naujas, kat) in PERVADINTI.items():
        for eq in Equipment.objects.filter(name=senas, category__in=AUTO_KAT):
            eq.name, eq.category = naujas, kat
            eq.save(update_fields=['name', 'category'])

    # 2. Dublikatai: pažymėjimus perkeliam į kanoninę eilutę
    for senas, kanoninis in SULIETI.items():
        tikslas = Equipment.objects.filter(name=kanoninis,
                                           category__in=AUTO_KAT).first()
        for eq in Equipment.objects.filter(name=senas, category__in=AUTO_KAT):
            if tikslas:
                for ryšys in ListingEquipment.objects.filter(equipment=eq):
                    jau = ListingEquipment.objects.filter(
                        listing_id=ryšys.listing_id, equipment=tikslas).exists()
                    if jau:
                        ryšys.delete()          # tas pats skelbimas jau turi
                    else:
                        ryšys.equipment = tikslas
                        ryšys.save(update_fields=['equipment'])
            eq.category = 'legacy'
            eq.save(update_fields=['category'])

    # 3. Nebeaktualios eilutės (varantieji ratai nėra savybė)
    Equipment.objects.filter(name__in=PARKUOTI,
                             category__in=AUTO_KAT).update(category='legacy')

    # 4. Trūkstami etalono įrašai
    for vardas, kat in NAUJI:
        if not Equipment.objects.filter(name=vardas, category=kat).exists():
            Equipment.objects.create(name=vardas, category=kat, order=0)


def atgal(apps, schema_editor):
    """Grąžinam angliškus pavadinimus (dublikatai lieka „legacy")."""
    Equipment = apps.get_model('listings', 'Equipment')
    for senas, (naujas, kat) in PERVADINTI.items():
        Equipment.objects.filter(name=naujas, category=kat).update(name=senas)


class Migration(migrations.Migration):

    dependencies = [('listings', '0088_ratlankiai_ir_pavadinimai')]

    operations = [migrations.RunPython(pirmyn, atgal)]
