from django.urls import path
from .views import OffersListView, SingleOfferView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offers-list'),
    path('offers/<int:pk>/', SingleOfferView.as_view(), name='single-offer')
]