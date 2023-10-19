from django.contrib import admin
from .models import ExtendUser, Sales, SalesDetail

# Register your models here.
admin.site.register([ExtendUser, Sales, SalesDetail])