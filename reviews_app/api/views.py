from reviews_app.models import Review
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializer import ReviewListSerializer, SingleReviewSerializer
from .permissions import IsUserCustomer, IsUserCreator

class ReviewListView(generics.ListCreateAPIView):
    permission_classes = [IsUserCustomer]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SingleReviewSerializer
        return ReviewListSerializer

    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get('business_user')
        if business_user_id is not None:
            queryset = queryset.filter(business_user=business_user_id)

        reviewer_id = self.request.query_params.get('reviewer_user')
        if reviewer_id is not None:
            queryset = queryset.filter(reviewer=reviewer_id)

        ordering = self.request.query_params.get('ordering')
        if ordering is not None:
            queryset = queryset.order_by(ordering)

        return queryset
    
class SingleReviewView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Review.objects.all()
    serializer_class = SingleReviewSerializer
    permission_classes = [IsAuthenticated, IsUserCustomer, IsUserCreator]