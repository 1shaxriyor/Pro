from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from orders.models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        action = request.query_params.get('action')

        if order.master != request.user:
            return Response({"detail": "Siz bu orderni boshqarolmaysiz."}, status=status.HTTP_403_FORBIDDEN)

        if action == "accept":
            order.status = "accepted"
        elif action == "reject":
            order.status = "rejected"
        else:
            return Response({"detail": "Noto‘g‘ri action."}, status=status.HTTP_400_BAD_REQUEST)

        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
