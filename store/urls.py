from django.urls import path, include
from rest_framework import routers

from . import views
from .views import *

router = routers.SimpleRouter()
router.register(r'edit', AuthUsersAddDeleteUpdateProductsAPIView)
router.register(r'find', AdminGetAllUsersPurchasis)

urlpatterns = [
    path('', product_list_create_view),
    path('<int:pk>/', product_list_view),
    path('all_users', UsersListAPIView.as_view()),
    path('tr', UsersTransactionAPIViev.as_view()),
    path('purchase', PurchasisAPIViev.as_view()),
    path('apiview', TrainingToUseAPIView.as_view()),
    path('apiview2', TrainingToUseAPIView2.as_view()),
    path('apiview2/<int:pk>/', TrainingToUseAPIView2.as_view()),

    path('products', AllUsersGetListAPIView.as_view({'get': "list"})),
    path('prod/', include(router.urls)),
    path('purch/', include(router.urls)),


]