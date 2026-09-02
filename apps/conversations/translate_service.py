"""
Google Cloud Translation API service su DB cache.

Naudojimas:
    from apps.conversations.translate_service import translate_messages_for_user
    
    output = translate_messages_for_user(messages_qs, target_lang='de')
    # → [{'id': 1, 'original': 'Labas', 'translated': 'Hallo', 'detected': 'lt'}, ...]
"""

import logging

from google.cloud import translate_v2 as translate
from .models import Message, MessageTranslation

logger = logging.getLogger(__name__)


# Singleton client (sukuriam tik vieną kartą)
_client = None


def get_client():
    global _client
    if _client is None:
        _client = translate.Client()
    return _client


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
            client = get_client()
            texts = [m.content for m in to_translate]
            
            # Google API priima list of strings — grąžina list of dicts
            results = client.translate(
                texts,
                target_language=target_lang,
                format_='text',  # plain text (ne HTML)
            )
            
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