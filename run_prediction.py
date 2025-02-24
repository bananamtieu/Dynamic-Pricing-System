import django
import os

# ✅ Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dynamic_pricing_system.settings")
django.setup()

# ✅ Import and run the price prediction
from pricing.ml_model import suggest_price

for i in range(1, 11):
    print(f"\n🚀 Running Price Prediction for Product ID {i}...\n")
    print(suggest_price(i))  # Expecting a new price
    print("--------------------------------------------------")
