from rest_framework import serializers
from .models import Product, SalesData, DemandIndicator, CompetitorPricing

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'

class DemandIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandIndicator
        fields = '__all__'

class CompetitorPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorPricing
        fields = '__all__'
