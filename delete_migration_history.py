import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dynamic_pricing_system.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app = 'pricing';")

print("✅ Deleted migration history for 'pricing' app.")