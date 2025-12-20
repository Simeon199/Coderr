from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BusinessSerializer, CustomerSerializer


class BusinessListView(generics.ListAPIView):
    """
    Returns a list of all users whose `type` field is set to `"business"`.
    Only authenticated callers are allowed.
    Any unhandled exception will surface a HTTP 500 (DRF default).
    """

    serializer_class = BusinessSerializer

    def get_queryset(self):
        user = self.request.user
        return user
    
    # def list(self, request, *args, **kwargs):
    #     try:
    #         queryset = self.get_queryset()
    #         serializer = self.serializer_class(queryset, many=True)
    #         return Response(serializer.data)
    #     except Exception as exc:
    #         return Response(
    #             {"detail": "Internal server error"},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

class CustomerListView(generics.ListAPIView):
    """
    Returns a list of *customer* profiles belonging to the authenticated user.

    - Only authenticated users can access it.
    - In case any unexpected exception occurs while fetching data,
      the view catches it and returns HTTP 500 with a generic error message.
    """
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.request.user.profile.__class__.objects.filter(type="customer-profile")
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
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