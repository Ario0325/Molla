from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Article
from Category_Article_Module.models import ArticleCategory
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='dispatch')
class ArticleListView(ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    paginate_by = 4

    def get_queryset(self):
        queryset = Article.objects.filter(
            is_active=True,
            status='published'
        ).select_related('author').prefetch_related('category').order_by('-created_at')

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__url_title=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.filter(
            is_active=True
        ).annotate(articles_count=Count('articles'))

        if 'category' in self.request.GET:
            context['category_param'] = f"category={self.request.GET['category']}&"
        else:
            context['category_param'] = ""

        return context


class ArticleDetailView(DetailView):
    template_name = 'ArticleModule/article_detail.html'
    model = Article
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_article = self.get_object()

        related_articles = Article.objects.filter(
            category__in=current_article.category.all(),
            is_active=True
        ).exclude(id=current_article.id).distinct()[:4]

        previous_article = Article.objects.filter(
            id__lt=current_article.id,
            is_active=True
        ).order_by('-id').first()

        next_article = Article.objects.filter(
            id__gt=current_article.id,
            is_active=True
        ).order_by('id').first()

        context.update({
            'related_articles': related_articles,
            'previous_article': previous_article,
            'next_article': next_article
        })

        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ArticleCategoryListView(ListView):
    template_name = 'Category_Article_Module/category_list.html'
    model = ArticleCategory
    context_object_name = 'categories'

    def get_queryset(self):
        return ArticleCategory.objects.filter(
            is_active=True,
            parent=None
        ).prefetch_related('articles')
