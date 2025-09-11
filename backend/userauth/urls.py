from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from .views import PaymentMethodView

router = DefaultRouter()

urlpatterns = [
    # JWT
    path('jwt/create/', TokenObtainPairView.as_view(), name='token-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),  # JWT Auth
    
    path("payment-method/", PaymentMethodView.as_view(), name="payment-method"),
]
