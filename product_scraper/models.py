from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scraping_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Brand {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    asin = models.CharField(max_length=255, null=False)
    sku = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product {self.name}"