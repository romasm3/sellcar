"""
Help Center & info pages views.
Visi puslapiai atviri (be login).
"""
from django.shortcuts import render


def help_center(request):
    """Pagrindinis Help Center puslapis — /help/"""
    return render(request, 'pages/help_center.html')


def whats_new(request):
    """Latest features & updates — /help/whats-new/"""
    updates = [
        {
            'date': '2026-05-13',
            'title': 'Dealer Subscriptions Launched',
            'description': 'Become a verified dealer for $100/month and list up to 30 vehicles.',
            'tag': 'New Feature',
            'tag_color': 'red',
        },
        {
            'date': '2026-05-10',
            'title': 'New Vehicle Categories: Trucks',
            'description': 'You can now buy and sell heavy commercial vehicles.',
            'tag': 'Update',
            'tag_color': 'blue',
        },
        {
            'date': '2026-04-28',
            'title': 'Wallet System & Bonuses',
            'description': 'Top up your wallet and get up to 20% bonus on payments.',
            'tag': 'New Feature',
            'tag_color': 'red',
        },
        {
            'date': '2026-04-15',
            'title': 'Saved Searches with Email Alerts',
            'description': 'Save your search criteria and receive notifications when new listings match.',
            'tag': 'Update',
            'tag_color': 'blue',
        },
    ]
    return render(request, 'pages/page_simple.html', {
        'page_title': "What's New",
        'page_subtitle': 'Latest features, updates, and platform announcements',
        'page_icon': 'fa-bullhorn',
        'page_color': 'blue',
        'updates': updates,
        'show_updates': True,
    })


def market_trends(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Market Trends',
        'page_subtitle': 'Vehicle price trends, popular models, and market insights',
        'page_icon': 'fa-chart-line',
        'page_color': 'green',
        'coming_soon': True,
    })


def tips_guides(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Tips & Guides',
        'page_subtitle': 'Expert advice for buying and selling vehicles',
        'page_icon': 'fa-lightbulb',
        'page_color': 'purple',
        'coming_soon': True,
    })


def pricing(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Pricing',
        'page_subtitle': 'Listing fees, dealer plans, and service pricing',
        'page_icon': 'fa-tag',
        'page_color': 'emerald',
        'coming_soon': True,
    })


def valuation(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Vehicle Valuation',
        'page_subtitle': "Estimate your car's market value — free and instant",
        'page_icon': 'fa-calculator',
        'page_color': 'teal',
        'coming_soon': True,
    })


def advertise(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Advertising',
        'page_subtitle': "Promote your business to SellCar's audience",
        'page_icon': 'fa-bullhorn',
        'page_color': 'orange',
        'coming_soon': True,
    })


def about_us(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'About Us',
        'page_subtitle': 'Our mission, story, and team',
        'page_icon': 'fa-info-circle',
        'page_color': 'gray',
        'coming_soon': True,
    })


def contact_page(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Contact Us',
        'page_subtitle': 'Get in touch with our team',
        'page_icon': 'fa-envelope',
        'page_color': 'pink',
        'coming_soon': True,
    })


def terms(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Terms of Use',
        'page_subtitle': 'Terms and conditions for using SellCar',
        'page_icon': 'fa-file-contract',
        'page_color': 'gray',
        'coming_soon': True,
    })


def privacy(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Privacy Policy',
        'page_subtitle': 'How we collect, use, and protect your data',
        'page_icon': 'fa-shield-alt',
        'page_color': 'gray',
        'coming_soon': True,
    })


def cookies(request):
    return render(request, 'pages/page_simple.html', {
        'page_title': 'Cookie Policy',
        'page_subtitle': 'How and why we use cookies',
        'page_icon': 'fa-cookie-bite',
        'page_color': 'gray',
        'coming_soon': True,
    })