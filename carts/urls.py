from django.urls import path
from . import views

urlpatterns = [path("cart/<int:pk>/", views.CartView.as_view())]
urlpatterns = [path("cart/<int:pk>/<int:product_id>", views.CartDetailView.as_view())]

# Na primeira rota, apenas para criar produtos dentro da CartProduct (adicionar ao carrinho)
# Na segunda rota, editar quantidade, excluir produto da CartProduct
