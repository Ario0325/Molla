from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Product, ProductCategory, ProductGallery
from sorl.thumbnail import get_thumbnail

class ProductListView(ListView):
    template_name = 'Product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = Product.objects.filter(is_active=True, is_delete=False)
        category_name = self.kwargs.get('category')
        if category_name:
            query = query.filter(category__url_title=category_name).distinct()
        return query

class AllProductsListView(ListView):
    template_name = 'Product_module/all_products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_delete=False).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = self.get_queryset().count()
        context['categories'] = ProductCategory.objects.filter(is_active=True, is_delete=False)
        return context

class ProductDetailView(DetailView):
    template_name = 'Product_module/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_delete=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_categories = self.object.category.all()
        if product_categories.exists():
            context['related_products'] = Product.objects.filter(
                category__in=product_categories,
                is_active=True,
                is_delete=False
            ).exclude(id=self.object.id).distinct()[:4]
        else:
            context['related_products'] = Product.objects.none()
        context['gallery_images'] = ProductGallery.objects.filter(product=self.object)
        return context
