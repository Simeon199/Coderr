from rest_framework import generics # For the moment probably not the right choice
from django.contrib.auth.models import User

class CustomerListView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def list(self, request):
        queryset = self.get_queryset()

class BusinessListView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def list(self, request):
        queryset = self.get_queryset()