from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    Listing,
    ListingImage,
    VehicleType,
    Brand,
    Model,
    FuelType,
    Transmission,
    Equipment,
)


# STEP 1: Brand, Model, VIN
class Step1BasicInfoForm(forms.Form):
    """Step 1: Brand, Model, Year, First Registration"""

    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.all(),
        label=_("Vehicle Type"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.filter(vehicle_type__slug='cars'),
        label=_("Brand"),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_brand'})
    )

    model = forms.ModelChoiceField(
        queryset=Model.objects.none(),
        label=_("Model"),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_model'})
    )

    year = forms.IntegerField(
        label=_("Manufacturing Year"),
        widget=forms.Select(attrs={'class': 'form-control'},
                          choices=[(y, y) for y in range(2025, 1949, -1)])
    )

    first_registration_month = forms.IntegerField(
        label=_("Registration Month"),
        widget=forms.Select(attrs={'class': 'form-control'},
                          choices=[(m, m) for m in range(1, 13)])
    )

    vin = forms.CharField(
        label=_("VIN Code"),
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'VIN code (optional)',
            'maxlength': '17'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = Model.objects.filter(brand_id=brand_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('brand'):
            self.fields['model'].queryset = self.initial['brand'].models.order_by('name')


# STEP 2: Photos and Video
class Step2MediaForm(forms.Form):
    """Step 2: Upload Photos and Video"""

    brand = forms.IntegerField(required=False)
    model = forms.IntegerField(required=False)
    year = forms.IntegerField(required=False)

    video_url = forms.URLField(
        label=_("Upload Video (YouTube or other URL)"),
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://'
        })
    )


