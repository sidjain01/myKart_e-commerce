from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_dob = models.DateField()
    user_phone = models.CharField(max_length=12)

    def __str__(self):
        return self.user

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_date = models.DateField()
    sub_category = models.CharField(max_length=50, default='')
    images = models.ImageField(upload_to='shop/images', default='')
    
    def __str__(self):
        return self.product_name

class CouponDis(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=50)
    discount_percent = models.PositiveIntegerField(default=0,validators=[MinValueValidator(1),MaxValueValidator(100)])
    
class Shipping_Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 50)
    mobile = models.CharField(max_length=12) 
    pincode = models.CharField(max_length = 6) 
    address = models.CharField(max_length = 300)
    city = models.CharField(max_length = 100) 
    state = models.CharField(max_length = 100)
    date_added = models.DateTimeField(auto_now_add = True)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50, default=None, null=True)
    totalamt = models.IntegerField(default=None, null=True)
    trans_mode = models.CharField(max_length=30,default=None,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(CouponDis, on_delete=models.PROTECT,default=None,null=True)
    shipping =  models.ForeignKey(Shipping_Address, on_delete=models.SET_NULL, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_qty = models.IntegerField(default=1)

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    msg = models.TextField()
    date = models.DateField(default=date.today)

