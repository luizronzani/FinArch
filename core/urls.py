from django.urls import path
from . import views
from core.views import landing_page

urlpatterns = [
    #users
    path('register/user/', views.register_user, name='register_user'),
    path('register/user_store/', views.register_user_store, name='register_user_store'),
    path('user-store/delete/<int:pk>/', views.delete_user_store, name='delete_user_store'),
    path('user_store/', views.user_store, name='user_store'),
    path('user_store/filter/', views.user_store_filter, name='user_store_filter'),
    path('users/', views.user_list, name='user_list'),
    #architects
    path('register/architect/', views.register_architect, name='register_architect'),
    path('architects/', views.architect_list, name='architect_list'),
    #stores
    path('register/store/', views.register_store, name='register_store'),
    path('stores/', views.store_list, name='store_list'),
    #sales
    path('register/sale/', views.register_sale, name='register_sale'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/ajax/', views.sales_ajax, name='sales_ajax'),

    #relatorios
    path('relatorios/', views.relatorios, name='relatorios'),
    #landing page
    path('', landing_page, name='landing'),  # vírgula adicionada aqui
    
]
