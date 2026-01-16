from django.db.models import Count, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from reviews_app.models import Review
from offers_app.models import Offer
from profile_app.models import BusinessProfile

class BaseInfoView(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        business_profile_count = BusinessProfile.objects.count()
        offer_count = Offer.objects.count()

        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        }

        return Response(data)