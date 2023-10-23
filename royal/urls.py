from django.urls import path
from royal.views import SalesView, RegisterView, StockView, MasterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('sales', SalesView.as_view(), name='sales'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='login_refresh'),
    path('stock', StockView.as_view(), name='stock'),
    path('master', MasterView.as_view(), name='master')
]
