# -*- coding: utf-8 -*-
"""
HTML puslapių kešavimas naršyklėje.

Puslapiai grįždavo be jokio `Cache-Control`, todėl naršyklė pati
spręsdavo, kiek laiko laikyti seną kopiją — po diegimo žmogus dar
matydavo senąjį maketą, nors serveryje jau naujas (taip nutiko su
kategorijų pikeriu 2026-08-25).

Sprendimas: HTML atsakymams sakom „prieš rodant — pasitikslink".
Statiniai failai (/static/) čia neliečiami: jie versijuojami ir turi
būti kešuojami ilgai.
"""


class HtmlBeKesoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        atsakymas = self.get_response(request)
        if request.path.startswith(('/static/', '/media/')):
            return atsakymas
        tipas = atsakymas.headers.get('Content-Type', '')
        if 'text/html' in tipas and not atsakymas.headers.get('Cache-Control'):
            atsakymas.headers['Cache-Control'] = 'no-cache, must-revalidate'
        return atsakymas
