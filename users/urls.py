from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from addresses import views as address_views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/<uuid:pk>/address/", address_views.AddressView.as_view()),
    path(
        "users/<uuid:pk>/address/<uuid:pk2>/",
        address_views.AddressDetailView.as_view(),
    ),
]
