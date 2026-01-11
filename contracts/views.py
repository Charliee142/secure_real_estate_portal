# contracts/views.py
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import json
import requests
from django.conf import settings
from django.urls import reverse
import uuid
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from .utils import detect_fraudulent_listings


@staff_member_required
def fraud_detection_view(request):
    flagged_properties = detect_fraudulent_listings()
    return render(request, "admin/fraud_detection.html", {"flagged_properties": flagged_properties})


def contract_detail(request, pk):
    contract = Contract.objects.get(pk=pk)
    return render(request, 'contracts/contract_detail.html', {'contract': contract})


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user.userprofile,).order_by("-created_at")
    return render(request, "contracts/transactions_history.html", {"transactions": transactions})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user.userprofile, status="pending")

    # Delete transaction if exists
    if booking.transaction:
        booking.transaction.delete()
    
    booking.delete()
    messages.success(request, "Booking has been canceled successfully.")
    return redirect("contracts/transaction_history")


@staff_member_required
def process_refund(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, status="completed")

    url = f"https://api.paystack.co/refund"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "transaction": transaction.reference,
        "amount": int(transaction.amount * 100)  # Convert to kobo
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    res = response.json()

    if res.get("status"):
        transaction.status = "refunded"
        transaction.save()
        messages.success(request, "Refund processed successfully.")
    else:
        messages.error(request, "Refund failed. Try again later.")

    return redirect("admin:transactions_transaction_changelist")


@login_required
def book_property(request, property_id):
    """
    Handles property booking for rentals.
    """
    property = get_object_or_404(Property, id=property_id)

    if not property.is_rental:
        messages.error(request, "This property is for sale, not rental.")
        return redirect("property_detail", slug=property.slug)

    # Check if user has already booked
    if Booking.objects.filter(user=request.user.userprofile, property=property, is_paid=True).exists():
        messages.warning(request, "You have already booked this property.")
        return redirect('property_detail', slug=property.slug)

    if request.method == "POST":
        months = int(request.POST.get("months", 1))  # Default to 1 month if not provided
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30 * months)  # Approximate months as 30 days each

        # Retrieve rental price based on selected months
        rental_price = property.get_rental_price(months)
        if rental_price is None:
            messages.error(request, f"Rental price for {months} month(s) is not available.")
            return redirect('property_detail', slug=property.slug)

        # Create a pending booking
        booking = Booking.objects.create(
            user=request.user.userprofile,
            property=property,
            amount=rental_price,
            status="Pending",
            start_date=start_date,
            end_date=end_date,
            months=months
        )

        messages.success(request, f"Property booked for {months} month(s). Proceed to payment.")
        return redirect('initiate_payment', property_id=property.id, duration_months=months)
    return render(request, "contracts/book_property.html", {"property": property})


@login_required
def initiate_payment(request, property_id, duration_months=None):
    """
    Handles payment initiation for both rentals and sales.
    """
    property = get_object_or_404(Property, id=property_id)

    # Check if user has already paid for this property
    if Booking.objects.filter(user=request.user.userprofile, property=property, is_paid=True).exists():
        messages.warning(request, "You have already paid for this property.")
        return redirect('property_detail', slug=property.slug)

    # Determine the correct price based on rental or sale
    if property.is_rental:
        if duration_months is None:
            messages.error(request, "Duration is required for rental payment.")
            return redirect('property_detail', slug=property.slug)

        amount = property.get_rental_price(duration_months)
        if amount is None:
            messages.error(request, f"Rental price for {duration_months} month(s) is not available.")
            return redirect('property_detail', slug=property.slug)
    else:
        amount = property.sale_price  # Sale price

    if amount is None:
        messages.error(request, "Invalid property price.")
        return redirect('property_detail', slug=property.slug)

    # Generate unique payment reference
    reference = str(uuid.uuid4())

    # Create pending transaction
    transaction = Transaction.objects.create(
        user=request.user.userprofile,
        property=property,
        transaction_type="rent" if property.is_rental else "sale",
        amount=amount,
        reference=reference,
        status="pending"
    )

    # If rental, link the transaction to a booking
    if property.is_rental:
        Booking.objects.create(
            user=request.user.userprofile,
            property=property,
            amount=amount,
            status="Pending",
            transaction=transaction,
            months=duration_months
        )

    # Paystack API Call
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": request.user.email,
        "amount": int(Decimal(amount) * 100),  # Convert to kobo
        "reference": reference,
        "callback_url": request.build_absolute_uri(reverse('verify_payment', args=[reference]))
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    res = response.json()

    if res.get("status"):
        return redirect(res["data"]["authorization_url"])  # Redirect to Paystack Payment Page
    else:
        transaction.delete()
        messages.error(request, "Error initializing payment. Try again.")
        return redirect("property_detail", slug=property.slug)


@login_required
def verify_payment(request, reference):
    """
    Verifies payment status from Paystack and updates booking/transaction status.
    """
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    res = response.json()

    transaction = get_object_or_404(Transaction, reference=reference)

    if res.get("status") and res["data"]["status"] == "success":
        transaction.status = "success"
        transaction.save()

        # If rental, update booking status
        if transaction.transaction_type == "rent":
            booking = Booking.objects.get(transaction=transaction)
            booking.status = "Paid"
            booking.is_paid = True
            booking.save()

        messages.success(request, "Payment successful! Booking confirmed.")
        return redirect("transactions")
    else:
        transaction.status = "failed"
        transaction.save()
        messages.error(request, "Payment verification failed. Contact support.")
    return redirect("property_detail", slug=transaction.property.slug)