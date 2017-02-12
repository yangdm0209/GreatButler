from django.contrib import admin

# Register your models here.
from product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_cost', 'price_wholesale', 'price_retail', 'specification', 'created_at']
    list_display_links = ['name']
    fields = ['name', 'price_cost', 'price_wholesale', 'price_retail', 'specification', 'other']
    search_fields = ['name']
    list_filter = ['created_at']
