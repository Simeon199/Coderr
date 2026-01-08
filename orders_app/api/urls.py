from django.urls import path
from .views import OrderListView, SingleOrderView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', SingleOrderView.as_view(), name='single-order')
]