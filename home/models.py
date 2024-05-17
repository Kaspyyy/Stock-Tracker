from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, max_length=255)
    logo = models.ImageField(upload_to='stock_icons/')
    last_price = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.name} ({self.symbol})"
