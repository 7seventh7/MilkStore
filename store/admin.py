from django.contrib import admin

from store.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'price', 'sale_price', 'get_discount')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid_purchase_name', 'create_time_display')

    def valid_purchase_name(self, obj):
        return f"Покупка: {obj.purchase.pk}"

    def create_time_display(self, obj):
        return obj.time_creation.strftime("%B %d, %Y %H:%M:%S")

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
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

