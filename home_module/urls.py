from django.urls import path 
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    path('contact-us/',views.ContactUs.as_view(),name='contact-us-page')
]
