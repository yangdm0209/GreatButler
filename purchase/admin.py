from django.contrib import admin

# Register your models here.
from purchase.models import Purchase, PurchaseDetail, PurchaseDetailShip


#
#
# class PurchaseDetailShipInline(admin.TabularInline):
#     model = PurchaseDetailShip
#     extra = 1  # how many rows to show
#
#
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    # inlines = (PurchaseDetailShipInline,)
    list_display = ['provider', 'stock', 'created_at']
    fields = ['provider', 'stock']


@admin.register(PurchaseDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'num', 'price']
    fields = ['product', 'num', 'price']
