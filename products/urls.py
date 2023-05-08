from django.urls import path
from .views import (
    ProductView,
    ProductDetailView,
    ProductRetrieveIdView,
    ProductRetrieveNameView,
    ProductRetrieveCategoryView,
)

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<uuid:product_id>/", ProductDetailView.as_view()),
    path("products/<str:name>/", ProductRetrieveNameView.as_view()),
    path("products/<str:category>/", ProductRetrieveCategoryView.as_view()),
]
