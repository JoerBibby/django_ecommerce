from django.urls import path
from .views import checkout_page, HomeView, ProductView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('product/<slug>', ProductView.as_view(), name='product_page'),
    path('checkout/', checkout_page, name='checkout_page')
]