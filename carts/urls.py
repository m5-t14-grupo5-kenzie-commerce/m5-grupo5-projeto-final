from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view()),
    path(
        "cart/<uuid:cart_id>/<int:product_id>/", views.CartProductDetailView.as_view()
    ),
]
