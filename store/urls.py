from django.urls import path, include
from rest_framework import routers

from . import views
from .views import *

router = routers.SimpleRouter()
router.register(r'prod', AuthUsersAddDeleteUpdateProductsAPIView)
router.register(r'admin_purch', AdminGetAllUsersPurchasis)
router.register(r'user_purch', UsersCRUDTheirPurchases,  basename='Purchace')


urlpatterns = [
    path('', product_list_create_view),
    path('<int:pk>/', product_list_view),
    path('all_users', UsersListAPIView.as_view()),
    path('tr', UsersTransactionAPIViev.as_view()),
    path('purchase1', PurchasisAPIViev.as_view()),
    path('apiview', TrainingToUseAPIView.as_view()),
    path('apiview2', TrainingToUseAPIView2.as_view()),
    path('apiview2/<int:pk>/', TrainingToUseAPIView2.as_view()),

    path('products', AllUsersGetListAPIView.as_view({'get': "list"})),
    path('trans', AllTransactions.as_view({'get': "list"})),
    path('transu', UserTransactions.as_view({'get': "list"})),
    path('', include(router.urls)),
    path('all_users', UsersListAPIView.as_view()),
]