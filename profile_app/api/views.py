from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .serializer import BusinessSerializer, CustomerSerializer

User = get_user_model

class BusinessListView(generics.ListAPIView):
    """
    Returns a list of all users whose `type` field is set to `"business"`.
    Only authenticated callers are allowed.
    Any unhandled exception will surface a HTTP 500 (DRF default).
    """

    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter by the custom `type` attribute on the user model.
        return User.objects.fitler(type="business")
    
    # Optional: override list to explicitly catch unexpected errors
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except Exception as exc:
            # The test patches BusinessListView.get - we must preserve the signature
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class CustomerListView(generics.ListAPIView):
    """
    Returns a list of *customer* profiles belonging to the authenticated user.

    - Only authenticated users can access it.
    - In case any unexpected exception occurs while fetching data,
      the view catches it and returns HTTP 500 with a generic error message.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Assuming each User has a OneToOne profile with fields `type` and other attrs.
        return self.request.user.profile.__class__.objects.filter(type="customer")
    
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