from django.urls import path
from .views import (
    ProductListCreateView, ProductRetrieveUpdateDeleteView,
    SalesDataListCreateView, SalesDataRetrieveUpdateDeleteView,
    DemandIndicatorListCreateView, DemandIndicatorRetrieveUpdateDeleteView,
    CompetitorPricingListCreateView, CompetitorPricingRetrieveUpdateDeleteView,
    PriceSuggestionView, ProductPriceHistoryView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail'),

    path('sales/', SalesDataListCreateView.as_view(), name='sales-list-create'),
    path('sales/<int:pk>/', SalesDataRetrieveUpdateDeleteView.as_view(), name='sales-detail'),

    path('demand/', DemandIndicatorListCreateView.as_view(), name='demand-list-create'),
    path('demand/<int:pk>/', DemandIndicatorRetrieveUpdateDeleteView.as_view(), name='demand-detail'),

    path('competitor-pricing/', CompetitorPricingListCreateView.as_view(), name='competitor-list-create'),
    path('competitor-pricing/<int:pk>/', CompetitorPricingRetrieveUpdateDeleteView.as_view(), name='competitor-detail'),

    path("suggest-price/<int:product_id>/", PriceSuggestionView.as_view(), name="price-suggestion"),
    
    # ✅ NEW: Endpoint to fetch price history for a product
    path("price-history/<int:product_id>/", ProductPriceHistoryView.as_view(), name="price-history"),
]
