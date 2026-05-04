import random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from . models import AuthLog, SocialAccount
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings


User = get_user_model()

class AuthService:

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def initiate_registration(email: str, password: str, request=None):
        email = email.lower().strip()

        if User.objects.filter(email=email).exists():
            raise ValueError("User already exists with this email.")
        
        otp = AuthService.generate_otp()

        data = {
            "email": email,
            "password": make_password(password),
            "otp": otp
        }

        cache_key = f'register:{email}'
        cache.set(cache_key, data, timeout=300) # 5 minutes

        AuthService.log_action(
            email=email,
            action="otp_sent",
            request=request,
            metadata={"purpose": "registration"}
        )

        return otp
    

    @staticmethod
    def verify_registration(email: str, otp_input: str, request=None):
        email = email.lower().strip()
        cache_key = f"auth:register:{email}"

        data = cache.get(cache_key)

        if not data:
            AuthService.log_action(email, "otp_failed", request=request)
            raise ValueError("OTP expired or invalid request")

        if data["otp"] != otp_input:
            data["attempts"] += 1

            cache.set(cache_key, data, timeout=300)

            AuthService.log_action(
                email=email,
                action="otp_failed",
                request=request,
                metadata={"attempts": data["attempts"]}
            )

            raise ValueError("Invalid OTP. Please try again.")

        # Create user
        user = User.objects.create(
            email=email,
            password=data["password"],
            is_verified=True
        )

        cache.delete(cache_key)

        AuthService.log_action(
            email=email,
            action="register_completed",
            user=user,
            request=request
        )

        return user
    

    @staticmethod
    def login_user(email: str, password: str, request=None):
        email = email.lower().strip()
        user = authenticate(email=email, password=password)

        if not user:
            AuthService.log(
                email=email,
                action="login_failed",
                request=request
            )

            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        AuthService.log(
            email=email,
            action="login",
            user=user,
            request=request
        )

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    

    @staticmethod
    def log_action(email, action, user=None, request=None, metadata=None):
        AuthLog.objects.create(
            user=user,
            email=email,
            action=action,
            ip_address=getattr(request, "META", {}).get("REMOTE_ADDR") if request else None,
            user_agent=getattr(request, "META", {}).get("HTTP_USER_AGENT") if request else None,
            metadata=metadata or {}
        )





class GoogleAuthService:

    @staticmethod
    def verify_google_token(token: str):
        try:
            data = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            return data
        except Exception:
            return None

    @staticmethod
    def login_or_register(data, request=None):
        email = data.get("email")
        google_id = data.get("sub")  # unique google user id
        name = data.get("name", "")

        if not email:
            raise ValueError("Google account has no email")

        email = email.lower().strip()

        # 1. Check if social account exists
        social = SocialAccount.objects.filter(
            provider="google",
            provider_id=google_id
        ).first()

        if social:
            user = social.user

        else:
            # 2. Check if user exists with same email
            user = User.objects.filter(email=email).first()

            if not user:
                user = User.objects.create(
                    email=email,
                    username=email,
                    first_name=name,
                    is_verified=True
                )

            # 3. Link social account
            SocialAccount.objects.create(
                user=user,
                provider="google",
                provider_id=google_id,
                extra_data=data
            )

        # 4. Generate JWT
        refresh = RefreshToken.for_user(user)

        # 5. Log event (optional but production-ready)
        AuthLog.objects.create(
            user=user,
            email=email,
            action="social_login",
            ip_address=getattr(request, "META", {}).get("REMOTE_ADDR"),
            user_agent=getattr(request, "META", {}).get("HTTP_USER_AGENT"),
            metadata={"provider": "google"}
        )

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }