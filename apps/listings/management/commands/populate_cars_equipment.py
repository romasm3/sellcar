from django.core.management.base import BaseCommand
from apps.listings.models import Equipment


class Command(BaseCommand):
    help = 'Populate Equipment DB with all 108 cars features matching template'

    def handle(self, *args, **options):
        # All 108 features iz tavo dabartinio template'o
        # Format: (category, slug, name)
        FEATURES = [
            # ─── INTERIOR (16) ───
            ('interior', 'auto_heater', 'Auto heater'),
            ('interior', 'electric_seats', 'Electric seats'),
            ('interior', 'leather_interior', 'Leather interior'),
            ('interior', 'heated_seats', 'Heated seats'),
            ('interior', 'cargo_cover', 'Cargo cover'),
            ('interior', 'memory_seats', 'Memory seats'),
            ('interior', 'ac', 'Air conditioning'),
            ('interior', 'tinted_windows', 'Tinted windows'),
            ('interior', 'multi_steering', 'Multi-function steering'),
            ('interior', 'climate_control', 'Climate control'),
            ('interior', 'sport_seats', 'Sport seats'),
            ('interior', 'velour_interior', 'Velour interior'),
            ('interior', 'electric_windows', 'Electric windows'),
            ('interior', 'massage_seats', 'Massage seats'),
            ('interior', 'heated_steering', 'Heated steering wheel'),
            ('interior', 'ventilated_seats', 'Ventilated seats'),

            # ─── EXTERIOR (15) ───
            ('exterior', 'auto_folding_mirrors', 'Auto-folding mirrors'),
            ('exterior', 'led_lights', 'LED lights'),
            ('exterior', 'headlight_washer', 'Headlight washer'),
            ('exterior', 'summer_tires', 'Summer tire set'),
            ('exterior', 'soft_close', 'Soft-close doors'),
            ('exterior', 'alloy_wheels', 'Alloy wheels'),
            ('exterior', 'fog_lights', 'Fog lights'),
            ('exterior', 'xenon_lights', 'Xenon lights'),
            ('exterior', 'tow_hitch', 'Tow hitch'),
            ('exterior', 'matrix_lights', 'Matrix lights'),
            ('exterior', 'sunroof', 'Sunroof'),
            ('exterior', 'winter_tires', 'Winter tire set'),
            ('exterior', 'led_drl', 'LED daytime lights'),
            ('exterior', 'panoramic_roof', 'Panoramic roof'),
            ('exterior', 'roof_rails', 'Roof rails'),

            # ─── ELECTRONICS (20) ───
            ('electronics', 'parking_sensors', 'Parking sensors'),
            ('electronics', 'adjustable_steering', 'Adjustable steering'),
            ('electronics', 'touchscreen', 'Touchscreen'),
            ('electronics', 'digital_dashboard', 'Digital dashboard'),
            ('electronics', 'auto_lights', 'Auto lights'),
            ('electronics', 'heated_windshield', 'Heated windshield'),
            ('electronics', 'navigation', 'Navigation / GPS'),
            ('electronics', 'start_stop', 'Start-Stop system'),
            ('electronics', 'cruise_control', 'Cruise control'),
            ('electronics', 'electric_trunk', 'Electric trunk'),
            ('electronics', 'paddle_shifters', 'Paddle shifters'),
            ('electronics', 'heated_mirrors', 'Heated mirrors'),
            ('electronics', 'keyless_entry', 'Keyless entry'),
            ('electronics', 'rain_sensor', 'Rain sensor'),
            ('electronics', 'dimming_mirror', 'Auto-dimming mirror'),
            ('electronics', 'lcd_screen', 'LCD screen'),
            ('electronics', 'hud', 'Head-up display (HUD)'),
            ('electronics', 'virtual_mirrors', 'Virtual mirrors'),
            ('electronics', 'wireless_phone_charging', 'Wireless phone charging'),
            ('electronics', 'electric_mirrors', 'Electric mirrors'),

            # ─── SAFETY (23) ───
            ('safety', 'camera_360', '360° camera'),
            ('safety', 'esp', 'ESP (Stability Control)'),
            ('safety', 'night_vision', 'Night vision assistant'),
            ('safety', 'front_camera', 'Front camera'),
            ('safety', 'blind_spot', 'Blind-spot monitoring'),
            ('safety', 'rear_camera', 'Rear camera'),
            ('safety', 'fatigue_alert', 'Fatigue alert'),
            ('safety', 'alarm_immobilizer', 'Alarm / Immobilizer'),
            ('safety', 'cruise_assist', 'Adaptive cruise control'),
            ('safety', 'hill_hold', 'Hill-hold assist'),
            ('safety', 'airbags', 'Airbags'),
            ('safety', 'collision_prevention', 'Collision prevention'),
            ('safety', 'auto_parking', 'Auto parking'),
            ('safety', 'isofix', 'ISOFIX (child seats)'),
            ('safety', 'tire_pressure', 'Tire pressure monitoring'),
            ('safety', 'long_range_assist', 'Long-range light assist'),
            ('safety', 'abs', 'Emergency brake (ABS)'),
            ('safety', 'lane_assist', 'Lane keeping assist'),
            ('safety', 'ecall', 'Emergency call (eCall)'),
            ('safety', 'traction_control', 'Traction control system'),
            ('safety', 'dynamic_cornering', 'Dynamic cornering lights'),
            ('safety', 'traffic_sign', 'Traffic sign recognition'),
            ('safety', 'follow_assist', 'Follow assist'),

            # ─── AUDIO/VIDEO (15) ───
            ('audio_video', 'carplay_android', 'Apple CarPlay / Android Auto'),
            ('audio_video', 'cd_player', 'CD player'),
            ('audio_video', 'hands_free', 'Hands-free system'),
            ('audio_video', 'usb', 'USB port'),
            ('audio_video', 'audio_player', 'Audio player'),
            ('audio_video', 'cd_changer', 'CD changer'),
            ('audio_video', 'mp3_player', 'MP3 player'),
            ('audio_video', 'usb_c', 'USB Type-C port'),
            ('audio_video', 'aux', 'AUX port'),
            ('audio_video', 'dvd_player', 'DVD player'),
            ('audio_video', 'premium_audio', 'Premium audio system'),
            ('audio_video', 'subwoofer', 'Subwoofer'),
            ('audio_video', 'bluetooth', 'Bluetooth'),
            ('audio_video', 'hifi', 'HiFi audio system'),
            ('audio_video', 'tv', 'TV screen'),

            # ─── OTHER (13) ───
            ('other', 'spare_tire', 'Spare tire'),
            ('other', 'not_taxi', 'Not used as taxi'),
            ('other', 'leasing', 'For sale on leasing'),
            ('other', 'disabled_access', 'Disabled access'),
            ('other', 'from_usa', 'From USA'),
            ('other', 'remote_start', 'Remote start'),
            ('other', 'prepared_sport', 'Sport-prepared'),
            ('other', 'service_book', 'Service book'),
            ('other', 'warranty', 'Warranty'),
            ('other', 'extra_power', 'Increased engine power'),
            ('other', 'air_suspension', 'Air suspension'),
            ('other', 'vin_listed', 'Listing with VIN'),
            ('other', 'extra_keys', 'Extra key set'),

            # ─── ELECTRIC (6) ───
            ('electric', 'apva_grant', 'APVA grant unused'),
            ('electric', 'bidirectional', 'Bidirectional charging'),
            ('electric', 'heat_pump', 'Heat pump'),
            ('electric', 'three_phase', 'Three-phase charging'),
            ('electric', 'battery_warranty', 'Battery warranty'),
            ('electric', 'fast_charging', 'Fast charging'),
        ]

        created_count = 0
        existing_count = 0
        skipped_count = 0

        for category, slug, name in FEATURES:
            # Try by name + category match first (avoid duplicates)
            existing = Equipment.objects.filter(
                category=category,
                name=name,
            ).first()

            if existing:
                existing_count += 1
                continue

            # Check if slug field exists on model
            try:
                eq = Equipment(category=category, name=name)
                if hasattr(Equipment, 'slug') or 'slug' in [f.name for f in Equipment._meta.fields]:
                    eq.slug = slug
                eq.save()
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  [+] [{category}] {name}'
                ))
            except Exception as e:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(
                    f'  [!] [{category}] {name} — {e}'
                ))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Created: {created_count}, Existing: {existing_count}, Skipped: {skipped_count}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Total cars equipment in DB: {Equipment.objects.exclude(category__startswith="truck_").exclude(category="gear").count()}'
        ))