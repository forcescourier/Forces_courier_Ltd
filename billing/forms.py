# billing/forms.py

from django import forms
from .models import Payment, SoldierPayment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "customer_name",
            "customer_phone",
            "customer_email",
            "payment_type",
            "reference_number",
            "amount",
            "payment_method",
            "transaction_id",
            "account_number",
            "card_last4",
            "auth_code",
            "notes",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter full name"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"}),
            "customer_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}),

            "payment_type": forms.Select(attrs={"class": "form-control"}),
            "reference_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional reference number"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0.00"}),

            "payment_method": forms.Select(attrs={"class": "form-control"}),

            "transaction_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mobile money transaction ID"}),
            "account_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mobile account number"}),

            "card_last4": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last 4 digits"}),
            "auth_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Card authorization code"}),

            "notes": forms.Textarea(attrs={"class": "form-control", "placeholder": "Additional notes", "rows": 3}),
        }

    def clean(self):
        """
        Custom validation depending on payment method.
        """
        cleaned_data = super().clean()
        method = cleaned_data.get("payment_method")

        if method in ["bkash", "nagad", "rocket"]:
            if not cleaned_data.get("transaction_id"):
                self.add_error("transaction_id", "Transaction ID is required for mobile money payments.")
            if not cleaned_data.get("account_number"):
                self.add_error("account_number", "Account number is required for mobile money payments.")

        if method == "card":
            if not cleaned_data.get("card_last4"):
                self.add_error("card_last4", "Last 4 digits are required for card payments.")
            if not cleaned_data.get("auth_code"):
                self.add_error("auth_code", "Authorization code is required for card payments.")

        return cleaned_data
    




class SoldierPaymentForm(forms.ModelForm):
    class Meta:
        model = SoldierPayment
        fields = ['total_charge', 'total_cod', 'total_payable', 'payment_method']
        widgets = {
            'total_charge': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_cod': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_payable': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

