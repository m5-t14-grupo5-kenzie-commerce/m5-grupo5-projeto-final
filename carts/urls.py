from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view()),
    path("cart/<uuid:product_id>/", views.CartDetailView.as_view()),
]
