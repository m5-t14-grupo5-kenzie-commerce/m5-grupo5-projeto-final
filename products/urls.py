from django.urls import path

from .views import (
    ProductView,
    ProductDetailView,
    ProductRetrieveNameView,
    ProductRetrieveCategoryView,
)

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<uuid:pk>/", ProductDetailView.as_view()),
    path("products/name/<str:name>/", ProductRetrieveNameView.as_view()),
    path("products/category/<str:category>/", ProductRetrieveCategoryView.as_view()),
]
