from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<slug:slug>/', views.property_detail, name='property_detail'),
    path('add_property/', views.add_property, name='add_property'),
    path('approve_property/<int:pk>/', views.approve_property, name='approve_property'),

    path('category/<slug:slug>/', views.show_category, name='show_category'),
    path('like/', views.like_category, name='like_category'),
    #path('about/', views.about, name='about'),
    #path('contact/', views.contact, name='contact'),
]