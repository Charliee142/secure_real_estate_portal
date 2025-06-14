from django.contrib import admin
from .models import *


admin.site.register(UserProfile)
admin.site.register(KYCVerification)
admin.site.register(FraudReport)
admin.site.register(Review)
admin.site.register(Complaint)
admin.site.register(SupportTicket)
admin.site.register(Promotion)

