from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=120, null=True, help_text="Введите название продукта")
    content = models.TextField(blank=True, null=True, help_text="Введите описание продукта")
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99, help_text="Введите цену продукта")

    class Meta:
        verbose_name = ('Продукт')
        verbose_name_plural = ('Продукты')
    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "20%"

class Purchase(models.Model):
    product_list = models.ManyToManyField(Product, related_name='product_list')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')


    class Meta:
        verbose_name = ('Покупка')
        verbose_name_plural = ('Покупки')

    def get_product_list(self):
        return self.product_list


class Transaction(models.Model):
    time_creation = models.DateTimeField(auto_now_add=True)
    purchase = models.OneToOneField(Purchase, related_name='transaction', on_delete=models.PROTECT, verbose_name='Покупка')
    class Meta:
        verbose_name = ('Чек')
        verbose_name_plural = ('Чеки')

    def __str__(self):
        return f'Покупка: {self.pk}'

