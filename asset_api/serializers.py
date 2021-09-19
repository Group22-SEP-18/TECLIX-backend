from rest_framework import serializers
from .models import Product


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SOProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['price']
