from django.views.generic import TemplateView
from Product_module.models import Product, ProductCategory

class HomeView(TemplateView):
    template_name = 'Home_module/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True, is_delete=False)
        context['products'] = Product.objects.filter(is_active=True, is_delete=False)[:10]
        context['special_products'] = Product.objects.filter(is_active=True, is_delete=False, is_special=True)[:5]
        return context