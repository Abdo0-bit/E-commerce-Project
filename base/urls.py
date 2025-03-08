from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name='home'),
    path('cart/' , views.cart , name='cart'),
    path('product/<int:pk>' , views.product_details , name='product_details'),
    path('add_product/<int:pk>' , views.add_product , name='add_product'),
    path('delete_product/<int:pk>' , views.delete_product , name='delete_product'),
    path('update_quantity/<int:pk>' , views.update_quantity , name='update_quantity'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
]