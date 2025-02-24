import os
import django
import random
import numpy as np
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dynamic_pricing_system.settings")
django.setup()

from pricing.models import Product, SalesData, DemandIndicator, CompetitorPricing

# ✅ Product List (10 Products with Varying Categories)
product_list = [
    {"name": "Bluetooth Speaker", "category": "Electronics", "min_price": 50, "max_price": 150, "cost_price": 40},
    {"name": "Wireless Headphones", "category": "Electronics", "min_price": 80, "max_price": 200, "cost_price": 60},
    {"name": "Gaming Mouse", "category": "Accessories", "min_price": 30, "max_price": 120, "cost_price": 20},
    {"name": "Smartphone Stand", "category": "Accessories", "min_price": 15, "max_price": 50, "cost_price": 10},
    {"name": "Portable Charger", "category": "Gadgets", "min_price": 40, "max_price": 100, "cost_price": 25},
    {"name": "Mechanical Keyboard", "category": "Electronics", "min_price": 70, "max_price": 250, "cost_price": 50},
    {"name": "Smart Watch", "category": "Wearables", "min_price": 90, "max_price": 300, "cost_price": 70},
    {"name": "Wireless Earbuds", "category": "Electronics", "min_price": 50, "max_price": 180, "cost_price": 40},
    {"name": "Laptop Stand", "category": "Accessories", "min_price": 25, "max_price": 80, "cost_price": 20},
    {"name": "External Hard Drive", "category": "Storage", "min_price": 60, "max_price": 200, "cost_price": 50},
]

# ✅ Simulation Parameters
num_days = 30  # Each product gets 30 days of data
start_date = datetime(2024, 1, 1)

price_elasticity = -0.5  # Sales drop by 0.5% per 1% price increase
competitor_impact = 1.2  # Competitor effect factor

# ✅ Market Trend Parameters
demand_boost_weekend = 1.10  # +10% demand on weekends
discount_days = set(random.sample(range(num_days), 3))  # Random discount days
event_spikes = set(random.sample(range(num_days), 2))  # Sudden demand surges
supply_issues = set(random.sample(range(num_days), 2))  # Random supply drops

# ✅ Insert Data for Each Product
for product_info in product_list:
    product, _ = Product.objects.get_or_create(
        name=product_info["name"],
        defaults={
            "category": product_info["category"],
            "min_price": product_info["min_price"],
            "max_price": product_info["max_price"],
            "cost_price": product_info["cost_price"]
        }
    )

    base_price = random.uniform(product_info["min_price"], product_info["max_price"])  # Different base prices
    base_sales = random.randint(50, 100)  # Base sales per day

    prev_price = base_price
    prev_units_sold = base_sales

    for i in range(num_days):
        date = start_date + timedelta(days=i)
        weekday = date.weekday()
        
        # ✅ Simulate competitor pricing
        competitor_price = base_price + random.uniform(-5, 5)
        if i in discount_days:
            competitor_price *= 0.95  # Simulate competitor discount (-5%)

        # ✅ Calculate price adjustment based on demand
        price_change_factor = (prev_units_sold - base_sales) / base_sales * 0.02
        price_today = prev_price * (1 + price_change_factor)

        # ✅ Competitor impact on sales
        competitor_effect = (competitor_price - price_today) / price_today

        # ✅ Base sales calculation
        units_sold_today = base_sales * (1 + price_elasticity * price_change_factor + competitor_impact * competitor_effect)

        # ✅ Weekend Boost
        if weekday >= 5:  # Saturday, Sunday
            units_sold_today *= demand_boost_weekend

        # ✅ Demand Surges (Events)
        if i in event_spikes:
            units_sold_today *= 1.25  # +25% spike

        # ✅ Supply Chain Issues
        if i in supply_issues:
            units_sold_today *= 0.75  # -25% supply restriction

        # ✅ Temporary Discount Days
        if i in discount_days:
            price_today *= 0.97  # Reduce price by 3%

        # ✅ Add randomness
        units_sold_today += random.randint(-5, 5)
        units_sold_today = max(20, round(units_sold_today))

        # ✅ Insert Sales Data
        SalesData.objects.create(
            product=product,
            date=date,
            units_sold=units_sold_today,
            price=price_today
        )

        # ✅ Insert Demand Indicators
        views = random.randint(400, 600)
        add_to_cart = int(units_sold_today * random.uniform(0.5, 1.5))
        conversion_rate = add_to_cart / views

        DemandIndicator.objects.create(
            product=product,
            date=date,
            views=views,
            add_to_cart=add_to_cart,
            conversion_rate=round(conversion_rate, 2)
        )

        # ✅ Insert Competitor Pricing
        CompetitorPricing.objects.create(
            product=product,
            date=date,
            competitor_price=competitor_price,
            discount=0,
            promotion="None"
        )

        # ✅ Update previous values
        prev_price = price_today
        prev_units_sold = units_sold_today

print("✅ Successfully Inserted Data for 10 Products Over 30 Days!")
