from django.db import models
from properties.models import *
from accounts.models import User
from django.utils import timezone
from datetime import timedelta


def default_end_date():
    return timezone.now().date() + timedelta(days=30)


class Booking(models.Model):
    user = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now)  # Defaults to the current date
    end_date = models.DateField(default=default_end_date)  # Use function instead of lambda
    months = models.PositiveIntegerField(default=1)  
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')],
        default='Pending', db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)  
    transaction = models.OneToOneField('Transaction', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.property.title} ({'Paid' if self.is_paid else 'Pending'}) for ({self.months} months)"
    
    
# 4️⃣ Transactions & Payments
class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('rent', 'Rent Payment'),
        ('sale', 'Property Sale'),
        ('deposit', 'Security Deposit'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)  # Paystack Reference
    status = models.CharField(max_length=20, default="pending", db_index=True)  # pending, completed, failed
    
    def __str__(self):
        return f"{self.property.title} - {self.status}"


# 6️⃣ Contracts & Agreements
class Contract(models.Model):
    CONTRACT_TYPE = [
        ('lease', 'Digital Lease Agreement'),
        ('sale', 'Sales Contract'),
        ('rental', 'Rental Agreement'),
        ('dispute', 'Dispute Resolution Case'),
    ]
    
    user = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE)
    document = models.FileField(upload_to='contracts/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_contract_type_display()} - {self.user.username}"
    

class EscrowTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('held', 'Funds Held'),
        ('released', 'Released'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyers')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    subaccount_code = models.CharField(max_length=255, blank=True, null=True)  # Paystack Subaccount
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Escrow {self.transaction_id} - {self.payment_status}"
    

class LeaseAgreement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Signing'),
        ('signed', 'Signed'),
        ('cancelled', 'Cancelled'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='landlord_agreements')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_agreements')
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    lease_start = models.DateField()
    lease_end = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.status == "pending" and timezone.now() > self.created_at + timezone.timedelta(days=7)  # 7 days deadline
    

class InstallmentPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('released', 'Released'),
    ]
    escrow = models.ForeignKey(EscrowTransaction, on_delete=models.CASCADE)
    milestone = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.milestone} - {self.payment_status}"

class RentalPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
    ]
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent_payments')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_payments')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    transaction_ref = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rental Payment - {self.property.title} - {self.status}"
    

class SalesInstallment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('released', 'Released'),
    ]
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_installments')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_payments')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    milestone = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    transaction_ref = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.property.title} - {self.milestone} - {self.status}"
