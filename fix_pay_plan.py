# -*- coding: utf-8 -*-
"""
fix_pay_plan.py
Pakeičia listing_pay_plan funkcijos POST dalį — vietoj wallet nuskaitymo
sukuria Stripe Checkout sesiją. Aktyvavimo logika perkeliama į webhook'ą.

Paleisti SellCar projekto šaknyje:
    python fix_pay_plan.py
"""
import io
import sys

PATH = r"apps\listings\views.py"

# Pakeičiamo bloko PRADŽIA ir PABAIGA (unikalūs žymekliai faile)
START_MARKER = "    if request.method != 'POST':\n        return redirect('listing_select_plan', pk=pk)\n\n    # \u2500\u2500\u2500 Calculate total"
END_MARKER = "    return redirect(reverse('listing_success', kwargs={'pk': listing.pk}) + '?action=published')\n"

NEW_BLOCK = '''    if request.method != 'POST':
        return redirect('listing_select_plan', pk=pk)

    # \u2500\u2500\u2500 Calculate total \u2500 naudojam final_price (su multiplier jei \u012fjungtas) \u2500\u2500\u2500
    total_price = Decimal(str(plan['final_price_usd']))

    # Stars addon: count \u00d7 days \u00d7 price_per_unit
    renew_count = int(request.POST.get('renew_count', 0) or 0)
    renew_days = int(request.POST.get('renew_days', 0) or 0)
    if renew_count > 0 and renew_days > 0:
        renew_cost = Decimal(str(renew_count * renew_days * float(pricing.addon_renew_price)))
        total_price += renew_cost
    else:
        renew_cost = Decimal('0')

    # Featured addon: days \u00d7 price_per_day
    featured_days = int(request.POST.get('featured_days', 0) or 0)
    if featured_days > 0:
        featured_cost = Decimal(str(featured_days * float(pricing.addon_featured_price)))
        total_price += featured_cost
    else:
        featured_cost = Decimal('0')

    total_price = total_price.quantize(Decimal('0.01'))

    # \u2500\u2500\u2500 Stripe Checkout \u2500 planai mokami TIK kortele (wallet nedalyvauja) \u2500\u2500\u2500
    stripe_secret = getattr(settings, 'STRIPE_SECRET_KEY', '')
    if not stripe_secret:
        messages.error(request, 'Payment system is being set up. Please try again later.')
        return redirect('listing_select_plan', pk=pk)

    addon_parts = []
    if renew_cost > 0:
        addon_parts.append(f"{renew_count}* x {renew_days}d")
    if featured_cost > 0:
        addon_parts.append(f"featured {featured_days}d")

    product_name = f"{listing.title} - {plan['label']} plan ({plan['days']}d)"
    if addon_parts:
        product_name += " + " + ", ".join(addon_parts)

    try:
        import stripe
        stripe.api_key = stripe_secret

        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': product_name[:250]},
                    'unit_amount': int(total_price * 100),
                },
                'quantity': 1,
            }],
            customer_email=request.user.email,
            success_url=request.build_absolute_uri(
                reverse('listing_success', kwargs={'pk': listing.pk}) + '?action=published'
            ),
            cancel_url=request.build_absolute_uri(
                reverse('listing_select_plan', kwargs={'pk': listing.pk})
            ),
            metadata={
                'type': 'listing_plan',
                'user_id': str(request.user.id),
                'listing_id': str(listing.pk),
                'plan_code': plan['code'],
                'plan_days': str(plan['days']),
                'plan_boost_days': str(plan.get('boost_days', 0)),
                'plan_boost_count': str(plan.get('boost_count', 0)),
                'plan_featured_days': str(plan.get('featured_days', 0)),
                'plan_highlight_days': str(plan.get('highlight_days', 0)),
                'renew_count': str(renew_count),
                'renew_days': str(renew_days),
                'addon_featured_days': str(featured_days),
                'total_price': str(total_price),
            },
        )
        return redirect(session.url)

    except Exception as e:
        messages.error(request, f'Payment error: {str(e)[:120]}')
        return redirect('listing_select_plan', pk=pk)
'''


def main():
    with io.open(PATH, 'r', encoding='utf-8') as f:
        src = f.read()

    start = src.find(START_MARKER)
    if start == -1:
        print("KLAIDA: nerastas START_MARKER. Failas nepakeistas.")
        sys.exit(1)

    # END: ieskom paskutinio listing_success redirect PO start pozicijos
    end_idx = src.find(END_MARKER, start)
    if end_idx == -1:
        print("KLAIDA: nerastas END_MARKER. Failas nepakeistas.")
        sys.exit(1)
    end = end_idx + len(END_MARKER)

    old_block = src[start:end]
    print("--- Randamas senas blokas (pirmos/paskutines eilutes) ---")
    lines = old_block.split('\n')
    print("PRADZIA:", lines[0])
    print("PABAIGA:", lines[-2] if len(lines) > 1 else lines[-1])
    print("Bloko ilgis:", len(old_block), "simboliu")

    new_src = src[:start] + NEW_BLOCK + src[end:]

    # Backup
    with io.open(PATH + '.bak_payplan', 'w', encoding='utf-8') as f:
        f.write(src)

    with io.open(PATH, 'w', encoding='utf-8') as f:
        f.write(new_src)

    print("\nOK: listing_pay_plan pakeista.")
    print("Backup issaugotas:", PATH + '.bak_payplan')


if __name__ == '__main__':
    main()