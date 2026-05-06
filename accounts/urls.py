from django.urls import path
from . views import (
    RegisterView, LoginView, GoogleAuthView, VerifyEmailView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),

    path('verify-email-otp/', VerifyEmailView.as_view(), name='verify-email-otp'),

    path('google/', GoogleAuthView.as_view(), name='google'),
]