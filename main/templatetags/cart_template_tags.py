from ..views import Order
from django import template

register = template.Library()

@register.filter
def cart_count(user):
    if user.is_authenticated:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order=order_qs[0]
            return order.items.count()
    else:
        return 0 
