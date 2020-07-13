from django.contrib import admin
from .models import Product, UserInfo, Order, Category, OrderItem, Contact, CouponDis
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(CouponDis)
