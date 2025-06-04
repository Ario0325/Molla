from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        return {
            'user_cart': cart,
            'cart_total': cart.get_total_price() if cart else 0,
            'cart_items_count': cart.get_items_count() if cart else 0,
            'cart_items': cart.items.all() if cart else []
        }
    return {
        'user_cart': None,
        'cart_total': 0,
        'cart_items_count': 0,
        'cart_items': []
    }
