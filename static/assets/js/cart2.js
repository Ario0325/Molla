$(document).ready(function() {
    // Format price function
    function formatPrice(price) {
        return new Intl.NumberFormat('fa-IR').format(price) + ' تومان';
    }

    // Calculate line total
    function calculateLineTotal(row) {
        let quantity = parseInt(row.find('.quantity-input').val()) || 1;
        let price = parseInt(row.find('.price-col').text().replace(/[^\d]/g, ''));
        return quantity * price;
    }

    // Update all totals
    function updateAllTotals() {
        let cartTotal = 0;

        // Update each line total
        $('tr[id^="cart-item-"]').each(function() {
            let lineTotal = calculateLineTotal($(this));
            $(this).find('.total-col').html(formatPrice(lineTotal));
            cartTotal += lineTotal;
        });

        // Update cart totals
        $('#cart-total, #cart-total-payable').html(formatPrice(cartTotal));
    }

    // Handle quantity changes
    $('.quantity-input').on('change input', function() {
        let itemId = $(this).data('item-id');
        let quantity = parseInt($(this).val()) || 1;
        let row = $(this).closest('tr');

        // Instant UI update
        updateAllTotals();

        // Send update to server
        $.ajax({
            url: `/cart/update-quantity/${itemId}/`,
            method: 'POST',
            data: {
                'quantity': quantity,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('.cart-items-count').text(response.cart_items_count);

                    const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 1000,
                        timerProgressBar: true
                    });
                    Toast.fire({
                        icon: 'success',
                        title: 'بروزرسانی شد'
                    });
                } else {
                    // Revert to server quantity if error
                    $(this).val(response.current_quantity);
                    updateAllTotals();

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
    });
});
