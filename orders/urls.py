from django.urls import path
from .views import OrderCreateView, OrderStatusUpdateView

urlpatterns = [
    path('api/orders/', OrderCreateView.as_view(), name='order_create'),
    path('api/orders/<int:id>/', OrderStatusUpdateView.as_view(), name='order_update'),
]
