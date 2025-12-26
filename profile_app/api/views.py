from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializer import(
    BusinessSerializer,
    CustomerSerializer,
    BusinessProfileUpdateSerializer,
    CustomerProfileUpdateSerializer
)
from auth_app.models import CustomUser
from profile_app.models import BusinessProfile, CustomerProfile
from django.shortcuts import get_object_or_404

class BusinessListView(generics.ListAPIView):
    """
    Returns a list of all business profiles.
    Only authenticated users are allowed.
    """
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Return BusinessProfile objects, not User objects
        return BusinessProfile.objects.all()

class CustomerListView(generics.ListAPIView):
    """
    Returns a list of all customer profiles.
    Only authenticated users are allowed.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Return CustomerProfile objects, not User objects
        return CustomerProfile.objects.all()

class ProfileView(APIView):
    """
    API view for retrieving and updating individual profiles.
    Requires the user to be authenticated.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, user=None):
        """
        Handle GET requests to retrieve a specific profile by ID.
        """
        try:
            user_obj = CustomUser.objects.get(pk=user)
            if user_obj.type == 'business':
                profile = BusinessProfile.objects.get(user=user_obj)
                serializer = BusinessSerializer(profile)
            else:
                profile = CustomerProfile.objects.get(user=user_obj)
                serializer = CustomerSerializer(profile)
            return Response(serializer.data)
        except (BusinessProfile.DoesNotExist, CustomerProfile.DoesNotExist):
            return Response(
                {'detail': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def patch(self, request, user=None):
        """
        Handle PATCH requests to update the authenticated user's profile.
        """
        try:
            user_obj = CustomUser.objects.get(pk=user)
            if user_obj.type == 'business':
                profile = BusinessProfile.objects.get(pk=user_obj)
                serializer = BusinessProfileUpdateSerializer(profile, data=request.data, partial=True)
            else:
                profile = CustomerProfile.objects.get(pk=user_obj)
                serializer = CustomerProfileUpdateSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else: 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except(BusinessProfile.DoesNotExist, CustomerProfile.DoesNotExist):
            return Response(
                {'detail': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class BusinessProfileDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific business profile by ID.
    """
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'

class CustomerProfileDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific customer profile by ID.
    """
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'