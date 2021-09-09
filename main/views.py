from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem, BillingAdress
from django.views.generic import DetailView, ListView, View
from django.utils import timezone
from django.contrib import messages
from .forms import NameForm, LoginForm, BillingAdressForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import stripe




class HomeView(ListView):
    model = Item
    paginate_by = 3
    template_name = 'main/home-page.html'



class ProductView(DetailView):
    model = Item 
    template_name = 'main/product-page.html'


class OrderSummary(LoginRequiredMixin ,View):
    def get(self, *args, **kwargs):
            try:
        
                order_qs = Order.objects.filter(user=self.request.user, ordered=False)
                order = order_qs[0]
                context = {
                    'order': order
                }
            except:
                messages.error(self.request, 'no active order')
                return redirect('/')
        

            return render(self.request, 'order_summary.html', context)

class CheckoutPage(View):
    def get(self, *args, **kwargs):
        form = BillingAdressForm()
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        order = order_qs[0]
        context = {
            'form': form,
            'order': order
        }

        
        return render(self.request, 'checkout-page.html', context )

    def post(self, *args, **kwargs):
        try:
        
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            order = order_qs[0]

            form = BillingAdressForm(self.request.POST or None)
            if form.is_valid():   
                address = form.cleaned_data.get('address')
                address_2 = form.cleaned_data.get('address_2')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAdress(
                    user = self.request.user,
                    address = address,
                    address_2 = address_2 ,
                    country = country ,
                    zip = zip ,
                    same_shipping_address = same_shipping_address ,
                    # save_info = save_info ,
                    payment_option = payment_option
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                print('success')
                return redirect('main:checkout_page')
            
        except ObjectDoesNotExist:
            messages.error(self.request, 'no active order')
            return redirect('/')



class PaymentView(View):

    def get(self, *args, **kwargs):

        return render (self.request, 'payment.html')


       


# Create your views here.
#add item from the product page
@login_required
def add_item_to_cart(request, slug):
    # get the current item from page
    item = get_object_or_404(Item, slug=slug)
    # create an Orderitem version 
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
        # user=request.user,
        # ordered=False)
   
    # check if user has a cart in progress 
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if yes, 
        # if cart already contains item, increase quantity by 1
        # else add order_item to the order
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug):
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'quantity of item increased')
            return redirect('main:product_page', slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, 'item added to cart')
            return redirect('main:product_page', slug=slug)
            
    # if no, create a new order for them, and add the order_item to it
    else:
        time = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=time)
        order.items.add(order_item)
        messages.info(request, 'item added to cart')
    return redirect('main:product_page', slug=slug)
#remove all instances of item, at product page
@login_required 
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        ordered=False)[0]
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug):
            order.items.remove(order_item)
            messages.info(request, 'item removed from cart')
            return redirect('main:order-summary')
        else:
            messages.info(request, 'cart does not contain this item')
            return redirect('main:product_page', slug=slug)
            
            # alert user that cart doesn't contain the item 
    else:
        messages.info(request, 'no active order in progress')
        return redirect('main:product_page', slug=slug)
        #alert user that they do not have an active cart 


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.info(request, 'You have logged in')
            return HttpResponseRedirect('yep')
    else:
        form = LoginForm()
    # add message confirming login 
    # user = request.user
    # string = f"logged in as {user}"
    # messages.info(request, string)
    return render(request, 'main/account/login.html', {'form': form })

def logout(request):
    return render(request, 'main/account/logout.html')

def sign_up(request):
    return render(request, 'main/account/signup.html')

#decrement item at checkout 
def remove_item_at_checkout_cart(request, slug):
    # get the current item from page
    item = get_object_or_404(Item, slug=slug)
    # create an Orderitem version 
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
        # user=request.user,
        # ordered=False)
   
    # check if user has a cart in progress 
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if yes, 
        # if cart already contains item, increase quantity by 1
        # else add order_item to the order
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug):
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, 'quantity of item decreased')
                return redirect('main:order-summary')
            else:
                order.items.remove(order_item)
                messages.info(request, 'item removed from cart')
                return redirect('main:order-summary')
        else:
            messages.info(request, 'cart does not contain this item')
            return redirect('main:order-summary')
    else:
        messages.info(request, 'you do not have an active order')

#increment item at checkout
def add_item_at_checkout(request, slug):
    # get the current item from page
    item = get_object_or_404(Item, slug=slug)
    # create an Orderitem version 
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
        # user=request.user,
        # ordered=False)
   
    # check if user has a cart in progress 
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if yes, 
        # if cart already contains item, increase quantity by 1
        # else add order_item to the order
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug):
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'quantity of item increased')
            return redirect('main:order-summary')
        else:
            messages.info(request, 'cart does not contain this item')
            return redirect('main:order-summary')
    else:
        messages.info(request, 'no active order')
            
    return redirect('main:order-summary')



stripe.api_key = 'sk_test_51JWM55HQ3tnpp7rgOMpHkz5lnSZ4TgAe2ZAF7QirRsDYryWOrLuPl7Fw9iljAtYPhbRKSxQLVIAQqRb86xAwhpNH009mFqS0WB'

def create_checkout_session(request):
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'T-shirt',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
  )

    return redirect(session.url, code=303)



