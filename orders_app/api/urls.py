from django.urls import path
from .views import OrderListView, SingleOrderView, InProgressOrderCountView, CompletedOrderCountView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='orders-list'),
    path('orders/<int:pk>/', SingleOrderView.as_view(), name='single-order'),
    path('order-count/<int:pk>/', InProgressOrderCountView.as_view(), name='in-progress-order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count')
]