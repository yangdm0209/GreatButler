from django.contrib import admin

# Register your models here.
from purchase.models import Purchase, PurchaseDetail, PurchaseDetailShip


class PurchaseDetailShipInline(admin.TabularInline):
    model = PurchaseDetailShip
    extra = 1  # how many rows to show


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = (PurchaseDetailShipInline,)
    list_display = ['custom', 'created_at']
    fields = ['custom']


@admin.register(PurchaseDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'num']
    fields = ['product', 'num']
