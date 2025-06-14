from django.contrib import admin
from .models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'amount',  'status', 'created_at')

admin.site.register(Contract)
admin.site.register(Booking)

