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
    BusinessProfileDetailSerializer,
    CustomerProfileUpdateSerializer,
    CustomerProfileDetailSerializer
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
        """Return all business profiles."""
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
        """Return all customer profiles."""
        return CustomerProfile.objects.all()


class ProfileView(APIView):
    """
    API view for retrieving and updating individual profiles.
    Dispatches to the correct profile type (business or customer)
    based on the user's type field.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def _get_profile(self, user_obj):
        """
        Retrieve the profile instance for the given user.
        Returns a BusinessProfile or CustomerProfile based on user type.
        """
        
        if user_obj.type == 'business':
            return get_object_or_404(BusinessProfile, user=user_obj)
        return get_object_or_404(CustomerProfile, user=user_obj)

    def _get_detail_serializer(self, user_obj, profile):
        """
        Return the appropriate detail serializer for the given profile.
        """

        if user_obj.type == 'business':
            return BusinessProfileDetailSerializer(profile)
        return CustomerProfileDetailSerializer(profile)

    def _get_update_serializer(self, user_obj, profile, data):
        """
        Return the appropriate update serializer for the given profile.
        """

        if user_obj.type == 'business':
            return BusinessProfileUpdateSerializer(profile, data=data, partial=True)
        return CustomerProfileUpdateSerializer(profile, data=data, partial=True)

    def get(self, request, user=None):
        """
        Retrieve a specific profile by user ID.
        """

        user_obj = get_object_or_404(CustomUser, pk=user)
        profile = self._get_profile(user_obj)
        serializer = self._get_detail_serializer(user_obj, profile)
        return Response(serializer.data)

    def patch(self, request, user=None):
        """
        Update the profile for the given user ID.
        Only the profile owner is allowed to update.
        """

        user_obj = get_object_or_404(CustomUser, pk=user)
        if request.user.id != user_obj.id:
            return Response({'detail': 'You do not have permission to update this profile.'}, status=status.HTTP_403_FORBIDDEN)
        profile = self._get_profile(user_obj)
        serializer = self._get_update_serializer(user_obj, profile, request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        detail_serializer = self._get_detail_serializer(user_obj, profile)
        return Response(detail_serializer.data)


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