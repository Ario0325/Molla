from django.contrib import admin
from .models import Product, ProductCategory, ProductSize, ProductColor, ProductGallery


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_percent', 'discounted_price', 'stock', 'get_categories', 'is_active']
    list_editable = ['is_active', 'stock', 'discount_percent']
    list_filter = ['category', 'is_active', 'is_special', 'is_new', 'discount_percent']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductGalleryInline]
    readonly_fields = ['discounted_price']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'category', 'description', 'short_description')
        }),
        ('قیمت و تخفیف', {
            'fields': ('price', 'discount_percent', 'discounted_price', 'old_price', 'stock')
        }),
        ('تصاویر و گالری', {
            'fields': ('image',)
        }),
        ('ویژگی‌ها', {
            'fields': ('sizes', 'colors', 'features', 'shipping_info')
        }),
        ('وضعیت', {
            'fields': ('is_active', 'is_special', 'is_new')
        }),
    )

    def get_categories(self, obj):
        return ", ".join([category.title for category in obj.category.all()])

    get_categories.short_description = 'دسته بندی‌ها'

    def save_model(self, request, obj, form, change):
        # The discount calculation is handled in the model's save method
        super().save_model(request, obj, form, change)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {'url_title': ('title',)}


admin.site.register(ProductSize)
admin.site.register(ProductColor)
