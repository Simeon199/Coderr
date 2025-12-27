from django.urls import path
from .views import OffersListView, OfferCreateUpdateView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offers-list'),
    path('offers/create/', OfferCreateUpdateView.as_view(), name='offer-create')
]