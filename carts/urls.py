from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view()),
    path("cart/<int:product_id>/", views.CartProductDetailView.as_view()),
]

# Na primeira rota, apenas para criar produtos dentro da CartProduct (adicionar ao carrinho)
# Na segunda rota, editar quantidade, excluir produto da CartProduct
