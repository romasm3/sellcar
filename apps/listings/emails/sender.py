"""
═══════════════════════════════════════════════════════════════════
DĖK Į: apps/listings/emails/sender.py

(Pilnai perrašo esamą failą - subject handling pataisytas)
═══════════════════════════════════════════════════════════════════
"""

import logging
from typing import Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import get_template, render_to_string
from django.utils import timezone

from apps.listings.email_settings import EMAIL_SCENARIOS, ADMIN_EMAIL

logger = logging.getLogger(__name__)


def should_send(code: str, to_user=None) -> tuple[bool, str]:
    """
    Patikrina ar šiuo metu galima siųsti šį scenarijų.
    """
    if not EMAIL_SCENARIOS.get(code, False):
        return False, f"EMAIL_SCENARIOS[{code}] = False"

    from apps.listings.models import EmailScenario
    try:
        scenario = EmailScenario.objects.get(code=code)
        if not scenario.is_enabled:
            return False, f"DB EmailScenario({code}).is_enabled = False"
    except EmailScenario.DoesNotExist:
        pass

    if to_user is not None and hasattr(to_user, 'profile'):
        profile = to_user.profile
        if not getattr(profile, 'email_notifications', True):
            return False, f"User {to_user.email} disabled email_notifications"

    return True, ''


def _try_render(template_name: str, context: dict) -> Optional[str]:
    """
    Bando renderinti šabloną. Jei nėra - None.
    """
    try:
        get_template(template_name)
    except TemplateDoesNotExist:
        return None

    try:
        return render_to_string(template_name, context).strip()
    except Exception as e:
        logger.error(f"[email] Template render failed: {template_name}: {e}")
        return None


def send_scenario(
    code: str,
    to_email: str,
    context: Optional[dict] = None,
    subject_override: Optional[str] = None,
    to_user=None,
    from_email: Optional[str] = None,
    reply_to: Optional[str] = None,
    attachments: Optional[list] = None,
) -> bool:
    """
    Siunčia vieną email'ą pagal scenarijaus kodą.
    """
    from apps.listings.models import EmailScenario

    context = context or {}

    can_send, reason = should_send(code, to_user)
    if not can_send:
        logger.info(f"[email] skipping {code} to {to_email}: {reason}")
        return False

    try:
        scenario = EmailScenario.objects.get(code=code)
    except EmailScenario.DoesNotExist:
        scenario = None
        logger.warning(
            f"[email] scenario {code} not in DB - run "
            f"'python manage.py sync_email_scenarios' first"
        )

    full_context = {
        'site_url': settings.SITE_URL,
        'site_name': 'AutoLeft',
        **context,
    }

    # Text body (REQUIRED)
    text_body = _try_render(f'emails/{code}.txt', full_context)
    if text_body is None:
        logger.error(f"[email] Missing text template: emails/{code}.txt")
        return False

    # HTML body (optional)
    html_body = _try_render(f'emails/{code}.html', full_context)

    # Subject
    if subject_override:
        subject = subject_override.strip()
    else:
        subject_rendered = _try_render(f'emails/{code}_subject.txt', full_context)
        if subject_rendered:
            # Force single line
            subject = subject_rendered.split('\n')[0].strip()
        elif scenario:
            subject = scenario.name
        else:
            subject = code

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
        reply_to=[reply_to] if reply_to else None,
    )
    if html_body:
        msg.attach_alternative(html_body, 'text/html')
    if attachments:
        for att in attachments:
            msg.attach(*att)

    try:
        result = msg.send(fail_silently=False)

        if scenario:
            scenario.send_count = (scenario.send_count or 0) + 1
            scenario.last_sent_at = timezone.now()
            scenario.save(update_fields=['send_count', 'last_sent_at'])

        logger.info(f"[email] sent {code} to {to_email}")
        return bool(result)

    except Exception as e:
        if scenario:
            scenario.fail_count = (scenario.fail_count or 0) + 1
            scenario.last_failed_at = timezone.now()
            scenario.last_error = f"{type(e).__name__}: {e}"
            scenario.save(update_fields=[
                'fail_count', 'last_failed_at', 'last_error'
            ])

        logger.error(f"[email] FAIL {code} to {to_email}: {e}")
        return False


def send_admin_scenario(code: str, context: Optional[dict] = None, **kwargs) -> bool:
    """
    Shortcut - siunčia admin email'ą (į ADMIN_EMAIL iš email_settings.py).
    """
    return send_scenario(
        code=code,
        to_email=ADMIN_EMAIL,
        context=context,
        **kwargs,
    )