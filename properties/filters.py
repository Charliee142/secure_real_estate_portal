import django_filters
from .models import *


class PropertyFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()  # Allows filtering by price range
    location = django_filters.CharFilter(lookup_expr='icontains')  # Allows filtering by location (case-insensitive match)
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),  # All available categories
        field_name='category',            # Filter on the 'category' field of Property model
        to_field_name='name'              # Match by category name (instead of ID)
    )

    class Meta:
        model = Property
        fields = ['location', 'price', 'category']