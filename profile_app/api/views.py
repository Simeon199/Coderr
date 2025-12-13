from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .serializer import BusinessSerializer

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
    pass