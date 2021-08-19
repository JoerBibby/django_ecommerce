from django.db import models
from django.conf import settings
from django.db.models.fields import SlugField
from django.db.models.fields.related import ForeignKey
from django.urls import reverse

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

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default='P')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default='S')
    slug = models.SlugField(default='item')
    description = models.TextField(default='This is an item')

    def get_absolute_url(self):
        return reverse("main:product_page", kwargs={"slug": self.slug})
    

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    created_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    def __str__(self):
        return self.user




