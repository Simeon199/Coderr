"""
URL patterns for the profile app API.
This module defines the endpoints for user profiles.
"""

from django.urls import path
from .views import BusinessListView, CustomerListView

urlpatterns = [
    path('profiles/business/', BusinessListView.as_view(), name="business-profile"),
    path('profiles/customer/', CustomerListView.as_view(), name="customer-profile")
]