from django.urls import path
from .views import scrape_brand_products
from .views import scrape_brand_view, scrape_brand_page


urlpatterns = [
    path('scrape/<str:brand_name>/', scrape_brand_products, name='scrape-brand-products'),
    path('scrape/', scrape_brand_view, name='scrape-brand'),
    path('scrape-brand/', scrape_brand_page, name='scrape-brand-page'),
]