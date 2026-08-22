"""Stripe API service wrapper. Visi Stripe call'ai eina per čia."""

import stripe
from decimal import Decimal
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_wallet_topup_session(user, amount_usd: Decimal, success_url: str, cancel_url: str):
    """Sukuria Stripe Checkout Session wallet papildymui."""
    amount_cents = int(amount_usd * 100)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'AutoLeft Wallet Top-Up',
                    'description': f'${amount_usd} credit to your AutoLeft wallet',
                },
                'unit_amount': amount_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=user.email,
        metadata={
            'purpose': 'wallet_topup',
            'user_id': str(user.pk),
            'amount_usd': str(amount_usd),
        },
    )
    return session


def verify_webhook_signature(payload: bytes, sig_header: str):
    """Patvirtina, kad webhook tikrai iš Stripe.

    Returns: stripe.Event instance
    Raises: ValueError, stripe.error.SignatureVerificationError
    """
    return stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET,
    )