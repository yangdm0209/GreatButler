from django.contrib import admin

# Register your models here.
from custom.models import Custom


@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'tel', 'addr', 'other']
    list_display_links = ['name']
    fields = ['name', 'type', 'tel', 'addr', 'other']
    search_fields = ['name', 'addr']
