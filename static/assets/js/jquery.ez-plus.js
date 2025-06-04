$(document).ready(function() {
    // تابع دریافت کوکی CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // بروزرسانی تعداد محصول
    $('.quantity-input').change(function() {
        let itemId = $(this).data('item-id');
        let quantity = parseInt($(this).val());
        let maxStock = parseInt($(this).attr('max'));
        let currentValue = parseInt($(this).prop('defaultValue'));

        // اعتبارسنجی تعداد
        if (isNaN(quantity) || quantity <= 0) {
            Swal.fire({
                icon: 'error',
                title: 'خطا',
                text: 'تعداد باید عددی مثبت باشد'
            });
            $(this).val(currentValue);
            return;
        }

        if (quantity > maxStock) {
            Swal.fire({
                icon: 'error',
                title: 'موجودی ناکافی',
                text: `حداکثر موجودی: ${maxStock}`
            });
            $(this).val(currentValue);
            return;
        }

        $.ajax({
            url: `/cart/update-quantity/${itemId}/`,
            method: 'POST',
            data: {
                'quantity': quantity,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.status === 'success') {
                    // بروزرسانی قیمت محصول
                    $(`#total-${itemId}`).text(response.new_total);

                    // بروزرسانی مجموع سبد خرید
                    $('#cart-total').text(response.cart_total);
                    $('#cart-total-payable').text(response.cart_total);

                    // بروزرسانی تعداد آیتم‌ها
                    $('.cart-items-count').text(response.cart_items_count);

                    // نمایش پیغام موفقیت
                    Swal.fire({
                        icon: 'success',
                        title: 'تعداد محصول بروزرسانی شد',
                        showConfirmButton: false,
                        timer: 1500
                    });
                } else {
                    // نمایش پیغام خطا
                    Swal.fire({
                        icon: 'error',
                        title: 'خطا',
                        text: response.message
                    });

                    // بازگرداندن مقدار قبلی
                    $(`.quantity-input[data-item-id="${itemId}"]`).val(currentValue);
                }
            },
            error: function() {
                Swal.fire({
                    icon: 'error',
                    title: 'خطای سیستمی',
                    text: 'لطفاً مجدداً تلاش کنید'
                });

                // بازگرداندن مقدار قبلی
                $(`.quantity-input[data-item-id="${itemId}"]`).val(currentValue);
            }
        });
    });

    // حذف محصول از سبد خرید
    $('.remove-item').click(function() {
        let itemId = $(this).data('item-id');

        Swal.fire({
            title: 'حذف محصول',
            text: 'آیا از حذف این محصول از سبد خرید مطمئن هستید؟',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'بله، حذف شود',
            cancelButtonText: 'انصراف'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: `/cart/remove-item/${itemId}/`,
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            // حذف ردیف محصول از جدول
                            $(`#cart-item-${itemId}`).fadeOut(300, function() {
                                $(this).remove();

                                // بروزرسانی مجموع سبد خرید
                                $('#cart-total').text(response.cart_total);
                                $('#cart-total-payable').text(response.cart_total);

                                // بروزرسانی تعداد آیتم‌ها
                                $('.cart-items-count').text(response.cart_items_count);

                                // اگر سبد خرید خالی شد، صفحه را رفرش کن
                                if ($('.cart-item').length === 0) {
                                    location.reload();
                                }

                                Swal.fire({
                                    icon: 'success',
                                    title: 'محصول حذف شد',
                                    showConfirmButton: false,
                                    timer: 1500
                                });
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'خطا',
                                text: response.message
                            });
                        }
                    },
                    error: function() {
                        Swal.fire({
                            icon: 'error',
                            title: 'خطای سیستمی',
                            text: 'لطفاً مجدداً تلاش کنید'
                        });
                    }
                });
            }
        });
    });

    // پاک کردن کل سبد خرید
    $('#clear-cart').click(function() {
        Swal.fire({
            title: 'پاک کردن سبد خرید',
            text: 'آیا مطمئن هستید که می‌خواهید تمام محصولات را حذف کنید؟',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'بله، پاک شود',
            cancelButtonText: 'انصراف'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '{% url "cart:clear-cart" %}',
                    method: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            // بارگذاری مجدد صفحه
                            location.reload();
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'خطا',
                                text: response.message
                            });
                        }
                    },
                    error: function() {
                        Swal.fire({
                            icon: 'error',
                            title: 'خطای سیستمی',
                            text: 'لطفاً مجدداً تلاش کنید'
                        });
                    }
                });
            }
        });
    });
});
