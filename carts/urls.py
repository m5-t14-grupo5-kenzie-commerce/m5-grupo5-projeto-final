from django.urls import path
from . import views

urlpatterns = [
    path("cart/<uuid:cart_id>/", views.CartView.as_view()),
    path("cart/<uuid:cart_id>/<uuid:product_id>", views.CartDetailView.as_view()),
]

# Na primeira rota, apenas para criar produtos dentro da CartProduct (adicionar ao carrinho)
# Na segunda rota, editar quantidade, excluir produto da CartProduct
