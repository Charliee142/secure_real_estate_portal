from django.db import models
from django.contrib.auth.models import User
from properties.models import *


# 2️⃣ User Roles & Verification
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Verified Buyer'),
        ('seller', 'Verified Seller'),
        ('agent', 'Real Estate Agent'),
        ('owner', 'Property Owner'),
        ('landlord', 'Landlord'),
        ('renter', 'Renter'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)  # If the user is a property owner
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# 5️⃣ Security & Verification
class KYCVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_document = models.FileField(upload_to='kyc_documents/')
    address_proof = models.FileField(upload_to='kyc_documents/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    feedback  = models.TextField(blank=True, null=True)

    def is_verified(self):
        return self.status == "approved"

    def __str__(self):
        return f"KYC - {self.user.username} - {self.get_status_display()}"
    

class FraudReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fraud_reports")  # Who is reporting
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_fraud", null=False, blank=False)  # Who is being reported
    name = models.CharField(max_length=100, null=True, blank=True)  # NEW
    email = models.EmailField(null=True, blank=True)              # NEW
    property = models.CharField(max_length=255, null=True, blank=True)  # NEW - name or address of property
    message = models.TextField(null=True, blank=True)             # NEW - replaces `reason`
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fraud Report - {self.user.username} - {'Reviewed' if self.is_reviewed else 'Pending'}"


# 7️⃣ Reviews & Ratings
class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} Stars"
    

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username} - {'Resolved' if self.resolved else 'Open'}"
    

# 8️⃣ Support System
class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket by {self.user.username} - {'Resolved' if self.resolved else 'Open'}"


# 9️⃣ Marketing & Promotions
class Promotion(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expires_on = models.DateField()
    is_active = models.BooleanField(default=True)  # Soft delete flag
    
    def __str__(self):
        return f"Promo for {self.property.title} - {self.discount}% Off"
    