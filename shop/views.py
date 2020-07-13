from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Product, UserInfo, Contact, Order, OrderItem, CouponDis, Shipping_Address
from math import ceil
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('shop_home')
        else:
            messages.info(request, 'Invalid Credentials!')
            return redirect('shop_login')
    else:
        return render(request, 'shop/login.html')


def logout(request):
    auth.logout(request)
    return redirect('shop_home')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').title()
        last_name = request.POST.get('last_name').title()
        email = request.POST.get('email')
        username = request.POST.get('username')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        if pwd1 == pwd2:
            if User.objects.filter(email=email).exists():
                messages.info(
                    request, 'Account associated to entered email already exist!')
                return redirect('shop_signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken!')
                return redirect('shop_signup')
            else:
                if username is not None:
                    user = User.objects.create_user(
                        username=username, password=pwd1, first_name=first_name, last_name=last_name, email=email)
                    user.save()
                    user_info = UserInfo(
                        user_id=user.id, user_dob=dob, user_phone=phone)
                    user_info.save()
                    return redirect('shop_login')
                else:
                    messages.info(request, 'Enter valid username')
                    return redirect('shop_signup')
        else:
            messages.info(request, 'Password does not match!')
            return redirect('shop_signup')
    else:
        return render(request, 'shop/signup.html')


def index(request):
    # products = Product.objects.all()
    allprod = []
    cat_prod = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in cat_prod}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        no_slides = n//4 + ceil((n/4) - (n//4))
        allprod.append([prod, range(1, no_slides), no_slides])
    params = {'allprod': allprod}
    return render(request, 'shop/index.html', params)


def home_addtocart(request, prod_id):
    if request.user.is_authenticated:
        prod = Product.objects.get(product_id=prod_id)
        current_order = Order.objects.filter(user=request.user, completed=False)
        if current_order.exists():
            current_order_object = current_order[0]
            order_item = OrderItem.objects.filter(order=current_order_object, product=prod)
            if order_item.exists():
                messages.info(request, 'Item already exists. You can alter quantity from cart!!')
                return redirect('shop_product_view',prod_id)
            else:
                order_item = OrderItem.objects.create(order=current_order_object, product=prod)
                order_item.save()
                messages.info(request, 'Item added to cart!!')
                return redirect('shop_product_view',prod_id)
        else:
            current_order = Order.objects.create(user=request.user)
            current_order.save()
            order_item = OrderItem.objects.create(order=current_order, product=prod)
            order_item.save()
            messages.info(request, 'Item added to cart!!')
            return redirect('shop_product_view',prod_id)
    else:
        return redirect('shop_login')


def home_addandbuy(request, prod_id):
    if request.user.is_authenticated:
        prod = Product.objects.get(product_id=prod_id)
        current_order = Order.objects.filter(user=request.user, completed=False)
        if current_order.exists():
            current_order_object = current_order[0]
            order_item = OrderItem.objects.filter(order=current_order_object, product=prod)
            if order_item.exists():
                return redirect('shop_cart')
            else:
                order_item = OrderItem.objects.create(order=current_order_object, product=prod)
                order_item.save()
                return redirect('shop_cart')
        else:
            current_order = Order.objects.create(user=request.user)
            current_order.save()
            order_item = OrderItem.objects.create(order=current_order, product=prod)
            order_item.save()
            return redirect('shop_cart')
    else:
        return redirect('shop_login')


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name').title()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        msg = request.POST.get('txtMsg')
        if msg is not None:
            contact = Contact.objects.create(
                name=name, email=email, phone=phone, msg=msg)
            contact.save()
            messages.info(
                request, 'Thanks for submitting your query. We will revert back to you soon.')
            return redirect('shop_home')
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.user.is_authenticated:
        order_qset = Order.objects.filter(user=request.user, completed=True)
        orders = False
        orderList = []
        if order_qset.exists():
            orders = True
            for order in order_qset:
                order_items = OrderItem.objects.filter(order=order)
                orderList.append([order,order_items]) 
        params = {'orderExist': orders, 'orderList': orderList}
        return render(request, 'shop/track.html', params)
    else:
        return redirect('shop_login')


def search(request):
    value = request.GET.get('search')
    products = Product.objects.all()
    val_sp = value.lower().split(" ")
    categories = set()
    name_prod = []
    cat_prod = []
    desc_prod = []
    query_result = []
    for product in products:
        if value.lower() in product.product_name.lower():
            name_prod.append(product)
            categories.add(product.sub_category)
        else: 
            for val in val_sp:
                if val in product.sub_category.lower():
                    cat_prod.append(product)
                    categories.add(product.sub_category)
                elif val in product.product_desc.lower():
                    desc_prod.append(product)
                    categories.add(product.sub_category)
    
    query_result = name_prod + cat_prod + desc_prod
    categories_l = list(categories)
    return render(request, 'shop/search.html',{'search':value, 'prod_list':query_result,'categories':categories_l})


