"""
Test email sending.

Naudojimas:
    python manage.py test_email
    python manage.py test_email --to kitas@email.com
"""
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Siunčia test email, kad patikrintum ar SMTP veikia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default=None,
            help='Email adresas kur siųsti (default: EMAIL_USER iš settings)',
        )

    def handle(self, *args, **options):
        to_email = options['to'] or settings.EMAIL_HOST_USER

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write("TEST EMAIL")
        self.stdout.write(f"{'='*60}")
        self.stdout.write(f"Backend:  {settings.EMAIL_BACKEND}")
        self.stdout.write(f"From:     {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"To:       {to_email}")
        self.stdout.write(f"SMTP:     {getattr(settings, 'EMAIL_HOST', 'N/A')}:{getattr(settings, 'EMAIL_PORT', 'N/A')}")
        self.stdout.write(f"{'='*60}\n")

        if 'console' in settings.EMAIL_BACKEND:
            self.stdout.write(self.style.WARNING(
                "ĮSPĖJIMAS: EMAIL_BACKEND = console. Email'as tik printinamas terminale, "
                "nesiunčiamas realiai.\n"
                "Jei nori realaus siuntimo - .env faile išimk EMAIL_USE_CONSOLE=True arba nustatyk į False."
            ))
            self.stdout.write("")

        subject = "✅ AutoLeft SMTP Test"
        body = (
            "Sveikas!\n\n"
            "Jei matai šį email, reiškia AutoLeft SMTP konfigūracija veikia.\n\n"
            "- Projektas: AutoLeft\n"
            f"- Serveris: {settings.SITE_URL}\n"
            f"- Backend: {settings.EMAIL_BACKEND}\n\n"
            "Sėkmės!\n"
        )

        try:
            result = send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,  # KRITIŠKA: False, kad matytume klaidas
            )

            if result == 1:
                self.stdout.write(self.style.SUCCESS(
                    f"✓ Email išsiųstas! Patikrink {to_email} inbox (ir spam)."
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    f"✗ send_mail grąžino {result} (tikėtasi 1)"
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n✗ KLAIDA:\n{type(e).__name__}: {e}\n"))
            self.stdout.write(self.style.WARNING(
                "Galimi sprendimai:\n"
                "  1. Patikrink .env: EMAIL_USER ir EMAIL_PASSWORD\n"
                "  2. EMAIL_PASSWORD turi būti Gmail App Password (16 simb, be tarpų)\n"
                "     Pvz: 'gvayuxpmppucmreg', NE 'gvay uxpm ppuc mreg'\n"
                "  3. Gmail account turi turėti 2-Step Verification įjungtą\n"
                "  4. Patikrink ar uždarytas port 587 firewall'e\n"
            ))