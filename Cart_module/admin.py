from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'قیمت کل'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'postal_code', 'is_paid', 'payment_date', 'payment_status')
    list_filter = ('is_paid', 'payment_status', 'payment_date')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone', 'payment_ref_id', 'postal_code')
    readonly_fields = ('payment_date', 'payment_ref_id', 'payment_authority')
    inlines = [CartItemInline]

    fieldsets = (
        ('اطلاعات مشتری', {
            'fields': (
                ('first_name', 'last_name'),
                ('phone', 'postal_code'),
                'address',
                'description'
            )
        }),
        ('اطلاعات پرداخت', {
            'fields': (
                'user',
                'is_paid',
                'payment_date',
                'payment_ref_id',
                'payment_status',
                'payment_authority'
            )
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else "-"
    full_name.short_description = 'نام کامل'
