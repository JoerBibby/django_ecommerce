from django.urls import path
from .views import (
    CheckoutPage,
    FilteredHomeViewByCategory,
    HomeView,
    ProductView,
    SearchView,
    add_item_to_cart,
    remove_from_cart,
    login,
    logout,
    sign_up,
    OrderSummary,
    remove_item_at_checkout_cart,
    add_item_at_checkout,
    PaymentView,
    create_checkout_session)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('filter/<category>', FilteredHomeViewByCategory.as_view(), name='filtered'),
    path('search/<title>', SearchView.as_view(), name='search' ),
    path('product/<slug>', ProductView.as_view(), name='product_page'),
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    path('checkout/', CheckoutPage.as_view(), name='checkout_page'),
    path('add-to-cart/<slug>', add_item_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('accounts/login', login, name='login'),
    path('accounts/logout', logout, name='logout'),
    path('accounts/signup', sign_up, name='signup'),
    path('remove-at-checkout/<slug>', remove_item_at_checkout_cart, name='remove-from-checkout'),
    path('add-item-at-checkout/<slug>', add_item_at_checkout, name='add-to-checkout'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    path('create-checkout-session/', create_checkout_session, name='checkout-session')
]


