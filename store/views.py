from django.db.models import Sum
from rest_framework import generics, status, viewsets, mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import *


class AllUsersGetListAPIView(viewsets.ReadOnlyModelViewSet):
    """Get liest of products. All users could make GET-requests."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AuthUsersAddDeleteUpdateProductsAPIView( mixins.CreateModelMixin,
                                               mixins.UpdateModelMixin,
                                               mixins.DestroyModelMixin,
                                               GenericViewSet):
    """Only Admin can Create, Update, Destroy Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)

class AdminGetAllUsersPurchasis(viewsets.ModelViewSet):
    """Only Admin can get all Purchases of all Users"""
    queryset = Purchase.objects.all().annotate(
        total_cost=Sum('product_list__price')
    )
    serializer_class = PurchaseSerializer
    permission_classes = (IsAdminUser,)


class TrainingToUseAPIView(APIView):
    """методы get, post и др. автоматически отрабатывают они уже определены в классе"""

    def get(self, request):
        """request.__dict__ = {'_request': <WSGIRequest: GET '/apiview'>, 'parsers': [<rest_framework.parsers.JSONParser object at 0x7fc8f140ec10>, <rest_framework.parsers.FormParser object at 0x7fc8f1405cd0>, <rest_framework.parsers.MultiPartParser object at 0x7fc8f1405d00>], 'authenticators': [<rest_framework.authentication.SessionAuthentication object at 0x7fc8f1405a60>, <rest_framework.authentication.BasicAuthentication object at 0x7fc8f1405eb0>], 'negotiator': <rest_framework.negotiation.DefaultContentNegotiation object at 0x7fc8f1384ac0>, 'parser_context': {'view': <store.views.TrainingToUseAPIView object at 0x7fc8f1375d60>, 'args': (), 'kwargs': {}, 'request': <rest_framework.request.Request: GET '/apiview'>, 'encoding': 'utf-8'}, '_data': <class 'rest_framework.request.Empty'>, '_files': <class 'rest_framework.request.Empty'>, '_full_data': <class 'rest_framework.request.Empty'>, '_content_type': <class 'rest_framework.request.Empty'>, '_stream': <class 'rest_framework.request.Empty'>, 'accepted_renderer': <rest_framework.renderers.BrowsableAPIRenderer object at 0x7fc8f13d4850>, 'accepted_media_type': 'text/html', 'version': None, 'versioning_scheme': None, '_authenticator': None, '_user': <django.contrib.auth.models.AnonymousUser object at 0x7fc8f13d4b20>, '_auth': None}"""

        data = Product.objects.filter(pk__gt=2).values()
        """Без .values data= <QuerySet [<Product: Product object (3)>, <Product: Product object (4)>]>"""
        """c .values data= <QuerySet [{'id': 3, 'title': 'Ice-Cream', 'content': '', 'price': Decimal('68.00')}, {'id': 4, 'title': 'Apple', 'content': '', 'price': Decimal('30.00')}]>"""
        # print('data=', data)

        return Response({"products": list(data)})

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if serializer.is_valid(raise_exception=True):  сохранение через save()
        #     serializer.save()
        print('reauest=', request)
        new_product = Product.objects.create(title=request.data['title'], content=request.data['content'],
                                             price=request.data['price'])
        # new_product = Product object(7)
        # print('ProductSerializer=', ProductSerializer(new_product))
        # print('ProductSerializer.data=', ProductSerializer(new_product).data)
        return Response({'post': ProductSerializer(new_product).data})

        # Возаращаем данные не используя сериализатор
        # return Response({'post': model_to_dict(new_product)})


class TrainingToUseAPIView2(APIView):
    """Используем сериализатор для сохранения"""

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "This product pk does not exists"})
        try:
            instance = Product.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = ProductSerializer2(data=request.data, instance=instance) #request.data = {'title': 1, 'content': 'FFFFFFF', 'price': 550}
        serializer.is_valid(raise_exception=True)
        serializer.save()  #!!!!!!!!! Вот эта штука вызывает метод update т.к. она ждут 2 параметра и мы их в serializer = Product(data=request.data, instance=instance)
        return Response({"post": serializer.data})
    def get(self,request):

        data = Product.objects.all().values()
        return Response({"products": list(data)})

    def post(self, request):
        print('request.data=', request.data)
        serializer = ProductSerializer2(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchasisAPIViev(generics.ListAPIView):
    # Добавлеем ещё одно поле (общая стоимость покупки) Вычисляем на стороне БД.
    queryset = Purchase.objects.all().annotate(
        total_cost=Sum('product_list__price')
    )
    serializer_class = PurchaseSerializer


class PurchasisPrefetchAPIViev(generics.ListAPIView):
    queryset = Purchase.objects.all().annotate(
        total_cost=Sum('product_list__price')
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

        if content == '':
            content = title
        serializer.save(content=content)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer2
    # lookup_field = 'pk'


product_list_view = ProductListAPIView.as_view()
