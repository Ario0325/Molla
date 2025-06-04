from Category_Article_Module.models import ArticleCategory

def article_categories(request):
    return {
        'article_categories': ArticleCategory.objects.all()
    }
