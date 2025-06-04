from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Home_module.urls')),
    path('category/', include('Category_Module.urls')),
    path('articles/', include('ArticleModule.urls')),
    path('article-categories/', include('Category_Article_Module.urls', namespace='article_categories')),  # تغییر نام namespace
    path('about-us/', include('AboutUs_module.urls')),
    path('contact-us/', include("ContactUs_module.urls")),
    path('admin/', admin.site.urls),
    path('account/', include('Account_modules.urls')),
    path('article-categories/', include('Category_Article_Module.urls')),
    path('products/', include('Product_module.urls')),
    path('cart/', include('Cart_module.urls', namespace='cart')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
