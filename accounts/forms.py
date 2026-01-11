from django import forms
from allauth.account.forms import SignupForm
from .models import *
from django.core.validators import RegexValidator


class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
        required=True
    )
    address = forms.CharField(max_length=255, required=True)
    profile_picture = forms.ImageField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Create a user profile
        UserProfile.objects.create(
            user=user,
            phone_number=self.cleaned_data.get("phone_number"),
            address=self.cleaned_data.get("address"),
            profile_picture=self.cleaned_data.get("profile_picture"),
        )
        return user


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']


class KYCVerificationForm(forms.ModelForm):
    class Meta:
        model = KYCVerification
        fields = ['id_document', 'address_proof']


class FraudReportForm(forms.ModelForm):
    class Meta:
        model = FraudReport
        fields = ['name', 'email', 'property', 'message']

class KYCApprovalForm(forms.ModelForm):
    class Meta:
        model = KYCVerification
        fields = ['status', 'feedback']


class FraudReportReviewForm(forms.ModelForm):
    class Meta:
        model = FraudReport
        fields = ['is_reviewed']


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["property", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": "Describe your complaint"}),
        }


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['property', 'discount', 'expires_on']
        widgets = {
            'expires_on': forms.DateInput(attrs={'type': 'date'}),
        }