from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.OrderView.as_view()),
    path("order/mysales/", views.MySaleOrderView.as_view()),
    path("order/myorders/", views.MyOrdersView.as_view()),
    path("order/<uuid:order_id>/", views.OrderDetailView.as_view()),
]
