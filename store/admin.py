from django.contrib import admin

from store.models import *

# !!!'sale_price' and 'get_discount' этих полей нет в модели, это методы из модели их тоже можно вызывать
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'price', 'sale_price', 'get_discount')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid_purchase_name', 'create_time_display')

    #Кастомное поле, которое выводит более понятную информацию о покупке
    def valid_purchase_name(self, obj):
        return f"Покупка: {obj.purchase.pk}"
    #Кастомное поле, которое выводит время в новом формате
    def create_time_display(self, obj):
        return obj.time_creation.strftime("%B %d, %Y %H:%M:%S")

# Добавил поле is_pade, в модели его нету, вычисляет оплачена ли покупка или нет
class PurchaseAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'is_pade')

    def is_pade(self, obj):
        purchase_id = getattr(obj, 'id') # obj это объект класса обращаться к атребутам только так, а не как к словрику
        transaction_id = Transaction.objects.filter(purchase__id=purchase_id)
        if transaction_id:
            return True
        else:
            return False

    is_pade.boolean = True   # Эта строчка позволяет иконки выводить
#
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Purchase, PurchaseAdmin)
#
# router = routers.DefaultRouter()
# router.register(r'product', ProductListAPIView)
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include(router.urls)),
# ]

