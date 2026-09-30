# -*- coding: utf-8 -*-
"""
PERF-01: TAILWIND IŠ SAVO FAILO, NE IŠ cdn.tailwindcss.com.

Anksčiau kiekvienas puslapis krovė cdn.tailwindcss.com (~400 KB JS) ir
Tailwind kompiliavosi naršyklėje; be to kiekviename atsakyme buvo 31–69 KB
įdėtinių <style> blokų. Dabar:
  • static/css/tailwind.css — sukompiliuotas (npm run build:css);
  • static/css/bazinis.css, paieskos_laukai.css, skelbimu_sarasas.css —
    buvę didžiausi įdėtiniai blokai.

Tikrinam per HTTP (DB neliečiam):
  • nė vienas iš 5 URL negrąžina „cdn.tailwindcss.com";
  • puslapyje susietas /static/css/tailwind*.css ir bazinis*.css → 200,
    ir tai tikras CSS (Tailwind klasės, :root kintamieji);
  • įdėtinių <style> blokų suma kiekviename puslapyje < 25 KB.

Paleidimas:
    python docs/tailwind_cdn_test.py                       # gyva svetainė
    TIKRINTI=http://127.0.0.1:8899 python docs/tailwind_cdn_test.py
"""
import os
import re
import sys
import urllib.request

BAZE = os.environ.get('TIKRINTI', 'https://autoleft.com').rstrip('/')
URL = ['/', '/paieska/parts/', '/paieska/cars/', '/917/', '/skelbimai/']
INLINE_RIBA = 25 * 1024

gerai = blogai = 0


def tikrink(salyga, tekstas, papildomai=''):
    global gerai, blogai
    if salyga:
        gerai += 1
        print(f'  OK   {tekstas}')
    else:
        blogai += 1
        print(f'  BLOGAI {tekstas}' + (f'\n         {papildomai}' if papildomai else ''))


def gauk(kelias):
    url = kelias if kelias.startswith('http') else BAZE + kelias
    req = urllib.request.Request(url, headers={'User-Agent': 'AutoLeft-tailwind-test/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:                           # tinklo klaida
        return None, str(e)


def main():
    print(f'Tikrinama: {BAZE}')
    css_nuorodos = set()
    for kelias in URL:
        print(f'\n— {kelias}')
        kodas, html = gauk(kelias)
        tikrink(kodas == 200, f'200 (gauta {kodas})')
        tikrink('cdn.tailwindcss.com' not in html, 'nėra „cdn.tailwindcss.com"')
        tw = re.findall(r'href="([^"]*/static/css/tailwind[^"]*\.css)"', html)
        tikrink(bool(tw), 'susietas /static/css/tailwind*.css', f'rasta {tw}')
        bz = re.findall(r'href="([^"]*/static/css/bazinis[^"]*\.css)"', html)
        tikrink(bool(bz), 'susietas /static/css/bazinis*.css')
        css_nuorodos.update(tw + bz)
        idetiniai = sum(len(b.encode()) for b in
                        re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
        tikrink(idetiniai < INLINE_RIBA,
                f'įdėtinių <style> {idetiniai // 1024} KB (< {INLINE_RIBA // 1024} KB)')

    print('\n— CSS failai')
    for href in sorted(css_nuorodos):
        kodas, css = gauk(href)
        tikrink(kodas == 200, f'{href} → 200 (gauta {kodas})')
        if 'tailwind' in href:
            tikrink('.bg-white' in css and '.flex' in css and '--tw-' in css,
                    f'   tikras Tailwind CSS ({len(css) // 1024} KB)')
        else:
            tikrink(':root' in css and '--accent-rgb' in css,
                    f'   baziniai kintamieji ({len(css) // 1024} KB)')

    print(f'\n════ {gerai} gerai / {blogai} blogai ════')
    return 1 if blogai else 0


if __name__ == '__main__':
    sys.exit(main())
