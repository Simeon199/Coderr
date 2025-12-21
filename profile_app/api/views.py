from django.contrib.auth.models import User
from auth_app.api.serializers import UserProfileSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BusinessSerializer, CustomerSerializer

class BusinessListView(generics.ListCreateAPIView):
    """
    Returns a list of all users whose `type` field is set to `"business"`.
    Only authenticated callers are allowed.
    Any unhandled exception will surface a HTTP 500 (DRF default).
    """
    queryset = User.objects.all()
    serializer_class = BusinessSerializer

    def get_queryset(self):
        return User.objects.filter(type="business")
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = UserProfileSerializer(queryset, many=True)
    #     return Response(serializer.data)

class CustomerListView(generics.ListAPIView):
    """
    Returns a list of *customer* profiles belonging to the authenticated user.

    - Only authenticated users can access it.
    - In case any unexpected exception occurs while fetching data,
      the view catches it and returns HTTP 500 with a generic error message.
    """
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        return User.objects.filter(type="customer")
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = UserProfileSerializer(queryset, many=True)
    #     return Response(serializer.data)
        
class ProfileView(APIView):
    """
    API view for retrieving and updating individual profiles.
    Requires the user to be authenticated
    """

    def get(self, request):
        """
        Handle GET requests to check for a profile by pk.
        
        Query Parameters:
            pk (int): The private key to search for.

        Returns:
            Response: Profile details if found, or an error message.
        """
        pk = request.query_params.get('pk')
        if not pk:
            return Response({'detail': 'Private '})