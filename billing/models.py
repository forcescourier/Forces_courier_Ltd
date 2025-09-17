from django.db import models

# transaction models 

class Payment(models.Model):
    PAYMENT_TYPES = [
        ("parcel_payment", "Parcel Payment"),
        ("cod_collection", "COD Collection"),
        ("advance_payment", "Advance Payment"),
        ("merchant_settlement", "Merchant Settlement"),
    ]

    METHODS = [
        ("cash", "Cash"),
        ("card", "Credit/Debit Card"),
        ("bkash", "bKash"),
        ("nagad", "Nagad"),
        ("rocket", "Rocket"),
        ("bank_transfer", "Bank Transfer"),
    ]

    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_email = models.EmailField(blank=True, null=True)

    payment_type = models.CharField(max_length=30, choices=PAYMENT_TYPES)
    reference_number = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=METHODS)

    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    auth_code = models.CharField(max_length=20, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference_number or 'Payment'} - {self.amount}"

class Transaction(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    transaction_parcel_id=models.ForeignKey('parcels.Parcel',on_delete=models.CASCADE,related_name='transactions')
    transaction_marchant_id=models.ForeignKey('accounts.Merchant',on_delete=models.CASCADE,related_name='transactions')
    transaction_amount=models.DecimalField(max_digits=10,decimal_places=2)
    transaction_status=models.CharField(max_length=50)
    transaction_created_at=models.DateTimeField(auto_now_add=True)
    transaction_updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.transaction_status}"
    

# invoice model
class Invoice(models.Model):
    invoice_id=models.AutoField(primary_key=True)
    invoice_transaction_id=models.ForeignKey('Transaction',on_delete=models.CASCADE,related_name='invoices')
    invoice_amount=models.DurationField(max_length=10)
    invoice_status=models.CharField(max_length=50)
    invoice_created_at=models.DateTimeField(auto_now_add=True)
    invoice_updated_at=models.DateTimeField(auto_now=True)
    def __STR__(self):
        return f"Invoice {self.invoice_id} - {self.invoice_status}"
    
