from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsProductOwner, IsSalerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSalerOrReadOnly]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(saler=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsProductOwner]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductRetrieveNameView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = ["name"]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        name = self.kwargs["name"]
        queryset = Product.objects.filter(name__icontains=name)
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)


class ProductRetrieveCategoryView(generics.RetrieveAPIView):
    lookup_url_kwarg = ["category"]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        category = self.kwargs["category"]
        queryset = Product.objects.filter(category__iexact=category)
        serializer = ProductSerializer(queryset, many=True)

        return Response(serializer.data)
