from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('report_fraud/<int:reported_user_id>/', views.report_fraud, name='report_fraud'),
    path('add_review/<int:property_id>/', views.add_review, name='add_review'),

    path('update-role/', views.update_user_role, name='update_role'),
    path('kyc_verification/', views.kyc_verification, name='submit_kyc'),
    path("kyc/success/", TemplateView.as_view(template_name="account/kyc_success.html"), name="kyc_success"),
    path("kyc/status/", views.kyc_status, name="kyc_status"),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('admin/kyc/<int:kyc_id>/approve/', views.approve_kyc, name='approve_kyc'),
    path('admin/fraud/<int:report_id>/review/', views.review_fraud_report, name='review_fraud'),


    path('account_settings', views.account_settings, name='account_settings'),
    #path('account/<int:user_id>/delete/', views.delete_account, name='delete_account'),
    #path('account/<int:user_id>/delete/confirm/', views.confirm_delete_account, name='confirm_delete_account'),

    path("complaints/submit/", views.submit_complaint, name="submit_complaint"),
    path("complaints/", views.complaint_list, name="complaint_list"),
    path("complaints/<int:complaint_id>/", views.complaint_detail, name="complaint_detail"),
    path("complaints/submit/<int:property_id>/", views.submit_complaint, name="submit_complaint_with_property"),
    
    path("contact_agent/<int:property_id>", views.contact_agent, name="contact_agent"),
    path("contact_agent/confirmation/", views.contact_confirmation, name="contact_confirmation"),


    path('promotions/', views.active_promotions, name='active_promotions'),
    path('promotions/<int:property_id>/', views.property_promotions, name='property_promotions'),
    path('promotions/add/', views.add_promotion, name='add_promotion'),
    path('promotions/edit/<int:promo_id>/', views.edit_promotion, name='edit_promotion'),
    path('promotions/delete/<int:promo_id>/', views.delete_promotion, name='delete_promotion'),
    path('promotions/undo/<int:promo_id>/', views.undo_delete_promotion, name='undo_delete_promotion'),

]