from rest_framework import generics
from .models import *
from .serializers import *

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