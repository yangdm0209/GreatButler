from django.contrib import admin


# Register your models here.
from stock.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'belong']
    field = ['name', 'belong', 'nums']
    list_display_links = ['name']
    search_fields = ['name']
