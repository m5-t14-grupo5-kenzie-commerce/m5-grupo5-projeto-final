from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order
from orders.permissions import IsOrderSaler, IsSaler
from orders.serializers import OrderSerializer
from django.core.mail import send_mail
from django.conf import settings

from users.models import User


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSaler]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(
            saler=request.user,
            status="Pedido realizado",
        )

        result_page = self.paginate_queryset(queryset)
        serializer = OrderSerializer(result_page, many=True)
        paginated_data = self.get_paginated_response(serializer.data)
        return paginated_data

    def perform_create(self, serializer):
        serializer.save(costumer=self.request.user)


class MySaleOrderView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSaler]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(saler=self.request.user)


class MyOrdersView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(costumer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOrderSaler]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "order_id"

    def perform_update(self, serializer):
        serializer.save()
        user = get_object_or_404(User, pk=serializer.data["costumer"]["id"])
        seller = get_object_or_404(User, pk=serializer.data["saler"]["id"])

        send_mail(
            subject=f"Order {serializer.data['id']} Update",
            message=f"Dear {user.last_name}, We wanted to let you know that the status of your order {serializer.data['id']} has been updated. The new status is {serializer.data['status']}. If you have any questions or concerns about your order, please dont hesitate to contact us. Thank you for choosing us. {seller.email}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def get_object(self):
        order = Order.objects.get(id=self.kwargs["order_id"])
        self.check_object_permissions(self.request, order)
        return order
