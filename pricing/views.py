from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, SalesData, DemandIndicator, CompetitorPricing
from .serializers import ProductSerializer, SalesDataSerializer, DemandIndicatorSerializer, CompetitorPricingSerializer
from .ml_model import suggest_price

# CRUD for Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# CRUD for Sales Data
class SalesDataListCreateView(generics.ListCreateAPIView):
    queryset = SalesData.objects.all()
    serializer_class = SalesDataSerializer

class SalesDataRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalesData.objects.all()
    serializer_class = SalesDataSerializer

# CRUD for Demand Indicators
class DemandIndicatorListCreateView(generics.ListCreateAPIView):
    queryset = DemandIndicator.objects.all()
    serializer_class = DemandIndicatorSerializer

class DemandIndicatorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DemandIndicator.objects.all()
    serializer_class = DemandIndicatorSerializer

# CRUD for Competitor Pricing
class CompetitorPricingListCreateView(generics.ListCreateAPIView):
    queryset = CompetitorPricing.objects.all()
    serializer_class = CompetitorPricingSerializer

class CompetitorPricingRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompetitorPricing.objects.all()
    serializer_class = CompetitorPricingSerializer

class PriceSuggestionView(APIView):
    """API endpoint to get an optimal price for a product."""
    def get(self, request, product_id):
        try:
            suggested_price = suggest_price(product_id)
            return Response({"product_id": product_id, "suggested_price": suggested_price})
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

# ✅ NEW: API to get historical prices of a product
class ProductPriceHistoryView(APIView):
    """API endpoint to fetch past price trends for a product."""
    def get(self, request, product_id):
        sales_data = SalesData.objects.filter(product_id=product_id).order_by("date")

        if not sales_data.exists():
            return Response({"error": "No sales data found for this product"}, status=404)

        history = [{"date": sale.date.strftime("%Y-%m-%d"), "price": sale.price} for sale in sales_data]
        return Response(history)
