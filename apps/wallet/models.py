class Wallet(models.Model):
    user = OneToOneField(User)
    balance = DecimalField(default=0)  # USD
    
class WalletTransaction(models.Model):
    wallet = ForeignKey(Wallet)
    amount = DecimalField  # +/- (positive=top-up, negative=spend)
    type = CharField(choices=['topup', 'listing_fee', 'boost', 'refund', 'admin_adjust'])
    description = CharField
    balance_after = DecimalField
    listing = FK(Listing, optional)  # jei susiję su listing
    stripe_payment_id = CharField(blank)  # tuščias dabar, užpildysim su Stripe
    status = CharField(['pending', 'completed', 'failed', 'refunded'])
    created_at = DateTimeField