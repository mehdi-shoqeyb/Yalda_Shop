from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name = 'register-page'),
    path('login/',views.LoginView.as_view(),name = 'login-page'),
    path('logout/',views.Logout,name = 'login-out-page'),
    path('otp/',views.OTPView.as_view(),name = 'otp-page'),
    path('otp-generate/',views.otp_generate,name='otp-generate')
]
