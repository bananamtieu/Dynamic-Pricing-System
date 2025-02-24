from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    min_price = models.FloatField()
    max_price = models.FloatField()
    cost_price = models.FloatField()

    def __str__(self):
        return self.name

class SalesData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField()
    units_sold = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.units_sold} units on {self.date.date()}"

class DemandIndicator(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField()
    views = models.IntegerField()
    add_to_cart = models.IntegerField()
    conversion_rate = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.conversion_rate*100}% conversion on {self.date.date()}"

class CompetitorPricing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField()
    competitor_price = models.FloatField()
    discount = models.FloatField()
    promotion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - Competitor price: ${self.competitor_price} on {self.date.date()}"
