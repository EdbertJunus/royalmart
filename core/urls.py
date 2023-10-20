
from django.contrib import admin
from django.urls import path
from royal.views import SalesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sales/', SalesView.as_view(), name='sales'),
]
