from rest_framework import serializers
from .models import Sales

class UploadExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
