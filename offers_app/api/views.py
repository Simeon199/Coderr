from offers_app.models import Offer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import OfferCreateSerializer, OfferListSerializer
from .permissions import IsBusinessUser

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class OffersListView(generics.ListCreateAPIView):
    permission_classes = [IsBusinessUser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def get_queryset(self):
        queryset = Offer.objects.all()
        
        # Filter by creator_id
        creator_id = self.request.query_params.get('creator_id')
        if creator_id is not None:
            queryset = queryset.filter(user_id=creator_id)

        # Filter by min_price
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        # Filter by max_delivery_time
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)

        # Apply search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)

        # Apply ordering
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)