from django.urls import path
from .views import ContactUsViews


urlpatterns = [
    path('', ContactUsViews.as_view(), name='Contact-us')
]