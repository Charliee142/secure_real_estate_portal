# properties/models.py
from django.db import models
from datetime import timedelta, datetime
from django.utils.text import slugify
#from accounts.models import UserProfile



# 1️⃣ Property Categories
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '-').lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Property(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('verified', 'Verified Listing'),
        ('rejected', 'Rejected Listing'),
        ('expired', 'Expired Listing'),
    ]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='property_images/')
    owner = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="properties")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    expiry_date = models.DateTimeField(null=True, blank=True) # Expiry feature
    reported_count = models.IntegerField(default=0) # Fraud detection
    is_rental = models.BooleanField(default=False)  # True for rentals, False for sales
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # Sale price if not rental
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update timestamp
    slug = models.SlugField(unique=True, blank=True, null=True)    

    class Meta:
        verbose_name_plural = 'Properties'

    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-set expiry date to 30 days from creation
        if not self.expiry_date:
            self.expiry_date = datetime.now() + timedelta(days=30)

        super(Property, self).save(*args, **kwargs)


    def is_expired(self):
        return self.expiry_date and self.expiry_date < datetime.now()
    
    def mark_as_expired(self):
        """Automatically mark listing as expired if past expiry date."""
        if self.is_expired():
            self.status = 'expired'
            self.save()

    def report_fraud(self):
        """Increase fraud report count and reject listing if too many reports."""
        self.reported_count += 1
        if self.reported_count >= 5:  # Threshold for automatic rejection
            self.status = 'rejected'
        self.save()
        return self.reported_count
    
    def __str__(self):
        return f"{self.title} ({'Rental' if self.is_rental else 'Sale'})"
    

    def get_rental_price(self, months):
        """Fetch rental price for a specific duration in months."""
        rental_price = self.rental_prices.filter(months=months).first()
        return rental_price.price if rental_price else None
    
    def __str__(self):
        return f"{self.title} ({'Rental' if self.is_rental else 'Sale'})"
    

    def get_price(self, months=None):
        """Return the correct price based on property type (sale or rental)."""
        if self.is_rental and months:
            return self.get_rental_price(months)
        return self.sale_price  # Return sale price if not a rental
    
    def __str__(self):
        return f"{self.title} ({'Rental' if self.is_rental else 'Sale'})"
    

class RentalPrice(models.Model):
    """
    Stores rental pricing for different durations (e.g., 1 month, 2 months, etc.).
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rental_prices")
    months = models.PositiveIntegerField()  # Example: 1, 2, 3 months, etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for this duration

    class Meta:
        unique_together = ('property', 'months')  # Ensures no duplicate durations for a property
        ordering = ['months'] # Order by months ascending

    def __str__(self):
        return f"{self.property.title} - {self.months} month(s): ${self.price}"