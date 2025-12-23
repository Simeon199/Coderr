"""
URL patterns for the profile app API.
This module defines the endpoints for user profiles.
"""

from django.urls import path
from .views import BusinessListView, CustomerListView, ProfileView

urlpatterns = [
    path('profiles/business/', BusinessListView.as_view(), name="business-profile"),
    path('profiles/customer/', CustomerListView.as_view(), name="customer-profile"),
    path('profile/<int:pk>/', ProfileView.as_view(), name="user-profile")
]