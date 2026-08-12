
"""

Language preference middleware.



Jei cookie kalba skiriasi nuo profilio — vartotojas ką tik perjungė

per set_language, tad įsimenam jo pasirinkimą į profilį.

Kitu atveju taikom profilio kalbą (kad "keliautų" tarp įrenginių).

"""

from django.conf import settings

from django.utils import translation





class UserLanguageMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response



    def __call__(self, request):

        if request.user.is_authenticated:

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

                elif user_lang:

                    translation.activate(user_lang)

                    request.LANGUAGE_CODE = user_lang

            except Exception:

                pass



        response = self.get_response(request)

        return response

