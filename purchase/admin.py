#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from purchase.models import Purchase, PurchaseDetail


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    # inlines = (PurchaseDetailShipInline,)
    list_display = ['provider', 'stock', 'created_at', 'detail_table']
    readonly_fields = ['provider', 'stock', 'detail']
    list_filter = ['created_at']

    def detail_list(self, obj):
        pro_list = []
        sum = 0
        for pro in obj.detail.all():
            pro_list.append('<li><a href="/admin/product/product/%s/">%s</a>: %s只 x %s = %s</li>' % (
                pro.product.id, pro.product, pro.num, pro.price, pro.num * pro.price))
            sum += pro.num * pro.price
        if len(pro_list) > 0:
            pros = ''.join(pro_list)
            return mark_safe('商品总数: <b>%s</b>   总价值： <b>%s</b> <br/><ul class="list-unstyled">%s</ul>' % (
                len(pro_list), sum, pros))
        else:
            return mark_safe('<span class="text-warning">还没有学生</span>')

    def detail_table(self, obj):
        html = '''
        <table class="table table-bordered">
            <caption style="font-size:18px; text-align:center;"><strong>货品清单</strong></caption>
            <thead>
            <tr>
                <th>名称</th>
                <th>数量</th>
                <th>单价</th>
            </tr>
            </thead>
            <tbody>
        '''
        for pro in obj.detail.all():
            html += '<tr><td><a href="/admin/product/product/%s/">%s</a></td><td>%s</td><td>%s</td></tr>' % (
                pro.product.id, pro.product, pro.num, pro.price)
        html += '</tbody></table>'
        html += '''<div>
                    <div class="col-sm-4"><strong>合计品项：&nbsp;</strong><span id="totalPros">%s</span>项</div>
                    <div class="col-sm-4"><strong>合计数目：&nbsp;</strong><span id="totalNums">%s</span>只</div>
                    <div class="col-sm-4"><strong>合计金额：&nbsp;</strong>￥<span id="totalPrice">%s</span></div>
                </div>''' % (obj.total_products, obj.total_nums, obj.total_prices)
        return mark_safe(html)

    detail_list.short_description = '详情'
    detail_table.short_description = '详情'


@admin.register(PurchaseDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'num', 'price', 'purchase_id']
    readonly_fields = ['product', 'num', 'price']

    def purchase_id(self, obj):
        purchase = ''
        for p in obj.purchase.all():
            purchase += '<a href="/admin/purchase/purchase/%d">purchase-%d</a>' % (p.id, p.id)
        return mark_safe(purchase)
