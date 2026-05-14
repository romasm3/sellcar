"""
Language preference middleware.

Loads logged-in user's preferred language from Profile and sets it
as the active language for the current request.

This makes language "stick" across devices/browsers when user logs in.
"""
from django.utils import translation


class UserLanguageMiddleware:
    """
    Auto-load language from user.profile.language for authenticated users.

    Order in MIDDLEWARE settings:
    - django.middleware.locale.LocaleMiddleware (sets language from cookie)
    - apps.accounts.middleware.UserLanguageMiddleware (overrides if user logged in)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                user_lang = profile.language

                # Override session/cookie language with user's preference
                if user_lang:
                    translation.activate(user_lang)
                    request.LANGUAGE_CODE = user_lang
                    if hasattr(request, 'session'):
                        request.session['_language'] = user_lang
            except Exception:
                pass  # No profile or DB issue — fallback to cookie/default

        response = self.get_response(request)
        return response