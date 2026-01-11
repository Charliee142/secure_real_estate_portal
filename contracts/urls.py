from django.urls import path
from . import views


urlpatterns = [
    path("transaction_history/", views.transaction_history, name="transactions"),
    path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("process-refund/<int:transaction_id>/", views.process_refund, name="process_refund"),

    path("book/<int:property_id>/", views.book_property, name="book_property"),
    path("pay/<int:property_id>/<int:duration_months>/", views.initiate_payment, name="initiate_payment"),
    path("verify/<str:reference>/", views.verify_payment, name="verify_payment"),
    path("admin/fraud-detection/", views.fraud_detection_view, name="fraud_detection"),
    
]