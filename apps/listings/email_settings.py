"""
═══════════════════════════════════════════════════════════════════
SellCar Email Scenarios - MASTER LIST
═══════════════════════════════════════════════════════════════════

Čia yra visų email'u SĄRAŠAS ir GLOBAL ON/OFF jungtukai.

Kaip veikia:
  - True  → scenarijus AKTYVUS (galima siųsti)
  - False → scenarijus IŠJUNGTAS (niekada nesiunčia, nesvarbu kas admin'e)

Kaip redaguoti:
  1. Keiti True/False čia, išsaugoti, restartinti serverį
  2. ARBA eik į Django admin /admin/listings/emailscenario/ ir ten junginėk
     (tai neveiks jei čia False - čia yra "hard kill switch")

Kaip pridėti naują scenarijų:
  1. Pridėk eilutę su kodu (pvz 'new_scenario': True)
  2. Paleisk: python manage.py sync_email_scenarios
  3. Sukurk šabloną apps/listings/emails/templates/
  4. Sukurk trigger'į (view'uose arba management command)

═══════════════════════════════════════════════════════════════════
"""

EMAIL_SCENARIOS = {
    # ═══════════════════════════════════════════════════════════
    # SELLER NOTIFICATIONS (apie jo skelbimus)
    # ═══════════════════════════════════════════════════════════
    'listing_published':              True,   # #1  Skelbimas paskelbtas
    'listing_expiring_soon':          True,   # #2  Baigiasi per 3 dienas
    'listing_expired':                True,   # #3  Pasibaigė
    'listing_sold_confirmation':      True,   # #4  Parduotas - sveikinam
    'listing_weekly_stats':           True,   # #5  Savaitės statistikos
    'listing_popular':                True,   # #6  Populiarus (daug views)
    'listing_reported':               True,   # #7  Kažkas pranešė
    # 'listing_admin_hidden':         # PRALEIDŽIAM (sakei nereikia)
    'listing_first_views':            True,   # #35 Pirmos 10 peržiūrų
    'listing_views_milestone':        True,   # #36 100/500/1000 views milestone
    'listing_no_sale_reminder':       True,   # #37 Savaitę nepardavei
    'listing_similar_sold':           True,   # #38 Panašus skelbimas parduotas
    'listing_saved_by_users':         True,   # #39 Žmonės išsaugojo
    'listing_auto_renew_reminder':    True,   # #40 Auto-renew priminimas
    'listing_expired_reminder':       True,   # #46 Expired skelbimų priminimas kas 4d

    # ═══════════════════════════════════════════════════════════
    # BUYER NOTIFICATIONS (apie išsaugotus skelbimus)
    # ═══════════════════════════════════════════════════════════
    'saved_listing_price_drop':       True,   # #9  Kaina nukrito
    'saved_listing_sold':             True,   # #10 Išsaugotas parduotas
    'saved_listing_updated':          True,   # #11 Pardavėjas atnaujino
    'followed_seller_new_listing':    True,   # #12 Pardavėjas paskelbė naują

    # ═══════════════════════════════════════════════════════════
    # SAVED SEARCH NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════
    'saved_search_new_results':       True,   # #13 Nauji rezultatai (9:00)
    'saved_search_price_drops':       True,   # #14 Kainos nukrito
    'saved_search_first_results':     True,   # #15 Pirmi rezultatai

    # ═══════════════════════════════════════════════════════════
    # ACCOUNT NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════
    'account_welcome':                True,   # #16 Sveiki atvykę
    'account_email_verification':     True,   # #17 Email patvirtinimas
    'account_password_reset':         True,   # #18 Slaptažodžio atnaujinimas
    'account_new_device_login':       True,   # #19 Naujas prisijungimas
    'account_profile_updated':        True,   # #20 Profile pakeistas
    'account_welcome_tutorial':       True,   # #42 Tutorial po 3d registracijos
    'account_reactivation':           True,   # #43 Neaktyvus >30d

    # ═══════════════════════════════════════════════════════════
    # COMMUNICATION
    # ═══════════════════════════════════════════════════════════
    'contact_seller':                 True,   # #21 Pirkėjas kreipėsi (JAU YRA)
    'contact_seller_reply':           True,   # #22 Atsakymas į žinutę
    'contact_seller_unanswered':      True,   # #23 Neatsakyta >24h
    'new_message_notification':       True,   # #45 Nauja žinute (Messages)

    # ═══════════════════════════════════════════════════════════
    # PAYMENTS (kai bus Stripe)
    # ═══════════════════════════════════════════════════════════
    'payment_success':                True,   # #24 Mokėjimas sėkmingas
    'payment_failed':                 True,   # #25 Mokėjimas nepavyko
    'payment_renewal_reminder':       True,   # #26 Savaitė iki atnaujinimo
    'payment_invoice':                True,   # #27 PDF sąskaita

    # ═══════════════════════════════════════════════════════════
    # MARKETING
    # ═══════════════════════════════════════════════════════════
    'marketing_weekly_top':           True,   # #28 Savaitės TOP
    'marketing_similar_listings':     True,   # #29 Panašūs skelbimai
    'marketing_promotions':           True,   # #30 Black Friday / akcijos

    # ═══════════════════════════════════════════════════════════
    # ADMIN NOTIFICATIONS (→ romasm3@gmail.com)
    # ═══════════════════════════════════════════════════════════
    'admin_new_listing_report':       True,   # #31 Skelbimas pranešas (JAU YRA)
    'admin_new_user_registration':    True,   # #32 Nauji vartotojai
    'admin_server_error':             True,   # #33 Django 500 klaidos
    'admin_critical_event':           True,   # #34 Spam/bot detection
    'admin_manual_broadcast':         True,   # #41 Custom email visiems

    # ═══════════════════════════════════════════════════════════
    # EXTRA (idėjos)
    # ═══════════════════════════════════════════════════════════
    'listing_photo_quality_tips':     True,   # #44 Mažos/blogos nuotraukos
}


