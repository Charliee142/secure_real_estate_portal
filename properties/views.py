# properties/views.py
from django.shortcuts import render, get_object_or_404
from .models import *
from contracts.models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .filters import PropertyFilter
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
import requests
from django.db.models import Count
from accounts.models import * 
from django.utils.timezone import now


def index(request):
    best_selling_property = Property.objects.filter(status='verified') \
    .annotate(sales_count=Count('transaction')) \
    .order_by('-sales_count')[:5]
    most_viewed_categories = Category.objects.order_by('-views')[:5]
    most_liked_categories = Category.objects.order_by('-likes')[:5]
   
    context = {
        'best_selling_property': best_selling_property,
        'most_viewed_categories': most_viewed_categories,
        'most_liked_categories': most_liked_categories,
    }
    return render(request, 'properties/index.html', context)


# Home Page - Show Verified Listings
def property_list(request):
    properties = Property.objects.filter(status="verified")# Show only approved listings
    property_filter = PropertyFilter(request.GET, queryset=properties)
    context = {
        'properties': properties,
        'filter': property_filter,
    }
    return render(request, 'properties/property_list.html', context)


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    promotions = Promotion.objects.filter(property=property, expires_on__gte=now().date())

    # Check if user has already rented or bought THIS property
    user_has_rented = False
    user_has_bought = False

    if request.user.is_authenticated:
        user_has_rented = Booking.objects.filter(user=request.user.userprofile, property=property, is_paid=True).exists()
        user_has_bought = Transaction.objects.filter(user=request.user.userprofile, property=property, status="success").exists()

    context = {
        'property': property,
        'user_has_rented_property': user_has_rented,
        'user_has_bought_property': user_has_bought,
        'promotions': promotions,
    }
    return render(request, 'properties/property_detail.html', context)


# Add New Property (Only Agents, Sellers, or Owners)
@login_required
def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.agent = request.user.profile  # Assign to logged-in user
            property.save()
            messages.success(request, "Property submitted for approval.")
            return redirect('index')
    else:
        form = PropertyForm()
    return render(request, 'properties/add_property.html', {'form': form})

# Approve Property (Admin Only)
@login_required
def approve_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.user.is_superuser:
        property.status = "verified"
        property.save()
        messages.success(request, "Property approved successfully!")
    return redirect('index')


def show_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.order_by('-views')[:5]
    category.views += 1
    category.save()

    pages = Property.objects.filter(category=category).order_by('-views')
    query = request.GET.get('query')
    # Search results, initially set as empty
    search_results = []
    if query:
        # Search functionality - filter pages based on the query within the current category
        search_results = pages.filter(title__icontains=query) [:5]  # Limit results for performance
        # If there are no results, show a message
        if not search_results:
            messages.info(request, "No results found for your query.")
    else:
        # If no query, show all pages in the category
        search_results = list(search_results)[:5]
        # Limit results for performance

    context = {
        'category': category,
        'categories': categories, 
        'pages': pages,
        'search_results': search_results,
        'query': query,  # To display the search term in the template if needed
    }
    return render(request, 'properties/category.html', context)


@login_required
def like_category(request):
    category_id = request.GET.get('category_id', None)
    if category_id:
        try:
            category = Category.objects.get(id=int(category_id))
            category.likes += 1
            category.save()
            return JsonResponse({'likes': category.likes})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)