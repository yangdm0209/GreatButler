from django.contrib import admin

# Register your models here.
from custom.models import Custom


@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'area', 'contacts', 'tel', 'addr', 'other', 'created_at']
    list_display_links = ['name']
    fields = ['name', 'type', 'area', 'contacts', 'tel', 'addr', 'other']
    search_fields = ['name', 'addr', 'tel', 'contacts']
    list_filter = ['type', 'area', 'created_at']

    def has_add_permission(self, request):
        print request.user
        return admin.ModelAdmin.has_add_permission(self, request)
