from rest_framework import serializers
from .models import *
from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')

class PurchasePrefetchSerializer(serializers.ModelSerializer):

    total_cost = serializers.IntegerField()
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'product_list', 'total_cost')

class PurchasePrefetchSerializer2(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) # Прячем поле юзера. Юзер выбирается автоматически
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'product_list')


class PurchaseSerializer(serializers.ModelSerializer):
    # Получаем список всех товаров входящич в покупку. пример работы с Many to many !!!!! Обязательно source!!!
    # Проверяй related name в модели
    # Пример вложенного сериализатора!!!
    products = ProductSerializer(many=True, source='product_list')

    # Обращаемся к модели Юзер через ForeinKey. Чтобы имена были вместо цифр

    user = serializers.CharField(source='user.username')
    total_cost = serializers.IntegerField() #т.к названия здесь и во viev. совпадают, то можно не писать source

    is_paid = serializers.SerializerMethodField(read_only=True)
    #total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'user', 'products', 'total_cost', 'is_paid')


    # !!!!! Функция которая вичисляет оплачена покупка или нет !!!!
    # Берём id покупки и если её нету в транзакциях, то покупка ещё не оплачена
    def get_is_paid(self, data):
        purchase_id = getattr(data, 'id')   # данные приходят в виде: data {'_state': <django.db.models.base.ModelState object at 0x7f4184992c10>, 'id': 1, 'user_id': 2}
        transaction_id = Transaction.objects.filter(purchase__id=purchase_id)
        if transaction_id:
            return True
        else:
            return False



class TransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='purchase.user')   # Берем данные из связанных таблиц
    email = serializers.CharField(source='purchase.user.email')
    product = PurchaseSerializer(many=True, read_only=True, source='product_list')

    class Meta:
        model = Transaction
        fields = ('user_name', 'email', 'time_creation', 'product')


class UserSerializer(serializers.ModelSerializer):
    # Дополнительне поле для вывода даты последней покупки пользователя
    last_purches = serializers.SerializerMethodField(read_only=True)

    def get_last_purches(self, data):  # data приходит из views.py
        username = getattr(data, 'id')
        last_purches = Transaction.objects.filter(purchase__user=username).last()
        return last_purches.time_creation

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'date_joined', 'last_purches')


class ProductSerializer2(serializers.Serializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    """Если мы используем класс Serializer то нужно описывать ему как выглядят нужные поля в модели, какие данные ему нужно проверять,
    Если искользуем класс ModelSerializer, то нужно прописать класс Meta"""
    title = serializers.CharField()
    content = serializers.CharField()
    price = serializers.IntegerField()

    # class Meta:
    #     model = Product
    #     fields = [
    #         'title',
    #         'content',
    #         'price',
    #         'sale_price',
    #         'my_discount'
    #     ]
    def create(self, validated_data):

        print('validated_data=', validated_data) #validated_data = {'title': 1, 'content': 'FFFFFFF', 'price': '550'}
        return Product.objects.create(**validated_data)

    """Ещё можно метод update определять в сериализаторе"""
    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title) #validated_data = {'title': 1, 'content': 'FFFFFFF', 'price': '550'}
        instance.content = validated_data.get('content', instance.content)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
