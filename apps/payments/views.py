"""Stripe Checkout + Webhook views."""

from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.accounts.models import WalletTransaction
from .models import StripeEvent, StripeCheckoutSession
from . import stripe_service


MIN_TOPUP_USD = Decimal('5.00')
MAX_TOPUP_USD = Decimal('1000.00')


def _safe_get(stripe_obj, key, default=''):
    """Helper: safely get attribute from Stripe object or dict.

    stripe.StripeObject neturi .get() metodo, bet veikia kaip dict per __getitem__.
    Šitas helperis veikia su abiem (dict ir StripeObject).
    """
    try:
        value = stripe_obj[key]
        return value if value is not None else default
    except (KeyError, TypeError):
        return default


@login_required
@require_POST
def create_wallet_topup_checkout(request):
    """Sukuria Stripe Checkout Session ir redirect'ina user'į."""
    try:
        amount = Decimal(str(request.POST.get('amount', '0')))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid amount.')
        return redirect('/accounts/wallet/')

    if amount < MIN_TOPUP_USD or amount > MAX_TOPUP_USD:
        messages.error(
            request,
            f'Amount must be between ${MIN_TOPUP_USD} and ${MAX_TOPUP_USD}.'
        )
        return redirect('/accounts/wallet/')

    success_url = request.build_absolute_uri(
        reverse('payments:topup_success')
    ) + '?session_id={CHECKOUT_SESSION_ID}'
    cancel_url = request.build_absolute_uri(reverse('payments:topup_cancel'))

    try:
        session = stripe_service.create_wallet_topup_session(
            user=request.user,
            amount_usd=amount,
            success_url=success_url,
            cancel_url=cancel_url,
        )
    except Exception as e:
        print(f'[stripe] checkout session creation failed: {e}')
        messages.error(request, 'Payment system error. Please try again.')
        return redirect('/accounts/wallet/')

    StripeCheckoutSession.objects.create(
        user=request.user,
        stripe_session_id=session.id,
        purpose='wallet_topup',
        amount_usd=amount,
        status='pending',
        metadata={'stripe_url': session.url},
    )

    return redirect(session.url, permanent=False)


@login_required
def topup_success(request):
    """User'is grįžo iš Stripe checkout — webhook'as faktiškai prideda balansą."""
    session_id = request.GET.get('session_id', '')

    if not session_id:
        return redirect('/accounts/wallet/')

    try:
        local_session = StripeCheckoutSession.objects.get(
            stripe_session_id=session_id,
            user=request.user,
        )
    except StripeCheckoutSession.DoesNotExist:
        messages.error(request, 'Session not found.')
        return redirect('/accounts/wallet/')

    if local_session.status == 'completed':
        messages.success(
            request,
            f'${local_session.amount_usd} added to your wallet successfully!'
        )
    else:
        messages.info(
            request,
            'Payment received. Your wallet will be updated within a few seconds.'
        )

    return redirect('/accounts/wallet/')


@login_required
def topup_cancel(request):
    messages.info(request, 'Payment cancelled.')
    return redirect('/accounts/wallet/')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Stripe webhook endpoint.

    1. csrf_exempt — Stripe nesiunčia CSRF token
    2. Signature verification — patvirtina, kad iš Stripe
    3. Idempotency — nepasidubliuoja
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    if not sig_header:
        return HttpResponseBadRequest('No signature')

    try:
        event = stripe_service.verify_webhook_signature(payload, sig_header)
    except ValueError as e:
        print(f'[stripe webhook] Invalid payload: {e}')
        return HttpResponseBadRequest('Invalid payload')
    except Exception as e:
        print(f'[stripe webhook] Signature verification failed: {e}')
        return HttpResponseBadRequest('Invalid signature')

    # IDEMPOTENCY CHECK
    event_id = event['id']
    if StripeEvent.objects.filter(stripe_event_id=event_id).exists():
        print(f'[stripe webhook] Event {event_id} already processed, skipping')
        return HttpResponse(status=200)

    event_type = event['type']
    print(f'[stripe webhook] Received: {event_type} (id={event_id})')

    try:
        if event_type == 'checkout.session.completed':
            _handle_checkout_completed(event)
        elif event_type == 'checkout.session.expired':
            _handle_checkout_expired(event)
        elif event_type == 'payment_intent.payment_failed':
            _handle_payment_failed(event)
        else:
            print(f'[stripe webhook] Unhandled event type: {event_type}')
    except Exception as e:
        print(f'[stripe webhook] Handler error for {event_type}: {e}')
        import traceback
        traceback.print_exc()
        return HttpResponse(status=500)

    # Log event kaip apdorotą
    try:
        obj_id = _safe_get(event['data']['object'], 'id', '')
    except Exception:
        obj_id = ''

    StripeEvent.objects.create(
        stripe_event_id=event_id,
        event_type=event_type,
        payload_summary=str(obj_id)[:500],
    )

    return HttpResponse(status=200)


