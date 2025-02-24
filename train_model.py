import django
import os

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dynamic_pricing_system.settings")
django.setup()

# Import and train model
from pricing.ml_model import train_pricing_model

print("\n🚀 Running model training script...\n")
train_pricing_model(force_retrain=True)  # Force retrain and save model
print("\nTraining complete! Model saved successfully.")
