from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from orders.models import Order
from orders.permissions import IsOrderSaler, IsSaler
from orders.serializers import OrderSerializer


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
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(costumer=self.request.user)


class MySaleOrderView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(saler=self.request.user)


class MyOrdersView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(costumer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOrderSaler]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = ["order_id"]

    def get_object(self):
        return Order.objects.get(id=self.kwargs["order_id"])
