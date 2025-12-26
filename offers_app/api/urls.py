from django.urls import path
from .views import OffersListView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offers-list')
]