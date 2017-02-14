from django.contrib import admin

# Register your models here.
from custom.models import Custom, Area, CustomType, Saler, Provider


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name']


@admin.register(CustomType)
class CustomTypeAdmin(admin.ModelAdmin):
    list_display = ['alias', 'name']
    fields = ['alias', 'name']


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


@admin.register(Saler)
class SalerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tel', 'addr', 'other', 'created_at']
    list_display_links = ['name']
    fields = ['name', 'tel', 'addr', 'other']
    search_fields = ['name', 'addr', 'tel']
    list_filter = ['created_at']

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'tel', 'addr', 'other', 'created_at']
    list_display_links = ['name']
    fields = ['name', 'tel', 'addr', 'other']
    search_fields = ['name', 'addr', 'tel']
    list_filter = ['created_at']
