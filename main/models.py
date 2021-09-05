from main.forms import PAYMENT_OPTIONS
from django.db import models
from django.conf import settings
from django.db.models.fields import SlugField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.contrib.auth.models import User

CATEGORY_CHOICES = [ 
    ('S', 'Shirt'),
    ('SW', 'Sportwear'),
    ('OW', 'Outwear')
]

LABEL_CHOICES = [ 
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
]

PAYMENT_OPTIONS = [
    ("S", "Stripe"),
    ("P", "Paypal")
]

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default='P')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='S')
    slug = models.SlugField(default='item')
    description = models.TextField(default='This is an item')

    def get_absolute_url(self):
        return reverse("main:product_page", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={"slug": self.slug})

    def get_remove_at_checkout_url(self):
        return reverse("main:remove-from-checkout", kwargs={"slug": self.slug})

    def get_add_at_checkout_url(self):
        return reverse("main:add-to-checkout", kwargs={"slug": self.slug})



class OrderItem(models.Model):
    item = ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_price(self):
        return self.item.price * self.quantity

    def get_total_discount_price(self):
        return self.item.discount_price * self.quantity



    
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False) 
    items = models.ManyToManyField(OrderItem)
    created_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey('BillingAdress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            if order_item.item.discount_price:
                total += order_item.get_total_discount_price()
            else:
                total += order_item.get_total_price()
        return total 


class BillingAdress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=1000)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    same_shipping_address = models.BooleanField()

    payment_option = models.CharField(choices=PAYMENT_OPTIONS, max_length=1, default="P")

    def __str__(self):
        return self.user.username
