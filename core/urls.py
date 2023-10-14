
from django.contrib import admin
from django.urls import path
from royal.views import UploadExcelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload-excel/', UploadExcelView.as_view(), name='upload'),
]