def product_view(request, id):
    product = Product.objects.filter(product_id=id)
    prod = {'product': product}
    return render(request, 'shop/prod_view.html', prod)


def cart(request):
    if request.user.is_authenticated:
        order_qset = Order.objects.filter(user=request.user, completed=False)
        cart_items = []
        if order_qset.exists():
            order = order_qset[0]
            cart_items = OrderItem.objects.filter(order=order)
        params = {'cart_items':cart_items}
        return render(request, 'shop/cart.html', params)
    else:
        return redirect('shop_login')


def remove_item(request, prod_id):
    order_qset = Order.objects.filter(user=request.user, completed=False)
    order = order_qset[0]
    prod = Product.objects.get(product_id=prod_id)
    OrderItem.objects.filter(order=order, product=prod).delete()
    return redirect('shop_cart')


def increase_item(request, prod_id):
    order = Order.objects.filter(user=request.user, completed=False)[0]
    prod = Product.objects.get(product_id=prod_id)
    order_item = OrderItem.objects.filter(order=order, product=prod)[0]
    if order_item.order_qty < 10 :
        order_item.order_qty = order_item.order_qty + 1
        order_item.save()
    else:
        messages.info(request, 'Max cart limit for this particular item reached!')
    return redirect('shop_cart')


def decrease_item(request, prod_id):
    order = Order.objects.filter(user=request.user, completed=False)[0]
    prod = Product.objects.get(product_id=prod_id)
    order_item = OrderItem.objects.filter(order=order, product=prod)[0]
    if order_item.order_qty > 1 :
        order_item.order_qty = order_item.order_qty - 1
        order_item.save()
    else:
        messages.info(request, 'Min cart limit for this particular item reached, click on Remove button if you want to remove product from Cart!')
    return redirect('shop_cart')


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon').upper()
        if coupon_code is not None:
            coupon = CouponDis.objects.filter(coupon_code=coupon_code)
            if coupon.exists():
                order = Order.objects.filter(user=request.user, completed=False)
                if order.exists():
                    order.update(coupon=coupon[0])
                    return redirect('shop_cart')
                else:
                    messages.info(request,"Try after adding items in the Cart!")
                    return redirect('shop_cart')
            else:
                order = Order.objects.filter(user=request.user, completed=False)
                if order.exists():
                    order.update(coupon=None)
                return redirect('shop_cart')
        else:
            messages.info(request,"Enter valid coupon code!")
            return redirect('shop_cart')
    else:
        return redirect('shop_cart')
    

def shipping_address(request):
    if request.method=='POST':
        address = None
        if request.POST.get('addressid'):
            address_id = request.POST.get('addressid')
            address = Shipping_Address.objects.get(id=address_id)       
        else:
            full_name = request.POST.get('full_name')
            mobile = request.POST.get('mobile')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            address = Shipping_Address.objects.create(user_id= request.user, full_name = full_name, mobile= mobile,
            pincode= pincode, address= address, city= city, state= state)
            address.save()
        order = Order.objects.get(user_id = request.user, completed = False)
        order.shipping = address
        order.save()
        # login(request, user)
        return render(request, 'shop/checkout.html')
    else: 
        addresses = Shipping_Address.objects.filter(user_id= request.user)
        return render(request, 'shop/deliver.html', {"addresses": addresses})


def checkout(request):
    if request.method == 'POST':
        totalamt = request.POST.get('totalamt')
        totalamt = int(totalamt)
        order = Order.objects.filter(user=request.user, completed=False)
        order.update(totalamt=totalamt)
        return redirect('deliver')
    return redirect('shop_cart')
        

def payment(request):
    if request.method == 'POST':
        pay = request.POST.get('paymentMethod')
        if pay == "paydel":
            order = Order.objects.filter(user=request.user, completed=False)[0]
            order.completed=True
            order.trans_mode="Cash On Delivery"
            order.save()
            response_dict={
                'ORDERID' : str(order.order_id),
                'STATUS' : 'TXN_SUCCESS'
            }
            return render(request, 'shop/complete.html', {'response': response_dict})
        else:
            order = Order.objects.filter(user=request.user, completed=False)[0]
            param_dict ={
                'MID':'WorldP64425807474247',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(order.totalamt),
                'CUST_ID': request.user.email,
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE':'WEBSTAGING',
                'CHANNEL_ID':'WEB',
                'CALLBACK_URL':'http://localhost:8000/shop/handlepayment/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY) 
            return render(request, 'shop/paytm.html', {'param_dict':param_dict})
    return redirect('shop_checkout')


@csrf_exempt
def handlepayment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            order_id = int(response_dict['ORDERID'])
            order = Order.objects.get(order_id=order_id)
            order.completed=True
            order.trans_mode="Paid Online"
            order.transaction_id=response_dict['TXNID']
            order.save()
            return render(request, 'shop/complete.html', {'response': response_dict})            
        else:
            return render(request, 'shop/complete.html', {'response': response_dict})            
    else:
        return redirect('shop_cart')