# STEP 3: Vehicle Data
class Step3VehicleDataForm(forms.Form):
    """Step 3: Technical Vehicle Data"""

    body_type = forms.ChoiceField(
        label=_("Body Type"),
        choices=[('', '---------')] + Listing.BODY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    fuel_type = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        label=_("Fuel Type"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    transmission = forms.ModelChoiceField(
        queryset=Transmission.objects.all(),
        label=_("Transmission"),
        widget=forms.RadioSelect()
    )

    doors = forms.ChoiceField(
        label=_("Number of Doors"),
        choices=Listing.DOOR_CHOICES,
        widget=forms.RadioSelect()
    )

    condition = forms.ChoiceField(
        label=_("Condition"),
        choices=[('', '---------')] + Listing.CONDITION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    color = forms.ChoiceField(
        label=_("Color"),
        choices=[('', '---------')] + Listing.COLOR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # 13. Defects — REQUIRED, tu\u0161\u010dias default (---------), vartotojas turi pasirinkti vien\u0105 i\u0161 variant\u0173 (\u012fskaitant "No defects")
    defects = forms.ChoiceField(
        label=_("Defects"),
        choices=[('', '---------')] + list(Listing.DEFECT_CHOICES),
        required=True,
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    steering = forms.ChoiceField(
        label=_("Steering"),
        choices=[('', '---------')] + Listing.STEERING_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    mileage = forms.IntegerField(
        label=_("Mileage (km)"),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-',
            'min': '0'
        })
    )

    engine_capacity = forms.DecimalField(
        label=_("Engine Capacity (L)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'L',
            'step': '0.1'
        })
    )

    power = forms.IntegerField(
        label=_("Power (kW)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'kW',
            'min': '0'
        })
    )

    # Extended fields
    drive_type = forms.ChoiceField(
        label=_("Drive Type"),
        choices=[('', '---------')] + Listing.DRIVE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    seats = forms.ChoiceField(
        label=_("Number of Seats"),
        choices=[('', '---------')] + Listing.SEATS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cylinders = forms.ChoiceField(
        label=_("Cilindrų skaičius"),
        choices=[('', '---------')] + Listing.CYLINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    gear_count = forms.ChoiceField(
        label=_("Pavarų skaičius"),
        choices=[('', '---------')] + Listing.GEAR_COUNT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    manufacturer_warranty = forms.BooleanField(
        label=_("Gamintojo garantija"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 rounded'})
    )

    sdk_number = forms.CharField(
        label=_("SDK kodas"),
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': _('VĮ Regitra')})
    )

    rim_size = forms.ChoiceField(
        label=_("Ratlankiai"),
        choices=[('', '---------')] + Listing.RIM_SIZE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    climate = forms.ChoiceField(
        label=_("Climate Control"),
        choices=[('', '---------')] + Listing.CLIMATE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    curb_weight = forms.IntegerField(
        label=_("Curb Weight (kg)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'kg',
            'min': '0'
        })
    )

    euro_standard = forms.ChoiceField(
        label=_("Euro Standard"),
        choices=[('', '---------')] + Listing.EURO_STANDARD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    co2_emission = forms.IntegerField(
        label=_("CO\u2082 Emission (g/km)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'g/km',
            'min': '0'
        })
    )

    fuel_consumption_city = forms.DecimalField(
        label=_("Fuel Consumption City (l/100km)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-',
            'step': '0.1',
            'min': '0'
        })
    )

    fuel_consumption_highway = forms.DecimalField(
        label=_("Fuel Consumption Highway (l/100km)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-',
            'step': '0.1',
            'min': '0'
        })
    )

    fuel_consumption_combined = forms.DecimalField(
        label=_("Fuel Consumption Combined (l/100km)"),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-',
            'step': '0.1',
            'min': '0'
        })
    )

    origin_country = forms.ChoiceField(
        label=_("Origin Country"),
        choices=[('', '---------')] + Listing.COUNTRY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    technical_inspection_month = forms.ChoiceField(
        label=_("Technical Inspection Month"),
        choices=[('', '-')] + [(str(m), f'{m:02d}') for m in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    technical_inspection_year = forms.ChoiceField(
        label=_("Technical Inspection Year"),
        choices=[('', '-')] + [(str(y), str(y)) for y in range(2024, 2036)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


# STEP 4: Equipment
class Step4EquipmentForm(forms.Form):
    """Step 4: Additional Equipment"""

    features_text = forms.CharField(
        label=_("Search Features"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type feature name...'
        })
    )

    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        equipment_by_category = {}
        for equipment in Equipment.objects.all():
            category = equipment.get_category_display()
            if category not in equipment_by_category:
                equipment_by_category[category] = []
            equipment_by_category[category].append(equipment)

        self.equipment_by_category = equipment_by_category


# STEP 5: Price
class Step5PriceForm(forms.Form):
    """Step 5: Price"""

    price = forms.DecimalField(
        label=_("Price (\u20ac)"),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter price',
            'min': '0',
            'step': '0.01'
        })
    )

    negotiable = forms.BooleanField(
        label=_("Price is negotiable"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# STEP 6: Description
class Step6DescriptionForm(forms.Form):
    """Step 6: Listing Description"""

    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Describe your vehicle...'
        })
    )


# STEP 7: Contact & Location
class Step7ContactForm(forms.Form):
    """Step 7: Contact Information & Location"""

    # 14. US pridetas prie country choices
    COUNTRY_CHOICES = [
        ('LT', 'Lithuania'),
        ('LV', 'Latvia'),
        ('EE', 'Estonia'),
        ('PL', 'Poland'),
        ('DE', 'Germany'),
        ('NL', 'Netherlands'),
        ('BE', 'Belgium'),
        ('FR', 'France'),
        ('IT', 'Italy'),
        ('ES', 'Spain'),
        ('AT', 'Austria'),
        ('CZ', 'Czech Republic'),
        ('SK', 'Slovakia'),
        ('HU', 'Hungary'),
        ('RO', 'Romania'),
        ('BG', 'Bulgaria'),
        ('SE', 'Sweden'),
        ('DK', 'Denmark'),
        ('FI', 'Finland'),
        ('NO', 'Norway'),
        ('GB', 'United Kingdom'),
        ('IE', 'Ireland'),
        ('CH', 'Switzerland'),
        ('US', 'United States'),
    ]

    country = forms.ChoiceField(
        label=_("Country"),
        choices=COUNTRY_CHOICES,
        initial='LT',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # 14. City laukas — NEPRIVALOMAS (kai pasirenka US, naudojama valstija)
    city = forms.CharField(
        label=_("City"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Vilnius'
        })
    )

    postal_code = forms.CharField(
        label=_("Postal Code"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 90210'
        })
    )

    address = forms.CharField(
        label=_("Street Address"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 123 Main St'
        })
    )

    hide_exact_address = forms.BooleanField(
        label=_("Hide exact address (show only city/area on map)"),
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    phone = forms.CharField(
        label=_("Contact Phone"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567'
        })
    )

    email = forms.EmailField(
        label=_("Email Address"),
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )

    show_phone = forms.BooleanField(
        label=_("Show phone number in listing"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    agree_terms = forms.BooleanField(
        label=_("I agree to the Terms and Conditions and Privacy Policy"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    agree_newsletter = forms.BooleanField(
        label=_("Subscribe to newsletter and special offers"),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # 14. Custom validation: city OR (US + state) reikalinga
    def clean(self):
        cleaned = super().clean()
        country = cleaned.get('country')
        city = cleaned.get('city', '').strip()
        # state ateina kaip POST['state'] — netrauke per form, validacija bus view'e
        if country != 'US' and not city:
            self.add_error('city', 'City is required.')
        return cleaned


# Image Upload Form
class ListingImageForm(forms.ModelForm):
    """Image Upload Form"""

    class Meta:
        model = ListingImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }