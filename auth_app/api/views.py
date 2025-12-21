from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    RegistrationResponseSerializer,
    CustomerProfileSerializer,
    BusinessProfileSerializer
)
from django.contrib.auth.models import User
from profile_app.models import CustomerProfile, BusinessProfile
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication

def get_token_response(user):
    """
    Helper function to generate token response.
    """
    token, created = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id
    }

class RegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    Handles creation of new users and returns token response.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Use the RegistrationResponseSerializer for consistent response format
        response_serializer = RegistrationResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    """
    View for user login.
    Handles authentication and returns token response.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response_serializer = RegistrationResponseSerializer(user)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerListView(generics.ListAPIView):
    """
    View to list all customer profiles.
    Returns customer data in the required format. 
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = CustomerProfile.objects.all()

class BusinessListView(generics.ListAPIView):
    """
    View to list all business profiles.
    Returns business data in the required format.
    """
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = BusinessProfile.objects.all()