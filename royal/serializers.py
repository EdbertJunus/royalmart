from rest_framework import serializers
from .models import Sales

class UploadExcelSerializer(serializers.Serializer):
    class Meta:
        model = Sales
        fields = ['sales_name', 'sales_file']
