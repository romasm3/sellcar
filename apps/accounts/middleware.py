
"""

Language preference middleware.



Jei cookie kalba skiriasi nuo profilio — vartotojas ką tik perjungė

per set_language, tad įsimenam jo pasirinkimą į profilį.

Kitu atveju taikom profilio kalbą (kad "keliautų" tarp įrenginių).

"""

from django.conf import settings

from django.utils import translation

from django.utils.translation import get_language_from_path





class UserLanguageMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response



    def __call__(self, request):

        # Adrese esantis priešdėlis (/en/…) yra stipresnis už profilio kalbą:

        # kitaip angliškas puslapis būtų atiduotas lietuviškai.

        is_adreso = get_language_from_path(request.path_info)

        if is_adreso is None and request.user.is_authenticated:

            try:

                profile = request.user.profile

                user_lang = profile.language

                cookie_lang = request.COOKIES.get(

                    settings.LANGUAGE_COOKIE_NAME, ''

                )

                valid = dict(settings.LANGUAGES)



                if cookie_lang and cookie_lang in valid and cookie_lang != user_lang:

                    profile.language = cookie_lang

                    profile.save(update_fields=['language'])

                    translation.activate(cookie_lang)

                    request.LANGUAGE_CODE = cookie_lang

                elif user_lang and user_lang in valid:

                    translation.activate(user_lang)

                    request.LANGUAGE_CODE = user_lang

            except Exception:

                pass



        response = self.get_response(request)

        return response

