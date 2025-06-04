from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.add_to_cart, name='add-to-cart'),
    path('detail/', views.cart_detail, name='cart-detail'),
    path('empty/', views.cart_empty, name='cart-empty'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove-item'),
    path('update/<int:item_id>/', views.update_cart_quantity, name='update-quantity'),
    path('clear/', views.clear_cart, name='clear-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/request/', views.payment_request, name='payment-request'),
    path('payment/verify/', views.payment_verify, name='payment-verify'),
    path('payment/success/', views.payment_success, name='payment-success'),
    path('payment/failed/', views.payment_failed, name='payment-failed'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update-quantity'),
]
