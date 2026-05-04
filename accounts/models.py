import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . managers import AuthenticationUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4, db_index=True)
    email = models.EmailField(unique=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = AuthenticationUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
    



class SocialAccount(models.Model):
    PROVIDER_CHOICES = (
        ("google", "Google"),
        ("facebook", "Facebook"),
        ("apple", "Apple"),

    )

    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_uid = models.CharField(max_length=255)

    # optional metadata
    extra_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("provider", "provider_uid")

    def __str__(self):
        return f"{self.provider} - {self.user.email}"



# class OTP(models.Model):
#     PURPOSE_CHOICES = (
#         ("email_verification", "Email Verification"),
#         ("password_reset", "Password Reset"),
#         ("login", "Login"),
#     )

#     email = models.EmailField()
#     code = models.CharField(max_length=6)

#     purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)

#     is_used = models.BooleanField(default=False)
#     expires_at = models.DateTimeField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def is_valid(self):
#         from django.utils import timezone
#         return not self.is_used and self.expires_at > timezone.now()
    


class AuthLog(models.Model):
    ACTION_CHOICES = (
        ("login", "Login"),
        ("login_failed", "Login Failed"),

        ("logout", "Logout"),

        ("otp_sent", "OTP Sent"),
        ("otp_failed", "OTP Failed"),
        ("otp_verified", "OTP Verified"),

        ("register_completed", "Register Completed"),
        
        ("social_login", "Social Login"),
    )

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(null=True, blank=True)

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.email if self.email else "Someone"} has an action of {self.action} on {self.created_at}'