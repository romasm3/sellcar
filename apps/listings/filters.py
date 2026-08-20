import django_filters
from .models import Listing, VehicleType, Brand, Model, FuelType, Transmission


class ListingFilter(django_filters.FilterSet):
    """Skelbimų filtravimas"""

    title = django_filters.CharFilter(lookup_expr="icontains", label="Paieška")

    vehicle_type = django_filters.ModelChoiceFilter(
        queryset=VehicleType.objects.all(), empty_label="Visi tipai", label="Tipas"
    )

    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.filter(vehicle_type__slug='cars'),
        empty_label="Visos markės", label="Markė"
    )

    model = django_filters.ModelChoiceFilter(
        queryset=Model.objects.all(), empty_label="Visi modeliai", label="Modelis"
    )

    year_min = django_filters.NumberFilter(
        field_name="year", lookup_expr="gte", label="Metai nuo"
    )
    year_max = django_filters.NumberFilter(
        field_name="year", lookup_expr="lte", label="Metai iki"
    )

    price_min = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Kaina nuo"
    )
    price_max = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Kaina iki"
    )

    mileage_min = django_filters.NumberFilter(
        field_name="mileage", lookup_expr="gte", label="Rida nuo"
    )
    mileage_max = django_filters.NumberFilter(
        field_name="mileage", lookup_expr="lte", label="Rida iki"
    )

    fuel_type = django_filters.ModelChoiceFilter(
        queryset=FuelType.objects.all(),
        empty_label="Visi kuro tipai",
        label="Kuro tipas",
    )

    transmission = django_filters.ModelChoiceFilter(
        queryset=Transmission.objects.all(),
        empty_label="Visos pavarų dėžės",
        label="Pavarų dėžė",
    )

    city = django_filters.CharFilter(lookup_expr="icontains", label="Miestas")

    condition = django_filters.ChoiceFilter(
        choices=Listing.CONDITION_CHOICES, empty_label="Visos būklės", label="Būklė"
    )

    class Meta:
        model = Listing
        fields = [
            "vehicle_type",
            "brand",
            "model",
            "fuel_type",
            "transmission",
            "condition",
            "city",
        ]
