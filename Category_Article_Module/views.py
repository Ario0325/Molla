from django.views.generic import ListView, DetailView
from .models import ArticleCategory
from ArticleModule.models import Article
from django.core.cache import cache

class ArticleCategoryListView(ListView):
    template_name = 'Category_Article_Module/category_list.html'
    model = ArticleCategory
    context_object_name = 'categories'

    def get_queryset(self):
        return ArticleCategory.objects.filter(is_active=True, parent=None)\
            .prefetch_related('articles')

class ArticleCategoryDetailView(DetailView):
    template_name = 'Category_Article_Module/category_detail.html'
    model = ArticleCategory
    context_object_name = 'category'
    slug_field = 'url_title'
    slug_url_kwarg = 'url_title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = f'category_articles_{self.object.id}'
        articles = cache.get(cache_key)

        if not articles:
            articles = Article.objects.filter(
                is_active=True,
                category=self.object
            ).select_related('author')\
            .prefetch_related('category')\
            .order_by('-created_at')
            cache.set(cache_key, articles, 60*15)

        context['articles'] = articles
        return context
