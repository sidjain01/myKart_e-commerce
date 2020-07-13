from .models import Order, OrderItem, CouponDis

def cart_total(request):
    quantity = 0
    sub_total = 0
    discount = 0
    total = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, completed=False)
        if order.exists():
            order = order[0]
            order_item = OrderItem.objects.filter(order=order)
            for item in order_item:
                quantity+= item.order_qty
                sub_total+= (item.product.price * item.order_qty)
            discount_coup = order.coupon
            if discount_coup is not None:
                coupon = CouponDis.objects.get(coupon_id=discount_coup.coupon_id)
                discount_per = coupon.discount_percent
                discount = (sub_total*discount_per)//100
            total = sub_total-discount 

    return{
        'cart_total': quantity,
        'sub_total': sub_total,
        'discount': discount,
        'total': total
    }
