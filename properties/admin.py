from django.contrib import admin
from .models import *



admin.site.site_header = "Secure Real Estate Admin"
admin.site.site_title = "Real Estate Portal"
admin.site.index_title = "Admin Dashboard"


class RentalPriceInline(admin.TabularInline):
    model = RentalPrice
    extra = 1  # Allows adding new rental price rows

    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'views', 'likes', 'slug')
    search_fields = ('name',)


class PropertyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'category', 'is_rental', 'location', 'status')
    inlines = [RentalPriceInline]  # Adds RentalPrice inline form
    search_fields = ('title', 'category', 'location', 'agent')
    list_editable = ('status',)  # Allow quick approval from the admin panel
   
    list_filter = ('status', 'category', 'location')

    def approve_properties(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected properties have been approved.")
    approve_properties.short_description = "Approve selected properties"


class RentalPriceAdmin(admin.ModelAdmin):
    list_display = ('property', 'months', 'price')
    list_filter = ('months', 'property')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(RentalPrice, RentalPriceAdmin)

