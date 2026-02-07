from reviews_app.models import Review
from profile_app.models import CustomerProfile, BusinessProfile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from .serializer import ReviewListSerializer, SingleReviewSerializer
from .permissions import IsUserWarranted, IsUserCreator, IsValidRating


class ReviewListView(generics.ListCreateAPIView):
    """
    API view for listing and creating reviews.
    Supports filtering by business_user, reviewer_user and custom ordering
    via query parameters. Creating a review requires a valid customer profile
    and prevents duplicate reviews for the same business.
    """

    permission_classes = [IsUserWarranted, IsValidRating]

    def get_serializer_class(self):
        """
        Return SingleReviewSerializer for POST requests, ReviewListSerializer otherwise.
        """
        if self.request.method == 'POST':
            return SingleReviewSerializer
        return ReviewListSerializer

    def get_queryset(self):
        """
        Return filtered and ordered review queryset based on query parameters.
        Supported query parameters:
            business_user: Filter reviews by business user ID.
            reviewer_user: Filter reviews by reviewer ID.
            ordering: Field name to order results by.
        """
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

    def _get_customer_profile(self):
        """
        Retrieve the customer profile for the authenticated user.
        Raises:
            ValidationError: If the user has no associated customer profile.
        """
        try:
            return CustomerProfile.objects.get(user=self.request.user)
        except CustomerProfile.DoesNotExist:
            raise ValidationError("The user does not have an associated customer profile.")

    def _get_business_profile(self):
        """
        Retrieve the business profile from the request data.
        Raises:
            ValidationError: If business_user is missing or does not exist.
        """
        business_user_id = self.request.data.get('business_user')
        if not business_user_id:
            raise ValidationError("business_user field is required.")
        try:
            return BusinessProfile.objects.get(user=business_user_id)
        except BusinessProfile.DoesNotExist:
            raise ValidationError("The specified business_user does not exist.")

    def perform_create(self, serializer):
        """
        Create a new review after validating profiles and checking for duplicates.
        Raises:
            ValidationError: If profiles are invalid or a duplicate review exists.
        """
        customer_profile = self._get_customer_profile()
        business_profile = self._get_business_profile()
        if Review.objects.filter(reviewer=customer_profile, business_user=business_profile).exists():
            raise ValidationError("You have already reviewed this business.")
        serializer.save(reviewer=customer_profile, business_user=business_profile)


class SingleReviewView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and deleting a single review.
    Only authenticated users who are the creator of the review can
    modify or delete it.
    """

    queryset = Review.objects.all()
    serializer_class = SingleReviewSerializer
    permission_classes = [IsAuthenticated, IsUserWarranted, IsUserCreator, IsValidRating]
