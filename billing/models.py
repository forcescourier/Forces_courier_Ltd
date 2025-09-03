from django.db import models

# transaction models 

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
    
