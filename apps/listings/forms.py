from django import forms
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
        label="Vehicle Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        label="Brand",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_brand'})
    )

    model = forms.ModelChoiceField(
        queryset=Model.objects.none(),
        label="Model",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_model'})
    )

    year = forms.IntegerField(
        label="Manufacturing Year",
        widget=forms.Select(attrs={'class': 'form-control'},
                          choices=[(y, y) for y in range(2025, 1949, -1)])
    )

    first_registration_month = forms.IntegerField(
        label="Registration Month",
        widget=forms.Select(attrs={'class': 'form-control'},
                          choices=[(m, m) for m in range(1, 13)])
    )

    vin = forms.CharField(
        label="VIN Code",
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

    video_url = forms.URLField(
        label="Upload Video (YouTube or other URL)",
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
        label="Body Type",
        choices=Listing.BODY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    fuel_type = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        label="Fuel Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    transmission = forms.ModelChoiceField(
        queryset=Transmission.objects.all(),
        label="Transmission",
        widget=forms.RadioSelect()
    )

    doors = forms.ChoiceField(
        label="Number of Doors",
        choices=Listing.DOOR_CHOICES,
        widget=forms.RadioSelect()
    )

    condition = forms.ChoiceField(
        label="Condition",
        choices=Listing.CONDITION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    color = forms.CharField(
        label="Color",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Black'})
    )

    mileage = forms.IntegerField(
        label="Mileage (km)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-',
            'min': '0'
        })
    )

    engine_capacity = forms.DecimalField(
        label="Engine Capacity (L)",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'L',
            'step': '0.1'
        })
    )

    power = forms.IntegerField(
        label="Power (kW)",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'kW',
            'min': '0'
        })
    )


# STEP 4: Equipment
class Step4EquipmentForm(forms.Form):
    """Step 4: Additional Equipment"""

    features_text = forms.CharField(
        label="Search Features",
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
        # Group equipment by category
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
        label="Price in Lithuania, with taxes, €",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '-',
            'min': '0',
            'step': '0.01'
        })
    )

    negotiable = forms.BooleanField(
        label="Show additional price without VAT",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# STEP 6: Description
class Step6DescriptionForm(forms.Form):
    """Step 6: Listing Description"""

    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Description'
        })
    )


# STEP 7: Contact
class Step7ContactForm(forms.Form):
    """Step 7: Contact Information"""

    COUNTRY_CHOICES = [
        ('LT', 'Lithuania'),
        ('LV', 'Latvia'),
        ('EE', 'Estonia'),
        ('PL', 'Poland'),
        ('DE', 'Germany'),
    ]

    country = forms.ChoiceField(
        label="Country",
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )

    phone = forms.CharField(
        label="Contact Phone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+37067112478'
        })
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )

    show_additional_phone = forms.BooleanField(
        label="Additional Phone",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    agree_terms = forms.BooleanField(
        label="I agree to the Terms and Conditions and Privacy Policy",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    agree_newsletter = forms.BooleanField(
        label="Newsletter and offers",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# Image Upload Form - FIXED: Removed 'multiple': True
class ListingImageForm(forms.ModelForm):
    """Image Upload Form"""

    class Meta:
        model = ListingImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                # REMOVED: 'multiple': True  - Django ModelForm doesn't support this
            })
        }
