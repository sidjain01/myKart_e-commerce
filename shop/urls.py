from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name='shop_home'),
    path('login/', views.login, name='shop_login'),
    path('logout/', views.logout, name='shop_logout'),
    path('signup/', views.signup, name='shop_signup'),
    path('about/', views.about, name='shop_about'),
    path('addtocart/<int:prod_id>/', views.home_addtocart, name='shop_addtocart'),
    path('addandbuy/<int:prod_id>/', views.home_addandbuy, name='shop_addandbuy'),
    path('contact/', views.contact, name='shop_contact'),
    path('tracker/', views.tracker, name='shop_tracker'),
    path('search/', views.search, name='shop_search'),
    path('productview/<int:id>', views.product_view, name='shop_product_view'),
    path('cart/', views.cart, name='shop_cart'),
    path('remove/<int:prod_id>', views.remove_item, name='shop_remove'),
    path('increase/<int:prod_id>', views.increase_item, name='shop_increase'),
    path('decrease/<int:prod_id>', views.decrease_item, name='shop_decrease'),
    path('applycoupon/', views.apply_coupon, name='shop_applycoupon'),
    path('checkout/', views.checkout, name='shop_checkout'),
    path('deliver', views.shipping_address, name = 'deliver'),
    path('payment/', views.payment, name='shop_payment'),
    path('handlepayment/', views.handlepayment, name='shop_handlepayment'),
    path('search/', views.search, name="shop_search"),
]