"""
Custom admin grouping.
Reorganizes admin sidebar into logical groups while preserving
the default Django admin look and feel.

Any model NOT in MODEL_GROUPS will appear in 'OTHER' group at the bottom,
so nothing ever gets hidden.
"""
from django.contrib import admin


# Group definitions: order matters — groups appear in this order
MODEL_GROUPS = [
    ("MESSAGING", [
        "broadcasts.broadcast",
        "listings.emailscenario",
    ]),
    ("USERS & ACCOUNTS", [
        "auth.user",
        "auth.group",
        "accounts.profile",
    ]),
    ("LISTINGS — CARS", [
        "listings.listing",
        "listings.listingimage",
    ]),
    ("MOTORCYCLES", [
        "listings.motorcyclebrand",
        "listings.motorcyclemodel",
    ]),
    ("TRUCKS", [
        "listings.truck",
        "listings.truckbrand",
        "listings.truckmodel",
        "listings.truckimage",
        "listings.truckequipment",
        "listings.savedtruck",
        "listings.savedtrucknotification",
        "listings.truckview",
        "listings.truckimpression",
        "listings.trucksalesrecord",
    ]),
    ("VEHICLE CATALOG", [
        "listings.vehicletype",
        "listings.subcategory",
        "listings.brand",
        "listings.model",
        "listings.fueltype",
        "listings.transmission",
        "listings.equipment",
    ]),
    ("PRICING & PAYMENTS", [
        "listings.pricingplan",
        "listings.pricingsettings",
        "listings.pricemultipliertier",
        "listings.promocode",
        "listings.promocodeusage",
    ]),
]


def get_app_list(self, request, app_label=None):
    """
    Override default admin app_list to return custom groups.
    Any model not assigned to a group ends up in 'OTHER'.
    """
    # Get all registered models (default Django logic)
    app_dict = self._build_app_dict(request, app_label)

    # Flatten: build a dict of "app_label.model_name" -> model_dict
    flat_models = {}
    for app in app_dict.values():
        for model in app["models"]:
            key = f"{app['app_label']}.{model['object_name'].lower()}"
            flat_models[key] = model

    # Build custom grouped output
    grouped_apps = []
    used_keys = set()

    for group_name, model_keys in MODEL_GROUPS:
        group_models = []
        for key in model_keys:
            if key in flat_models:
                group_models.append(flat_models[key])
                used_keys.add(key)

        if group_models:
            grouped_apps.append({
                "name": group_name,
                "app_label": group_name.lower().replace(" ", "_").replace("&", "and"),
                "app_url": "",
                "has_module_perms": True,
                "models": group_models,
            })

    # Catch-all: any registered model not assigned to a group goes here
    leftover = [m for k, m in flat_models.items() if k not in used_keys]
    if leftover:
        grouped_apps.append({
            "name": "OTHER",
            "app_label": "other",
            "app_url": "",
            "has_module_perms": True,
            "models": leftover,
        })

    return grouped_apps


# Monkey-patch the default admin site
admin.AdminSite.get_app_list = get_app_list
