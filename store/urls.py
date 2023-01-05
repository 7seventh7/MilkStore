from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', product_list_create_view),
    path('<int:pk>/', product_list_view),
    path('all_users', UsersListAPIView.as_view()),
    path('tr', UsersTransactionAPIViev.as_view())
]