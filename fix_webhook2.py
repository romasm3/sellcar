# -*- coding: utf-8 -*-
"""
fix_webhook2.py  (v2 — patikimesnis)
Prideda 'listing_plan' saka i stripe_webhook funkcija (apps/accounts/views.py).

Skirtumas nuo v1: ieško NE viso teksto bloko, o vienos unikalios eilutes
('return HttpResponse(status=200)' su 8 tarpais) FUNKCIJOS RIBOSE.
Naują saką įterpia tiksliai PRIES ta eilute.

Paleisti AutoLeft projekto saknyje:
    python fix_webhook2.py
"""
import io
import sys

PATH = r"apps\accounts\views.py"

NEW_BRANCH_LINES = """
            elif _md('type') == 'listing_plan':
                from datetime import timedelta
                from apps.listings.models import Listing

                listing_id = int(_md('listing_id', '0') or 0)
                user_id = int(_md('user_id', '0') or 0)
                plan_days = int(_md('plan_days', '0') or 0)
                plan_boost_days = int(_md('plan_boost_days', '0') or 0)
                plan_boost_count = int(_md('plan_boost_count', '0') or 0)
                plan_featured_days = int(_md('plan_featured_days', '0') or 0)
                plan_highlight_days = int(_md('plan_highlight_days', '0') or 0)
                renew_count = int(_md('renew_count', '0') or 0)
                renew_days = int(_md('renew_days', '0') or 0)
                addon_featured_days = int(_md('addon_featured_days', '0') or 0)

                # Idempotency — jau apdorota? (tikrinam pagal WalletTransaction log)
                already = WalletTransaction.objects.filter(
                    stripe_session_id=session_id,
                    status='completed',
                ).exists()
                if already:
                    return HttpResponse(status=200)

                payment_intent = session.payment_intent or ''

                try:
                    listing = Listing.objects.get(pk=listing_id)
                except Listing.DoesNotExist:
                    return HttpResponse('Listing not found', status=200)

                # Jeigu jau aktyvus — nedubliuojam
                if listing.status == 'active':
                    return HttpResponse(status=200)

                now = timezone.now()

                # Aktyvuojam skelbima
                listing.activate(days=plan_days)

                # Boost (renewed badge) jei planas turi boost arba pirko stars
                if plan_boost_days > 0 or renew_count > 0:
                    listing.last_boosted_at = now
                    listing.save(update_fields=['last_boosted_at'])

                # Stars — max is plano ir addon'o
                final_star_count = max(plan_boost_count, renew_count)
                final_star_days = max(plan_boost_days, renew_days)
                if final_star_count > 0:
                    listing.star_level = 1
                    listing.star_count = final_star_count
                    if final_star_days > 0:
                        if listing.star_expires_at and listing.star_expires_at > now:
                            listing.star_expires_at = listing.star_expires_at + timedelta(days=final_star_days)
                        else:
                            listing.star_expires_at = now + timedelta(days=final_star_days)
                    listing.save(update_fields=['star_level', 'star_count', 'star_expires_at'])

                # Featured on homepage — planas + addon
                total_featured = plan_featured_days + addon_featured_days
                if total_featured > 0:
                    if listing.featured_until and listing.featured_until > now:
                        listing.featured_until = listing.featured_until + timedelta(days=total_featured)
                    else:
                        listing.featured_until = now + timedelta(days=total_featured)
                    listing.save(update_fields=['featured_until'])

                # Highlight — tik is plano
                if plan_highlight_days > 0:
                    if listing.highlight_until and listing.highlight_until > now:
                        listing.highlight_until = listing.highlight_until + timedelta(days=plan_highlight_days)
                    else:
                        listing.highlight_until = now + timedelta(days=plan_highlight_days)
                    listing.save(update_fields=['highlight_until'])

                # Tranzakcijos logas (idempotency markeris + istorija)
                try:
                    user = User.objects.get(id=user_id)
                    total_price = Decimal(str(_md('total_price', '0') or '0'))
                    WalletTransaction.objects.create(
                        user=user,
                        amount=-total_price,
                        transaction_type='spend',
                        status='completed',
                        description=f"Listing #{listing.pk} - plan {_md('plan_code', '')} (Stripe)",
                        stripe_session_id=session_id,
                        stripe_payment_intent=payment_intent,
                        completed_at=now,
                    )
                except Exception as log_err:
                    print(f"[webhook] listing_plan tx log failed: {log_err}")
"""


def main():
    with io.open(PATH, 'r', encoding='utf-8') as f:
        src = f.read()

    # Jau pridėta?
    if "elif _md('type') == 'listing_plan':" in src:
        print("INFO: listing_plan saka jau egzistuoja. Nieko nedaroma.")
        sys.exit(0)

    # Surandam stripe_webhook funkcijos riba
    fn_start = src.find('def stripe_webhook')
    if fn_start == -1:
        print("KLAIDA: nerasta funkcija 'def stripe_webhook'.")
        sys.exit(1)

    # Funkcijos pabaiga = kita 'def ' arba '@' nuo 0 itrauka po fn_start
    rest = src[fn_start + 5:]
    fn_end_rel = len(rest)
    for marker in ('\ndef ', '\n@', '\nclass '):
        idx = rest.find(marker)
        if idx != -1 and idx < fn_end_rel:
            fn_end_rel = idx
    fn_end = fn_start + 5 + fn_end_rel

    fn_body = src[fn_start:fn_end]

    # Ieskom paskutinio 'return HttpResponse(status=200)' su tiksliai 8 tarpais itrauka
    TARGET = "\n        return HttpResponse(status=200)\n"
    pos_in_body = fn_body.rfind(TARGET)
    if pos_in_body == -1:
        # bandom be galunes \n
        TARGET = "\n        return HttpResponse(status=200)"
        pos_in_body = fn_body.rfind(TARGET)
        if pos_in_body == -1:
            print("KLAIDA: nerasta '        return HttpResponse(status=200)' eilute funkcijoje.")
            sys.exit(1)

    insert_pos = fn_start + pos_in_body  # pries \n
    new_src = src[:insert_pos] + NEW_BRANCH_LINES + src[insert_pos:]

    with io.open(PATH + '.bak_webhook', 'w', encoding='utf-8') as f:
        f.write(src)
    with io.open(PATH, 'w', encoding='utf-8') as f:
        f.write(new_src)

    print("OK: listing_plan saka prideta i stripe_webhook.")
    print("Backup issaugotas:", PATH + '.bak_webhook')


if __name__ == '__main__':
    main()