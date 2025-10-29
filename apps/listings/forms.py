from django import forms
from .models import (
    Listing,
    ListingImage,
    VehicleType,
    Brand,
    Model,
    FuelType,
    Transmission,
)


class ListingCreateForm(forms.ModelForm):
    """Skelbimo kūrimo forma"""

    class Meta:
        model = Listing
        fields = [
            "vehicle_type",
            "brand",
            "model",
            "title",
            "description",
            "year",
            "mileage",
            "fuel_type",
            "transmission",
            "engine_capacity",
            "power",
            "color",
            "condition",
            "vin",
            "registration_number",
            "first_registration",
            "price",
            "negotiable",
            "city",
            "address",
            "latitude",
            "longitude",
            "features",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "features": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Pvz: Kondicionierius, Lieti ratlankiai, Parkavimo sistema",
                }
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2030}
            ),
            "mileage": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "engine_capacity": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            ),
            "power": forms.NumberInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "vin": forms.TextInput(attrs={"class": "form-control", "maxlength": 17}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "first_registration": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "vehicle_type": forms.Select(attrs={"class": "form-control"}),
            "brand": forms.Select(attrs={"class": "form-control"}),
            "model": forms.Select(attrs={"class": "form-control"}),
            "fuel_type": forms.Select(attrs={"class": "form-control"}),
            "transmission": forms.Select(attrs={"class": "form-control"}),
            "condition": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pridėti placeholder tekstus
        self.fields["title"].widget.attrs["placeholder"] = "Pvz: BMW 320d 2018m."
        self.fields["city"].widget.attrs["placeholder"] = "Vilnius"
        self.fields["address"].widget.attrs["placeholder"] = (
            "Gatvės pavadinimas ir numeris"
        )


class ListingImageForm(forms.ModelForm):
    """Nuotraukų įkėlimo forma"""

    class Meta:
        model = ListingImage
        fields = ["image", "caption", "is_main"]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nuotraukos aprašymas (neprivaloma)",
                }
            ),
            "is_main": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ListingSearchForm(forms.Form):
    """Paieškos forma"""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ieškoti pagal pavadinimą, markę, modelį...",
            }
        ),
    )

    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.all(),
        required=False,
        empty_label="Visi tipai",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label="Visos markės",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    model = forms.ModelChoiceField(
        queryset=Model.objects.all(),
        required=False,
        empty_label="Visi modeliai",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    fuel_type = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        required=False,
        empty_label="Visi kuro tipai",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    transmission = forms.ModelChoiceField(
        queryset=Transmission.objects.all(),
        required=False,
        empty_label="Visos pavarų dėžės",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    year_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Metai nuo", "min": 1900}
        ),
    )

    year_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Metai iki", "max": 2030}
        ),
    )

    price_from = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Kaina nuo (€)", "min": 0}
        ),
    )

    price_to = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Kaina iki (€)", "min": 0}
        ),
    )

    mileage_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Rida nuo (km)", "min": 0}
        ),
    )

    mileage_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Rida iki (km)", "min": 0}
        ),
    )