def _handle_checkout_completed(event):
    """Stripe Checkout sesija sėkmingai baigta."""
    session_obj = event['data']['object']
    stripe_session_id = session_obj['id']

    # metadata gali būti StripeObject, ne dict
    metadata = session_obj['metadata'] if 'metadata' in session_obj else {}
    purpose = _safe_get(metadata, 'purpose', '')

    print(f'[stripe webhook] checkout.session.completed: {stripe_session_id}, purpose={purpose}')

    if purpose == 'wallet_topup':
        _process_wallet_topup(stripe_session_id, session_obj, metadata)
    else:
        print(f'[stripe webhook] Unknown purpose: {purpose}')


def _process_wallet_topup(stripe_session_id, session_obj, metadata):
    """Prideda kreditą prie wallet balanso."""
    try:
        local_session = StripeCheckoutSession.objects.get(
            stripe_session_id=stripe_session_id,
        )
    except StripeCheckoutSession.DoesNotExist:
        print(f'[stripe webhook] Local session not found: {stripe_session_id}')
        return

    if local_session.status == 'completed':
        print(f'[stripe webhook] Session already completed: {stripe_session_id}')
        return

    user = local_session.user
    amount = local_session.amount_usd
    profile = getattr(user, 'profile', None)

    if not profile:
        print(f'[stripe webhook] User {user.pk} has no profile')
        return

    # Patikrinam ar Stripe sumai sutampa su mūsų local
    stripe_amount_cents = _safe_get(session_obj, 'amount_total', 0)
    stripe_amount = Decimal(str(stripe_amount_cents)) / Decimal('100')
    if stripe_amount != amount:
        print(
            f'[stripe webhook] AMOUNT MISMATCH! '
            f'Local: ${amount}, Stripe: ${stripe_amount}, session: {stripe_session_id}'
        )
        amount = stripe_amount  # naudojam Stripe sumą — tikrąją

    with transaction.atomic():
        profile.wallet_balance = (profile.wallet_balance or Decimal('0')) + amount
        profile.save(update_fields=['wallet_balance'])

        WalletTransaction.objects.create(
            user=user,
            amount=amount,
            transaction_type='topup',
            description=f'Wallet top-up via Stripe (${amount})',
        )

        local_session.status = 'completed'
        local_session.completed_at = timezone.now()
        local_session.save(update_fields=['status', 'completed_at'])

    print(f'[stripe webhook] ✓ Wallet topup: user={user.email} +${amount}')


def _handle_checkout_expired(event):
    session_obj = event['data']['object']
    stripe_session_id = session_obj['id']

    try:
        local_session = StripeCheckoutSession.objects.get(
            stripe_session_id=stripe_session_id,
        )
        local_session.status = 'expired'
        local_session.save(update_fields=['status'])
        print(f'[stripe webhook] Session expired: {stripe_session_id}')
    except StripeCheckoutSession.DoesNotExist:
        pass


def _handle_payment_failed(event):
    payment_intent = event['data']['object']
    pi_id = _safe_get(payment_intent, 'id', '')
    print(f'[stripe webhook] Payment failed: {pi_id}')