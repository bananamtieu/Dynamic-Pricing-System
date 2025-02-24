from django.contrib import admin

# Register your models here.
from .models import Product, SalesData, DemandIndicator, CompetitorPricing

admin.site.register(Product)
admin.site.register(SalesData)
admin.site.register(DemandIndicator)
admin.site.register(CompetitorPricing)