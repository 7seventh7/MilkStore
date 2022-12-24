from django.contrib import admin

from store.models import *

admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Purchase)