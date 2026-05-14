"""
Populate default pricing plans for all vehicle types.

Usage: python manage.py populate_pricing_plans
"""
from django.core.management.base import BaseCommand
from apps.listings.models import VehicleType, PricingPlan


DEFAULT_PLANS = {
    'motorcycles': [
        {
            'duration_days': 30,
            'price': 15.99,
            'old_price': None,
            'discount_percent': None,
            'is_popular': False,
            'order': 1,
            'boost_days': 0,
            'vip_days': 0,
            'homepage_ad_days': 0,
        },
        {
            'duration_days': 60,
            'price': 18.99,
            'old_price': 47.99,
            'discount_percent': 60,
            'is_popular': True,
            'order': 2,
            'boost_days': 6,
            'vip_days': 0,
            'homepage_ad_days': 0,
        },
        {
            'duration_days': 90,
            'price': 19.99,
            'old_price': 82.81,
            'discount_percent': 76,
            'is_popular': False,
            'order': 3,
            'boost_days': 6,
            'vip_days': 5,
            'homepage_ad_days': 1,
        },
    ],
    'cars': [
        {
            'duration_days': 30,
            'price': 19.99,
            'old_price': None,
            'discount_percent': None,
            'is_popular': False,
            'order': 1,
            'boost_days': 0,
            'vip_days': 0,
            'homepage_ad_days': 0,
        },
        {
            'duration_days': 60,
            'price': 22.99,
            'old_price': 57.99,
            'discount_percent': 60,
            'is_popular': True,
            'order': 2,
            'boost_days': 6,
            'vip_days': 0,
            'homepage_ad_days': 0,
        },
        {
            'duration_days': 90,
            'price': 23.99,
            'old_price': 95.99,
            'discount_percent': 75,
            'is_popular': False,
            'order': 3,
            'boost_days': 6,
            'vip_days': 5,
            'homepage_ad_days': 1,
        },
    ],
}


class Command(BaseCommand):
    help = 'Populate default pricing plans for motorcycles and cars'

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for vt_slug, plans in DEFAULT_PLANS.items():
            try:
                vt = VehicleType.objects.get(slug=vt_slug)
            except VehicleType.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'VehicleType "{vt_slug}" not found, skipping')
                )
                continue

            for plan_data in plans:
                plan, created = PricingPlan.objects.get_or_create(
                    vehicle_type=vt,
                    duration_days=plan_data['duration_days'],
                    defaults=plan_data,
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created: {vt.name} - {plan.duration_days}d - ${plan.price}'
                        )
                    )
                else:
                    skipped_count += 1
                    self.stdout.write(
                        f'Exists:  {vt.name} - {plan.duration_days}d - ${plan.price}'
                    )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created: {created_count}, Skipped: {skipped_count}'
            )
        )