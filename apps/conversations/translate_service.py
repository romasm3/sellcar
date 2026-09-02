"""
Google Cloud Translation API service su DB cache.

DU KELIAI IKI GOOGLE — abu veda į tą patį Cloud Translation v2:

  1. JSON rakto failas (GOOGLE_APPLICATION_CREDENTIALS). Jei jis yra,
     dirbam kaip anksčiau — per google-cloud-translate biblioteką.
  2. API raktas (GOOGLE_TRANSLATE_API_KEY, o jo nesant —
     GOOGLE_MAPS_API_KEY). Serveryje JSON failo nėra, o .env raktą turi.

Kodėl antram keliui NENAUDOJAM `client_options={"api_key": ...}`:
patikrinta google-cloud-translate 3.26.0 kode —
`translate_v2.Client.__init__` iš `client_options` skaito TIK
`api_endpoint`, o `api_key` tyliai ignoruoja ir vis tiek eina ieškoti
numatytųjų kredencialų. Todėl su raktu kreipiamės tiesiai į tą patį
viešą v2 galinį tašką (`requests` jau yra priklausomybėse).

Jei nėra NEI failo, NEI rakto — keliam VertimoNera. Tylaus originalo su
sėkmės būsena čia nebūna: žmogus turi pamatyti „Vertimas neįjungtas".

Naudojimas:
    from apps.conversations.translate_service import translate_messages_for_user

    output = translate_messages_for_user(messages_qs, target_lang='de')
    # → [{'id': 1, 'original': 'Labas', 'translated': 'Hallo', 'detected': 'lt'}, ...]
"""

import logging

from django.conf import settings

from .models import Message, MessageTranslation

logger = logging.getLogger(__name__)

API_URL = 'https://translation.googleapis.com/language/translate/v2'
LAIKAS = 15          # s — kad sąsaja nekabotų, jei Google neatsako


class VertimoNera(Exception):
    """Vertimas neįjungtas: nėra nei JSON rakto failo, nei API rakto."""


def _api_raktas():
    """API raktas iš .env. Savas — pirmiau, Maps — atsarginis."""
    return (getattr(settings, 'GOOGLE_TRANSLATE_API_KEY', '')
            or getattr(settings, 'GOOGLE_MAPS_API_KEY', '') or '').strip()


def _rakto_failas():
    kelias = getattr(settings, 'GOOGLE_CREDENTIALS_PATH', None)
    try:
        return bool(kelias) and kelias.is_file()
    except Exception:
        return False


# Singleton client (sukuriam tik vieną kartą)
_client = None


def get_client():
    """Bibliotekos klientas — tik kai yra JSON rakto failas."""
    from google.cloud import translate_v2 as translate
    global _client
    if _client is None:
        _client = translate.Client()
    return _client


def _versk(tekstai, target_lang):
    """[{'translatedText','detectedSourceLanguage'}] — vienas kvietimas.

    Kuriuo keliu eiti, sprendžiam čia; visa kita servise vienoda.
    """
    if _rakto_failas():
        return get_client().translate(
            tekstai, target_language=target_lang, format_='text')

    raktas = _api_raktas()
    if not raktas:
        raise VertimoNera('nėra nei GOOGLE_APPLICATION_CREDENTIALS failo, '
                          'nei GOOGLE_TRANSLATE_API_KEY / GOOGLE_MAPS_API_KEY')

    import requests
    atsakymas = requests.post(
        API_URL, params={'key': raktas},
        json={'q': tekstai, 'target': target_lang, 'format': 'text'},
        timeout=LAIKAS,
    )
    if atsakymas.status_code != 200:
        # Google klaidą pasakom savais žodžiais — ji nurodo, ką taisyti.
        try:
            klaida = atsakymas.json().get('error', {}).get('message', '')
        except Exception:
            klaida = atsakymas.text[:200]
        raise RuntimeError('Google Translate %s: %s'
                           % (atsakymas.status_code, klaida))
    duomenys = atsakymas.json().get('data', {}).get('translations', [])
    return [{'translatedText': t.get('translatedText', ''),
             'detectedSourceLanguage': t.get('detectedSourceLanguage', '')}
            for t in duomenys]


def translate_messages_for_user(messages, target_lang='en'):
    """
    Verčia žinutes į target_lang. Naudoja DB cache.
    
    Args:
        messages: QuerySet arba list of Message objektų
        target_lang: ISO kodas ('en', 'de', 'es', 'lt', 'lv', 'pl', etc.)
    
    Returns:
        list of dicts: [{
            'id': msg_id,
            'original': '...',
            'translated': '...',
            'detected': 'en',  # auto-detected source lang
        }, ...]
    """
    target_lang = (target_lang or 'en').lower().split('-')[0]  # 'en-us' → 'en'
    
    # Filtruojam tik žinutes su tekstu
    messages_with_text = [m for m in messages if m.content and m.content.strip()]
    if not messages_with_text:
        return []
    
    msg_ids = [m.id for m in messages_with_text]
    
    # 1. Surinkim ką jau turim cache'e
    cached = {
        t.message_id: {
            'translated': t.translated_text,
            'detected': t.detected_source_lang,
        }
        for t in MessageTranslation.objects.filter(
            message_id__in=msg_ids,
            target_lang=target_lang,
        )
    }
    
    # 2. Surinkim ką dar reikia versti
    to_translate = [m for m in messages_with_text if m.id not in cached]
    
    # 3. Batch'u kviečiam Google API (jei yra ką)
    if to_translate:
        try:
            texts = [m.content for m in to_translate]
            results = _versk(texts, target_lang)
            
            # Saugojam į DB cache
            new_records = []
            for msg, result in zip(to_translate, results):
                translated = result.get('translatedText', msg.content)
                detected = result.get('detectedSourceLanguage', '')
                
                cached[msg.id] = {
                    'translated': translated,
                    'detected': detected,
                }
                new_records.append(MessageTranslation(
                    message=msg,
                    target_lang=target_lang,
                    translated_text=translated,
                    detected_source_lang=detected,
                ))
            
            if new_records:
                MessageTranslation.objects.bulk_create(
                    new_records,
                    ignore_conflicts=True,
                )
        except VertimoNera:
            # Vertimas išvis neįjungtas — ne „nepavyko", o „nenustatyta".
            # Keliam aukštyn, kad sąsaja parodytų „Vertimas neįjungtas".
            raise
        except Exception as e:
            # Failsafe: jei API neveikia (quota viršyta, network issue, etc.)
            # — grąžinam originalų tekstą, vartotojas matys non-translated.
            #
            # Kvietimas ir raktas nepaliesti. Pridėta tik žyma 'klaida':
            # be jos sąsaja negalėjo atskirti „išversta į tą pačią kalbą"
            # nuo „nepavyko", tad po žinute negalėdavo parodyti
            # „Nepavyko išversti" (reikalavimas 2026-09-02, 7 punktas).
            logger.exception('Google Translate API klaida: %s', e)
            for msg in to_translate:
                cached[msg.id] = {
                    'translated': msg.content,
                    'detected': '',
                    'klaida': True,
                }
    
    # 4. Sudarom output (ta pati eilė kaip input messages)
    output = []
    for m in messages_with_text:
        cache_entry = cached.get(m.id, {
            'translated': m.content,
            'detected': '',
        })
        output.append({
            'id': m.id,
            'original': m.content,
            'translated': cache_entry['translated'],
            'detected': cache_entry['detected'],
            'klaida': bool(cache_entry.get('klaida')),
        })
    return output