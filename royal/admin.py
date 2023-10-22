from django.contrib import admin
from .models import ExtendUser, Sales, SalesDetail, Stock

# Register your models here.
admin.site.register([ExtendUser, Sales, SalesDetail, Stock])