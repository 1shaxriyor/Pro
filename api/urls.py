from django.urls import path
from .views import OrderListCreateView, OrderUpdateView
app_name = "orders"
urlpatterns = [
    path('api/orders/', OrderListCreateView.as_view(), name='order_list_create'),
    path('api/orders/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
]
