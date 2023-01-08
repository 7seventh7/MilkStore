from django.db.models import F, Sum
from rest_framework import generics
from .models import *
from .serializers import *

class PurchasisAPIViev(generics.ListAPIView):

    #Добавлеем ещё одно поле (общая стоимость покупки) Вычисляем на стороне БД.
    queryset = Purchase.objects.all().annotate(
        total_cost = Sum('product_list__price')
    )
    serializer_class = PurchaseSerializer

class PurchasisPrefetchAPIViev(generics.ListAPIView):
    queryset = Purchase.objects.all().annotate(
        total_cost = Sum('product_list__price')
    )
    serializer_class = PurchasePrefetchSerializer


class UsersTransactionAPIViev(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer



class UsersListAPIView(generics.ListAPIView):
    """Получаем список всех Пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ProductListCreateAPIView(generics.ListCreateAPIView):
    """Получаем списко всех продуктов в магазине и добавляем новый продукт"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print('serializer=', serializer)
        print('serializer.vdata=', serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')

        if content is '':
            content = title
        serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'

product_list_view = ProductListAPIView.as_view()