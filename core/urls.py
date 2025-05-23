from django.urls import path
from . import views

urlpatterns = [
    path('register/user/', views.register_user, name='register_user'),
    path('users/', views.user_list, name='user_list'),
    path('register/architect/', views.register_architect, name='register_architect'),
    path('architects/', views.architect_list, name='architect_list'),
    path('register/store/', views.register_store, name='register_store'),
    path('stores/', views.store_list, name='store_list'),
    path('register/sale/', views.register_sale, name='register_sale'),
    path('sales/', views.sale_list, name='sale_list'),
]