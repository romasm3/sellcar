from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_banner_image_profile_contact_person_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wallet_balance',
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10,
                verbose_name='Wallet Balance (points)'
            ),
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(
                    decimal_places=2, max_digits=10,
                    help_text='Positive for top-ups, negative for spends',
                    verbose_name='Amount (points)'
                )),
                ('bonus_amount', models.DecimalField(
                    decimal_places=2, default=0, max_digits=10,
                    verbose_name='Bonus points'
                )),
                ('transaction_type', models.CharField(
                    choices=[
                        ('topup', 'Top-up'),
                        ('bonus', 'Bonus'),
                        ('spend', 'Spend'),
                        ('refund', 'Refund'),
                        ('test_topup', 'Test top-up'),
                    ],
                    default='topup', max_length=20
                )),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('completed', 'Completed'),
                        ('failed', 'Failed'),
                        ('refunded', 'Refunded'),
                    ],
                    default='pending', max_length=20
                )),
                ('description', models.CharField(blank=True, max_length=200)),
                ('stripe_session_id', models.CharField(blank=True, db_index=True, max_length=200)),
                ('stripe_payment_intent', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='wallet_transactions',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Wallet Transaction',
                'verbose_name_plural': 'Wallet Transactions',
                'ordering': ['-created_at'],
            },
        ),
    ]