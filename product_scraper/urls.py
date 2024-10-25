from django.urls import path
from .views import scrape_brand_view


urlpatterns = [
    path('scrape/', scrape_brand_view, name='scrape-brand'),
]