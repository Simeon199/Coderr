from offers_app.models import Offer, OfferDetail
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import OfferCreateSerializer, OfferListSerializer, SingleOfferSerializer, SingleOfferUpdateSerializer, SingleOfferDeleteSerializer, SingleOfferDetailSerializer
from .permissions import IsBusinessUser, SingleOfferPermission, SingleOfferDetailPermission


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination with a default page size of 6.
    Allows clients to override page size via the 'page_size' query parameter.
    """

    page_size = 6
    page_size_query_param = 'page_size'


class OffersListView(generics.ListCreateAPIView):
    """
    API view for listing offers with filtering, search and ordering,
    and for creating new offers.
    """

    permission_classes = [IsBusinessUser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        """Return OfferCreateSerializer for POST requests, OfferListSerializer otherwise."""
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def _apply_filters(self, queryset):
        """
        Apply query parameter filters for creator, min price and max delivery time.
        """
        creator_id = self.request.query_params.get('creator_id')
        if creator_id is not None and creator_id.strip():
            queryset = queryset.filter(user_id=creator_id)
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)
        return queryset

    def _apply_search(self, queryset):
        """
        Apply search filter on title and description fields.
        """
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)
        return queryset

    def get_queryset(self):
        """
        Return filtered, searched and ordered offer queryset based on query parameters.
        """
        queryset = Offer.objects.all()
        queryset = self._apply_filters(queryset)
        queryset = self._apply_search(queryset)
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def perform_create(self, serializer):
        """Save the new offer with the authenticated user as the creator."""
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)


class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting a single offer.
    Serializer is selected based on the HTTP method.
    """

    queryset = Offer.objects.all()
    permission_classes = [SingleOfferPermission]

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the HTTP method.
        """
        if self.request.method == 'GET':
            return SingleOfferSerializer
        elif self.request.method == 'PATCH':
            return SingleOfferUpdateSerializer
        elif self.request.method == 'DELETE':
            return SingleOfferDeleteSerializer

    def update(self, request, *args, **kwargs):
        """
        Update an offer and return the updated data using the same serializer.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SingleOfferDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single offer detail entry.
    """

    queryset = OfferDetail.objects.all()
    serializer_class = SingleOfferDetailSerializer
    permission_classes = [SingleOfferDetailPermission]
