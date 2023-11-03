from rest_framework import serializers
from .models import ExtendUser, Sales, Stock

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtendUser
        fields = '__all__'
    
    def create(self, validated_data):
        user = ExtendUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class StockUploadSerializer(serializers.Serializer):
    stockFile = serializers.FileField(required=True)

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class MasterSerializer(serializers.Serializer):
    periode = serializers.CharField(required=True, max_length=255)
