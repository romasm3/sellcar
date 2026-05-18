from django.db import models
from django.contrib.auth.models import User


class StripeEvent(models.Model):
    """Idempotency log — Stripe siunčia tą patį webhook 2-3x, kad nesiduplikuotų."""
    stripe_event_id = models.CharField(max_length=255, unique=True, db_index=True)
    event_type = models.CharField(max_length=100)
    processed_at = models.DateTimeField(auto_now_add=True)
    payload_summary = models.TextField(blank=True)

    class Meta:
        ordering = ['-processed_at']
        verbose_name = 'Stripe Event'
        verbose_name_plural = 'Stripe Events'

    def __str__(self):
        return f'{self.event_type} @ {self.processed_at:%Y-%m-%d %H:%M}'


class StripeCheckoutSession(models.Model):
    """Audit trail visiem Stripe checkout sessijoms — debug + reconciliation."""

    PURPOSE_CHOICES = [
        ('wallet_topup', 'Wallet Top-Up'),
        ('listing_plan', 'Listing Plan'),
        ('listing_services', 'Listing Services'),
        ('dealer_subscription', 'Dealer Subscription'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stripe_sessions')
    stripe_session_id = models.CharField(max_length=255, unique=True, db_index=True)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Stripe Checkout Session'
        verbose_name_plural = 'Stripe Checkout Sessions'

    def __str__(self):
        return f'{self.user.email} - {self.purpose} - ${self.amount_usd} ({self.status})'