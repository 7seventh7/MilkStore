from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=120, null=True)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "20%"

class Purchase(models.Model):
    product_list = models.ManyToManyField(Product, related_name='product_list')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

class Transaction(models.Model):
    time_creation = models.DateTimeField(auto_now_add=True)
    purchase = models.OneToOneField(Purchase, related_name='transaction', on_delete=models.PROTECT)
