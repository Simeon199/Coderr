from offers_app.models import Offer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import OfferSerializer

class OffersListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = PageNumberPagination