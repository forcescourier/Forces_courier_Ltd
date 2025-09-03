from django.db import models

# Statement model

class Statement(models.Model):
    statement_id=models.AutoField(primary_key=True)
    statement_transaction_id=models.ForeignKey('billing.Transaction',on_delete=models.CASCADE,related_name='statements')
    statement_credit_amount=models.DecimalField(max_digits=10, decimal_places=2)
    statement_created_at=models.DateTimeField(auto_now_add=True)
    statement_updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.statement_id