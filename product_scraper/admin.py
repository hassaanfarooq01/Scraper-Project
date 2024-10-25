from django.contrib import admin
from .models import Brand, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'scraping_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('scraping_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'asin', 'brand', 'created_at', 'updated_at')
    search_fields = ('name', 'asin')
    list_filter = ('brand',)
    date_hierarchy = 'created_at'
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(brand__name__icontains=search_term)
        return queryset, use_distinct