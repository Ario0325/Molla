import uuid
import logging
logger = logging.getLogger(__name__)
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
import requests
import json
from django.views.decorators.http import require_POST
from Product_module.templatetags.product_extras import price_format
from .models import Cart, CartItem
from .forms import CheckoutForm
from Product_module.models import Product


def generate_ref_id():
    return f"REF-{uuid.uuid4().hex[:8].upper()}"

def verify_payment(authority, amount):
    return True

def verify_payment(authority, amount):
    data = {
        "merchant_id": settings.MERCHANT_ID,
        "amount": amount * 10,
        "authority": authority
    }

    try:
        response = requests.post(settings.ZARINPAL_API_VERIFY, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['data']['code'] == 100
        return False
    except:
        return False

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        size = data.get('size')
        color = data.get('color')

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user, is_paid=False).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)

            product = get_object_or_404(Product, id=product_id)

            if product.stock < quantity:
                return JsonResponse({
                    'status': 'error',
                    'message': 'موجودی کافی نیست'
                })

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                size=size,
                color=color,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({
                'status': 'success',
                'message': 'محصول به سبد خرید اضافه شد',
                'cart_total': cart.get_total_price(),
                'cart_items_count': cart.get_items_count()
            })

        return JsonResponse({
            'status': 'error',
            'message': 'لطفا ابتدا وارد حساب کاربری خود شوید'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'درخواست نامعتبر'
    })


@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart or not cart.items.exists():
        return redirect('cart:cart-empty')

    context = {
        'cart': cart,
    }
    return render(request, 'Cart_module/cart_detail.html', context)


def cart_empty(request):
    return render(request, 'Cart_module/cart_empty.html')


@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()

        return JsonResponse({
            'status': 'success',
            'message': 'محصول از سبد خرید حذف شد',
            'cart_total': f"{cart.get_total_price():,} تومان",
            'cart_items_count': cart.get_items_count()
        })

    return JsonResponse({
        'status': 'error',
        'message': 'درخواست نامعتبر'
    })


@require_POST
def update_quantity(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity > cart_item.product.stock:
            return JsonResponse({
                'status': 'error',
                'message': 'موجودی کافی نیست',
                'current_quantity': cart_item.quantity
            })

        if new_quantity < 1:
            new_quantity = 1

        cart_item.quantity = new_quantity
        cart_item.save()

        return JsonResponse({
            'status': 'success',
            'item_total': price_format(cart_item.get_total_price()),
            'cart_total': price_format(cart_item.cart.get_total_price()),
            'cart_items_count': cart_item.cart.get_items_count()
        })

    except CartItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'آیتم مورد نظر یافت نشد'
        })

@login_required
def clear_cart(request):
    if request.method == 'POST':
        try:
            cart = Cart.objects.filter(user=request.user, is_paid=False).first()

            if cart:
                cart.items.all().delete()

                return JsonResponse({
                    'status': 'success',
                    'message': 'سبد خرید با موفقیت خالی شد'
                })

            return JsonResponse({
                'status': 'error',
                'message': 'سبد خرید یافت نشد'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'خطا در خالی کردن سبد خرید'
            })

    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart or not cart.items.exists():
        return redirect('cart:cart-empty')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # به روز رسانی مستقیم فیلدهای Cart
            cart.first_name = form.cleaned_data['first_name']
            cart.last_name = form.cleaned_data['last_name']
            cart.phone = form.cleaned_data['phone']
            cart.address = form.cleaned_data['address']
            cart.postal_code = form.cleaned_data['postal_code']
            cart.description = form.cleaned_data.get('description', '')

            cart.save()

            messages.success(request, 'اطلاعات با موفقیت ثبت شد')
            return redirect('cart:payment-request')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {errors}")
    else:
        initial_data = {
            'first_name': cart.first_name or '',
            'last_name': cart.last_name or '',
            'phone': cart.phone or '',
            'address': cart.address or '',
            'postal_code': cart.postal_code or '',
            'description': cart.description or '',
        }
        form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'Cart_module/checkout.html', context)
