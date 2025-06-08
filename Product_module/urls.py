from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('all/', views.AllProductsListView.as_view(), name='all-products'),
    path('category/<str:category>/', views.ProductListView.as_view(), name='product-list-by-category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail')
]
