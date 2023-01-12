from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', product_list_create_view),
    path('<int:pk>/', product_list_view),
    path('all_users', UsersListAPIView.as_view()),
    path('tr', UsersTransactionAPIViev.as_view()),
    path('purchase', PurchasisAPIViev.as_view()),
    path('apiview', TrainingToUseAPIView.as_view()),
    path('apiview2', TrainingToUseAPIView2.as_view()),
    path('apiview2/<int:pk>/', TrainingToUseAPIView2.as_view()),
]