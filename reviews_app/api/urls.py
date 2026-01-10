from django.urls import path
from .views import ReviewListView, SingleReviewView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', SingleReviewView.as_view(), name="single-review")
]