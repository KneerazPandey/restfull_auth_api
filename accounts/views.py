from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from . service import AuthService, GoogleAuthService
from . serializers import (
    RegisterSerializer, VerifyOTPSerializer, LoginSerializer, UserSerializer, 
    GoogleAuthSerializer
)

class RegisterView(APIView):
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                AuthService.initiate_registration(email=email, password=password, request=request)

                return Response({
                    "email": email,
                    "message": "OTP has been sent to your email.",
                })

            except ValueError as e:
                return Response({"error": str(e)}, status=400)
        

class VerifyEmailView(APIView):

    def post(self, request: Request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]

            try:
                user = AuthService.verify_registration(
                    email=email,
                    otp_input=otp,
                    request=request
                )

                return Response({
                    "message": "Email verified successfully",
                    "user_id": user.id,
                    "email": user.email
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                result = AuthService.login_user(email=email, password=password, request=request)

                user_data = UserSerializer(result["user"]).data

                return Response({
                    "user": user_data,
                    "access": result["access"],
                    "refresh": result["refresh"]
                })

            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data["id_token"]

            google_data = GoogleAuthService.verify_google_token(token)

            if not google_data:
                return Response(
                    {"error": "Invalid Google token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                print(google_data)
                result = GoogleAuthService.login_or_register(
                    google_data,
                    request=request
                )

                return Response({
                    "user": UserSerializer(result["user"]).data,
                    "access": result["access"],
                    "refresh": result["refresh"]
                })

            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )