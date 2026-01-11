# accounts/views.py
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


# Admin permission check
def is_admin(user):
    return user.is_staff or user.is_superuser


# Admin KYC Approval
@login_required
@user_passes_test(is_admin)
def approve_kyc(request, kyc_id):
    kyc = get_object_or_404(KYCVerification, id=kyc_id)

    if request.method == "POST":
        form = KYCApprovalForm(request.POST, instance=kyc)
        if form.is_valid():
            form.save()
            if kyc.status == 'approved':
                kyc.is_verified = True
                kyc.save()
                send_mail(
                    "KYC Approved",
                    f"Dear {kyc.user.username}, your KYC verification has been approved!",
                    "admin@realestate.com",
                    [kyc.user.email],
                    fail_silently=True,
                )
            elif kyc.status == 'rejected':
                send_mail(
                    "KYC Rejected",
                    f"Dear {kyc.user.username}, your KYC verification has been rejected.\nReason: {kyc.rejection_reason}",
                    "admin@realestate.com",
                    [kyc.user.email],
                    fail_silently=True,
                )
            messages.success(request, "KYC status updated successfully.")
            return redirect('admin_kyc_list')
    else:
        form = KYCApprovalForm(instance=kyc)

    return render(request, "admin/approve_kyc.html", {"form": form, "kyc": kyc})


# Admin Fraud Report Review
@login_required
@user_passes_test(is_admin)
def review_fraud_report(request, report_id):
    report = get_object_or_404(FraudReport, id=report_id)
    
    if request.method == "POST":
        form = FraudReportReviewForm(request.POST, instance=report)
        if form.is_valid():
            report.is_reviewed = True  # Mark as reviewed
            form.save()

            # Send email notification to the user
            send_mail(
                "Fraud Report Reviewed",
                f"Dear {report.user.username},\n\nYour fraud report titled '{report.title}' has been reviewed by our team.",
                "charlespeter142@gmail.com",
                [report.user.email],
                fail_silently=True,
            )
            messages.success(request, "Fraud report reviewed successfully.")
            return redirect('admin_fraud_reports')
    else:
        form = FraudReportReviewForm(instance=report)

    return render(request, "admin/review_fraud.html", {"form": form, "report": report})

# Report Fraud
@login_required
def report_fraud(request, reported_user_id):
    reported_user = get_object_or_404(User, id=reported_user_id)
    FraudReport.objects.create(reported_by=request.user, reported_user=reported_user, reason="Fraudulent activity detected.")
    messages.success(request, "Fraud report submitted successfully.")
    return redirect('index')


@login_required
def add_review(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('property_detail', slug=property.slug)
    else:
        form = ReviewForm()
    return render(request, 'account/add_review.html', {'form': form, 'property': property})

@login_required
def update_user_role(request):
    """View for updating user role"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User role updated successfully.")
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'account/update_role.html', {'form': form})


@login_required
def kyc_verification(request):
    """View for submitting KYC documents"""
    kyc, created = KYCVerification.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = KYCVerificationForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc_instance = form.save()

            # Email to admins
            subject = "New KYC Submission"
            message = render_to_string('emails/kyc_admin_notification.html', {
                'user': request.user,
                'kyc': kyc_instance,
            })
            email = EmailMessage(
                subject, message, settings.DEFAULT_FROM_EMAIL,
                [admin[1] for admin in settings.ADMINS]
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)

            # Email to user
            site = get_current_site(request)
            user_subject = "KYC Verification Submitted"
            user_message = render_to_string('emails/kyc_user_confirmation.html', {
                'user': request.user,
                'site_name': site.name,
            })
            user_email = EmailMessage(
                user_subject, user_message, settings.DEFAULT_FROM_EMAIL,
                [request.user.email]
            )
            user_email.content_subtype = "html"
            user_email.send(fail_silently=True)

            return redirect('kyc_success')
    else:
        form = KYCVerificationForm(instance=kyc)

    return render(request, 'account/kyc_verification.html', {'form': form})


@login_required
def kyc_status(request):
    kyc = KYCVerification.objects.filter(user=request.user).first()
    return render(request, 'account/kyc_status.html', {'kyc': kyc})


@login_required
def report_fraud(request, reported_user_id):
    reported_user = get_object_or_404(User, id=reported_user_id)

    if request.method == "POST":
        form = FraudReportForm(request.POST)
        if form.is_valid():
            fraud_report = form.save(commit=False)
            fraud_report.user = request.user
            fraud_report.reported_user = reported_user
            fraud_report.save()

            # Prepare HTML email
            subject = "🚨 Fraud Report Submitted"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_emails = [admin[1] for admin in settings.ADMINS]  # List of admin emails

            context = {
                'name': fraud_report.name,
                'email': fraud_report.email,
                'property': fraud_report.property,
                'message': fraud_report.message,
            }

            html_content = render_to_string('emails/fraud_report_email.html', context)
            text_content = f"""
            Fraud Report Submitted:
            Name: {fraud_report.name}
            Email: {fraud_report.email}
            Property: {fraud_report.property}
            Message: {fraud_report.message}
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return render(request, 'account/fraud_report_confirmation.html')
    else:
        form = FraudReportForm()
    return render(request, "account/report_fraud.html", {"form": form, "reported_user": reported_user})


@login_required
def dashboard(request):
    fraud_reports = FraudReport.objects.filter(user=request.user)  # Reports made by the user
    all_users = User.objects.exclude(id=request.user.id)  # Exclude self

    return render(request, "account/dashboard.html", {
        "user": request.user,
        "fraud_reports": fraud_reports,
        "all_users": all_users  # Send all users to template
    })


def profile(request):
    user_profile = request.user.profile
    user_properties = Property.objects.filter(owner=user_profile)

    return render(request, 'account/profile.html', {
        'profile': user_profile,
        'properties': user_properties
    })


@login_required
def submit_complaint(request, property_id=None):
    property_instance = None
    if property_id:
        property_instance = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.property = property_instance
            complaint.save()
            messages.success(request, "Your complaint has been submitted successfully.")
            return redirect("complaint_list")
    else:
        form = ComplaintForm()

    return render(request, "complaints/submit_complaint.html", {"form": form, "property": property_instance})

@login_required
def complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "complaints/complaint_list.html", {"complaints": complaints})

@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    return render(request, "complaints/complaint_detail.html", {"complaint": complaint})


def active_promotions(request):
    """View to list all active promotions."""
    promotions = Promotion.objects.filter(is_active=True)
    return render(request, 'promotions/active_promotions.html', {'promotions': promotions})


def property_promotions(request, property_id):
    """View to list promotions for a specific property."""
    property_obj = get_object_or_404(Property, id=property_id)
    promotions = Promotion.objects.filter(property=property_obj, expires_on__gte=now().date())
    return render(request, 'promotions/property_promotions.html', {'property': property_obj, 'promotions': promotions})


def add_promotion(request):
    """View to add a new promotion."""
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('active_promotions')
    else:
        form = PromotionForm()
    
    return render(request, 'promotions/add_promotion.html', {'form': form})


def edit_promotion(request, promo_id):
    """View to edit an existing promotion."""
    promotion = get_object_or_404(Promotion, id=promo_id)
    
    if request.method == 'POST':
        form = PromotionForm(request.POST, instance=promotion)
        if form.is_valid():
            form.save()
            return redirect('active_promotions')
    else:
        form = PromotionForm(instance=promotion)
    
    return render(request, 'promotions/edit_promotion.html', {'form': form, 'promotion': promotion})


@require_http_methods(["DELETE"])
def delete_promotion(request, promo_id):
    try:
        promo = Promotion.objects.get(pk=promo_id)
        promo.is_active = False
        promo.save()
        request.session['last_deleted_promo_id'] = promo.id  # store promo ID for undo
        return JsonResponse({'success': True})
    except Promotion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Promotion not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def undo_delete_promotion(request, promo_id):
    try:
        promo = Promotion.objects.get(pk=promo_id)
        if not promo.is_active:
            promo.is_active = True
            promo.save()

            return redirect('active_promotions')  # Replace with your correct URL name
        else:
            return JsonResponse({'success': False, 'error': 'Promotion is already active'}, status=400)
    except Promotion.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Promotion not found'}, status=404)
    

def contact_agent(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # --- Email to Agent ---
        subject_agent = f"New Inquiry About {property.title}"
        context = {
            'name': name,
            'email': email,
            'message': message,
            'property': property
        }

        html_content_agent = render_to_string("emails/contact_agent_email.html", context)
        text_content_agent = f"From: {name} <{email}>\n\nMessage:\n{message}"

        msg_agent = EmailMultiAlternatives(
            subject_agent,
            text_content_agent,
            'noreply@yourdomain.com',
            [property.owner.user.email]
        )
        msg_agent.attach_alternative(html_content_agent, "text/html")
        msg_agent.send()

        # --- Email to User ---
        subject_user = f"Copy of your message to agent - {property.title}"
        html_content_user = render_to_string("emails/contact_user_copy.html", context)
        text_content_user = f"Hi {name},\n\nHere’s a copy of the message you sent:\n\n{message}"

        msg_user = EmailMultiAlternatives(
            subject_user,
            text_content_user,
            'noreply@yourdomain.com',
            [email]
        )
        msg_user.attach_alternative(html_content_user, "text/html")
        msg_user.send()

        return redirect(reverse('contact_confirmation') + f"?property={property.title}")

    return render(request, 'account/contact_agent.html', {'property': property})


def contact_confirmation(request):
    property_title = request.GET.get('property', 'the property')
    return render(request, 'account/contact_confirmation.html', {'property_title': property_title})


@login_required
def account_settings(request):
    return render(request, 'account/account_settings.html')