@login_required
def payment_request(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart or not cart.items.exists():
        return redirect('cart:cart-empty')

    if not all([cart.first_name, cart.last_name, cart.phone, cart.address, cart.postal_code]):
        messages.warning(request, 'لطفا ابتدا اطلاعات تحویل را تکمیل کنید')
        return redirect('cart:checkout')

    try:
        total_amount = cart.get_total_price()

        transaction_id = generate_ref_id()

        payment_context = {
            'amount': total_amount,
            'cart_id': cart.id,
            'transaction_id': transaction_id,
            'user_email': request.user.email,
            'user_mobile': cart.phone
        }

        request.session['payment_details'] = payment_context

        logger.info(f"Payment Request - Cart ID: {cart.id}, Amount: {total_amount}")

        return render(request, 'Cart_module/payment_gateway.html', payment_context)

    except Exception as e:
        logger.error(f"Payment Request Error: {str(e)}")
        messages.error(request, 'خطا در آماده سازی پرداخت')
        return redirect('cart:checkout')


@login_required
def payment_verify(request):
    authority = request.GET.get('Authority', '')
    status = request.GET.get('Status', '')

    cart = Cart.objects.filter(
        payment_authority=authority,
        is_paid=False,
        user=request.user
    ).first()

    if not cart:
        cart = Cart.objects.filter(
            user=request.user,
            is_paid=False
        ).first()

    if not cart:
        messages.error(request, 'سبد خرید معتبری یافت نشد')
        return redirect('cart:cart-detail')

    try:
        status = 'OK'

        if status == 'OK':
            for item in cart.items.all():
                if item.quantity > item.product.stock:
                    messages.error(request, f'موجودی محصول {item.product.title} کافی نیست')
                    return redirect('cart:cart-detail')

            cart.is_paid = True
            cart.payment_date = timezone.now()
            cart.payment_ref_id = generate_ref_id()
            cart.payment_status = 'SUCCESS'
            cart.save()

            try:
                cart.update_stock()
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('cart:cart-detail')

            Cart.objects.create(user=request.user)

            messages.success(request, 'پرداخت با موفقیت انجام شد')
            return redirect('cart:payment-success')
        else:
            cart.payment_status = 'FAILED'
            cart.save()
            messages.error(request, 'پرداخت ناموفق بود')
            return redirect('cart:payment-failed')

    except Exception as e:
        messages.error(request, 'خطا در پردازش پرداخت')
        return redirect('cart:payment-failed')

    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    cart = get_object_or_404(Cart, payment_authority=authority, is_paid=False)

    if status == 'OK':
        data = {
            "merchant_id": settings.MERCHANT_ID,
            "amount": cart.get_total_price() * 10,
            "authority": authority
        }

        try:
            response = requests.post(settings.ZARINPAL_API_VERIFY, json=data)
            if response.status_code == 200:
                result = response.json()
                if result['data']['code'] == 100:
                    cart.is_paid = True
                    cart.payment_date = timezone.now()
                    cart.payment_ref_id = result['data']['ref_id']
                    cart.payment_status = 'SUCCESS'
                    cart.save()

                    for item in cart.items.all():
                        product = item.product
                        product.stock -= item.quantity
                        product.save()

                    Cart.objects.create(user=request.user)

                    messages.success(request, 'پرداخت با موفقیت انجام شد')
                    return redirect('cart:payment-success')

        except Exception as e:
            cart.payment_status = 'ERROR'
            cart.save()
            messages.error(request, 'خطا در تایید پرداخت')
    else:
        cart.payment_status = 'CANCELED'
        cart.save()
        messages.error(request, 'پرداخت ناموفق بود')

    return redirect('cart:payment-failed')


@login_required
def payment_success(request):
    last_cart = Cart.objects.filter(user=request.user, is_paid=True).order_by('-payment_date').first()
    return render(request, 'Cart_module/payment_success.html', {'cart': last_cart})


@login_required
def payment_failed(request):
    return render(request, 'Cart_module/payment_failed.html')


def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({
                'status': 'success',
                'new_total': cart_item.get_total_price(),
                'cart_total': cart_item.cart.get_total_price()
            })
    return JsonResponse({'status': 'error'})


@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            cart = cart_item.cart

            cart_item.delete()

            return JsonResponse({
                'status': 'success',
                'message': 'محصول با موفقیت حذف شد',
                'cart_total': f"{cart.get_total_price():,} تومان",
                'cart_items_count': cart.get_items_count()
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'خطا در حذف محصول'
            })

    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر'})


@login_required
def payment_request(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart or not cart.items.exists():
        return redirect('cart:cart-empty')

    # Generate unique transaction ID
    transaction_id = f'TRX-{uuid.uuid4().hex[:8].upper()}'

    context = {
        'amount': cart.get_total_price(),
        'order_id': cart.id,
        'transaction_id': transaction_id
    }

    request.session['payment_transaction_id'] = transaction_id

    return render(request, 'Cart_module/test_payment.html', context)
@login_required
def payment_process(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart:
        return redirect('cart:cart')

    context = {
        'amount': cart.get_total_price(),
        'order_id': cart.id,
        'transaction_id': request.session.get('payment_transaction_id')
    }

    return render(request, 'Cart_module/test_payment.html', context)



@login_required
def payment_verify(request):
    cart = Cart.objects.filter(
        user=request.user,
        is_paid=False
    ).first()

    if not cart:
        messages.error(request, 'سبد خرید معتبری یافت نشد')
        return redirect('cart:cart-detail')

    cart.is_paid = True
    cart.payment_date = timezone.now()
    cart.payment_ref_id = generate_ref_id()
    cart.payment_status = 'SUCCESS'
    cart.save()

    cart.update_stock()

    Cart.objects.create(user=request.user)

    messages.success(request, 'پرداخت با موفقیت انجام شد')
    return redirect('cart:payment-success')