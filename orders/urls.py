from django.urls import path
from .views import order_form_view, orders_list_view, master_orders_view
from .views import OrderCreateView, OrderStatusUpdateView

urlpatterns = [
    # API
    path('api/orders/', OrderCreateView.as_view(), name='order_create'),
    path('api/orders/<int:id>/', OrderStatusUpdateView.as_view(), name='order_update'),

    # Frontend
    path('order-form/', order_form_view, name='order_form'),
    path('orders/', orders_list_view, name='orders_list'),
    path('master/orders/', master_orders_view, name='master_orders'),
]