# ═══════════════════════════════════════════════════════════════
# SCENARIO METADATA (aprašymai, kategorijos)
# ═══════════════════════════════════════════════════════════════
# Naudojama admin puslapyje ir sync_email_scenarios komandoje
# ═══════════════════════════════════════════════════════════════

SCENARIO_METADATA = {
    # SELLER
    'listing_published': {
        'category': 'Seller',
        'name': 'Listing Published',
        'description': 'Sent to seller when their listing goes live.',
        'trigger': 'Immediate, after publish',
    },
    'listing_expiring_soon': {
        'category': 'Seller',
        'name': 'Listing Expiring Soon',
        'description': 'Warning 3 days before listing expires.',
        'trigger': 'Daily cron 9:00',
    },
    'listing_expired': {
        'category': 'Seller',
        'name': 'Listing Expired',
        'description': 'Notification that listing has expired - can be reactivated.',
        'trigger': 'Daily cron 9:00',
    },
    'listing_sold_confirmation': {
        'category': 'Seller',
        'name': 'Listing Sold - Congrats',
        'description': 'Congratulations email when seller marks listing as SOLD.',
        'trigger': 'Immediate, on SOLD action',
    },
    'listing_weekly_stats': {
        'category': 'Seller',
        'name': 'Weekly Stats',
        'description': 'Weekly summary: views, impressions, saved counts per listing.',
        'trigger': 'Weekly Monday 9:00',
    },
    'listing_popular': {
        'category': 'Seller',
        'name': 'Listing Popular',
        'description': 'Listing got many views (+100/day).',
        'trigger': 'Daily cron 9:00',
    },
    'listing_reported': {
        'category': 'Seller',
        'name': 'Listing Reported',
        'description': 'Someone reported the listing.',
        'trigger': 'Immediate',
    },
    'listing_first_views': {
        'category': 'Seller',
        'name': 'First Views Milestone',
        'description': 'Listing hit first 10 views.',
        'trigger': 'Daily cron 9:00',
    },
    'listing_views_milestone': {
        'category': 'Seller',
        'name': 'Views Milestone',
        'description': 'Listing reached 100/500/1000 views.',
        'trigger': 'Daily cron 9:00',
    },
    'listing_no_sale_reminder': {
        'category': 'Seller',
        'name': 'No Sale Reminder',
        'description': 'Listing active 7 days but not sold - suggest lowering price.',
        'trigger': 'Daily cron 9:00',
    },
    'listing_similar_sold': {
        'category': 'Seller',
        'name': 'Similar Listing Sold',
        'description': 'A similar car was sold at lower price - pricing insight.',
        'trigger': 'Daily cron 9:00',
    },
    'listing_saved_by_users': {
        'category': 'Seller',
        'name': 'Saved by Users',
        'description': 'N users saved this listing this week.',
        'trigger': 'Weekly Monday 9:00',
    },
    'listing_auto_renew_reminder': {
        'category': 'Seller',
        'name': 'Auto-renew Reminder',
        'description': '3 days before listing expires - renew reminder.',
        'trigger': 'Daily cron 9:00',
    },

    # BUYER
    'saved_listing_price_drop': {
        'category': 'Buyer (Saved)',
        'name': 'Saved Listing - Price Drop',
        'description': 'Price dropped on a saved listing.',
        'trigger': 'Daily cron 9:00',
    },
    'saved_listing_sold': {
        'category': 'Buyer (Saved)',
        'name': 'Saved Listing - Sold',
        'description': 'Your saved listing was just sold.',
        'trigger': 'Immediate, on SOLD action',
    },
    'saved_listing_updated': {
        'category': 'Buyer (Saved)',
        'name': 'Saved Listing - Updated',
        'description': 'Seller updated the saved listing.',
        'trigger': 'Daily cron 9:00',
    },
    'followed_seller_new_listing': {
        'category': 'Buyer (Saved)',
        'name': 'Followed Seller - New Listing',
        'description': 'A seller you follow published a new listing.',
        'trigger': 'Daily cron 9:00',
    },

    # SAVED SEARCH
    'saved_search_new_results': {
        'category': 'Saved Search',
        'name': 'Saved Search - New Results',
        'description': 'New listings match your saved search.',
        'trigger': 'Daily cron 9:00',
    },
    'saved_search_price_drops': {
        'category': 'Saved Search',
        'name': 'Saved Search - Price Drops',
        'description': 'Price dropped on matching listings.',
        'trigger': 'Daily cron 9:00',
    },
    'saved_search_first_results': {
        'category': 'Saved Search',
        'name': 'Saved Search - First Results',
        'description': 'First results appeared for your new search.',
        'trigger': 'Daily cron 9:00',
    },

    # ACCOUNT
    'account_welcome': {
        'category': 'Account',
        'name': 'Welcome',
        'description': 'Welcome email after registration.',
        'trigger': 'Immediate',
    },
    'account_email_verification': {
        'category': 'Account',
        'name': 'Email Verification',
        'description': 'Verify email token link.',
        'trigger': 'Immediate',
    },
    'account_password_reset': {
        'category': 'Account',
        'name': 'Password Reset',
        'description': 'Password reset link.',
        'trigger': 'Immediate',
    },
    'account_new_device_login': {
        'category': 'Account',
        'name': 'New Device Login',
        'description': 'Alert for login from new device/browser.',
        'trigger': 'Immediate',
    },
    'account_profile_updated': {
        'category': 'Account',
        'name': 'Profile Updated',
        'description': 'Contact info or password changed.',
        'trigger': 'Immediate',
    },
    'account_welcome_tutorial': {
        'category': 'Account',
        'name': 'Welcome Tutorial',
        'description': 'Tutorial email 3 days after registration.',
        'trigger': 'Daily cron 9:00',
    },
    'account_reactivation': {
        'category': 'Account',
        'name': 'Reactivation',
        'description': 'Miss you - 30 days inactive.',
        'trigger': 'Weekly Monday 9:00',
    },

    # COMMUNICATION
    'contact_seller': {
        'category': 'Communication',
        'name': 'Contact Seller Inquiry',
        'description': 'Buyer contacts seller about listing.',
        'trigger': 'Immediate',
    },
    'contact_seller_reply': {
            'category': 'Communication',
            'name': 'Contact - Reply',
            'description': 'Seller replied to inquiry.',
            'trigger': 'Immediate',
        },
        'contact_seller_unanswered': {
            'category': 'Communication',
            'name': 'Contact - Unanswered',
            'description': 'Reminder to answer message older than 24h.',
            'trigger': 'Daily cron 9:00',
        },
        'new_message_notification': {
            'category': 'Communication',
            'name': 'New Message Notification',
            'description': 'User received a new message in Messages.',
            'trigger': 'Immediate, when message is sent',
        },
        'listing_expired_reminder': {
            'category': 'Seller',
            'name': 'Expired Reminder',
            'description': 'Listing has expired - remind every 4 days to activate.',
            'trigger': 'Daily cron, every 4 days per listing',
        },

    # PAYMENTS
    'payment_success': {
        'category': 'Payments',
        'name': 'Payment Success',
        'description': 'Stripe payment confirmation.',
        'trigger': 'Immediate (Stripe webhook)',
    },
    'payment_failed': {
        'category': 'Payments',
        'name': 'Payment Failed',
        'description': 'Stripe payment declined.',
        'trigger': 'Immediate (Stripe webhook)',
    },
    'payment_renewal_reminder': {
        'category': 'Payments',
        'name': 'Renewal Reminder',
        'description': 'Subscription/feature expires in 7 days.',
        'trigger': 'Daily cron 9:00',
    },
    'payment_invoice': {
        'category': 'Payments',
        'name': 'Invoice PDF',
        'description': 'PDF invoice attached after payment.',
        'trigger': 'Immediate (Stripe webhook)',
    },

    # MARKETING
    'marketing_weekly_top': {
        'category': 'Marketing',
        'name': 'Weekly TOP',
        'description': 'Popular cars this week newsletter.',
        'trigger': 'Weekly Monday 9:00',
    },
    'marketing_similar_listings': {
        'category': 'Marketing',
        'name': 'Similar Listings',
        'description': 'You viewed BMW - see similar.',
        'trigger': 'Weekly Monday 9:00',
    },
    'marketing_promotions': {
        'category': 'Marketing',
        'name': 'Promotions / Sales',
        'description': 'Black Friday, special offers.',
        'trigger': 'Manual',
    },

    # ADMIN
    'admin_new_listing_report': {
        'category': 'Admin',
        'name': 'Listing Report',
        'description': 'User reported a listing.',
        'trigger': 'Immediate',
    },
    'admin_new_user_registration': {
        'category': 'Admin',
        'name': 'New User Registration',
        'description': 'Hourly digest of new users.',
        'trigger': 'Hourly cron',
    },
    'admin_server_error': {
        'category': 'Admin',
        'name': 'Server Error (500)',
        'description': 'Django exception notification.',
        'trigger': 'Immediate',
    },
    'admin_critical_event': {
        'category': 'Admin',
        'name': 'Critical Event',
        'description': 'Spam/bot detection alerts.',
        'trigger': 'Immediate',
    },
    'admin_manual_broadcast': {
        'category': 'Admin',
        'name': 'Manual Broadcast',
        'description': 'Custom email to all users from admin panel.',
        'trigger': 'Manual from admin',
    },
    # EXTRA
    'listing_photo_quality_tips': {
        'category': 'Extra',
        'name': 'Photo Quality Tips',
        'description': 'Low quality photos detected - suggest improvements.',
        'trigger': 'Daily cron 9:00',
    },
}


# ═══════════════════════════════════════════════════════════════
# ADMIN EMAIL
# ═══════════════════════════════════════════════════════════════
# Visi admin scenarijai (admin_*) siunčiami čia
# ═══════════════════════════════════════════════════════════════
ADMIN_EMAIL = 'romasm3@gmail.com'