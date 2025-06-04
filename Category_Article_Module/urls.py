from django.urls import path
from . import views

app_name = 'article_category'

urlpatterns = [
    path('', views.ArticleCategoryListView.as_view(), name='category-list'),
    path('<str:url_title>', views.ArticleCategoryDetailView.as_view(), name='category-detail'),
]
