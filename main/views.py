from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem
from django.views.generic import DetailView, ListView



class HomeView(ListView):
    model = Item
    template_name = 'main/home-page.html'



class ProductView(DetailView):
    model = Item 
    template_name = 'main/product-page.html'




def checkout_page(request):

    return render(request, 'main/checkout-page.html')

# Create your views here.

def add_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug):
            order_item.quantity += 1
            order_item.save()
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
    return redirect('main:product_page', kwargs={'slug': slug})
        





