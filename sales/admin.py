#!/usr/bin/env python
# coding: utf-8


from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from sales.models import Sales, SalesDetail, SalesPay


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['custom', 'stock', 'created_at', 'detail_table', 'pay_status']
    fields = ['custom', 'stock', 'detail', 'pay_status']
    list_filter = ['created_at', 'pay_status']

    def detail_table(self, obj):
        html = '''
        <table class="table table-bordered">
            <caption style="font-size:18px; text-align:center;"><strong>货品清单</strong></caption>
            <thead>
            <tr>
                <th>名称</th>
                <th>数量</th>
                <th>单价</th>
                <th>折扣</th>
            </tr>
            </thead>
            <tbody>
        '''
        for pro in obj.detail.all():
            html += '<tr><td><a href="/admin/product/product/%s/">%s</a></td><td>%s</td><td>%s</td><td>%s%%</td></tr>' % (
                pro.product.id, pro.product, pro.num, pro.price, int(pro.scale * 100))

        html += '</tbody></table>'
        html += '''<div>
                    <div class="col-sm-4"><strong>合计品项：&nbsp;</strong><span id="totalPros">%s</span>项</div>
                    <div class="col-sm-4"><strong>合计数目：&nbsp;</strong><span id="totalNums">%s</span>只</div>
                    <div class="col-sm-4"><strong>合计金额：&nbsp;</strong>￥<span id="totalPrice">%s</span></div>
                </div>''' % (obj.total_products, obj.total_nums, obj.total_prices)
        return mark_safe(html)

    detail_table.short_description = '详情'


@admin.register(SalesDetail)
class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'num', 'price', 'scale']
    fields = ['product', 'num', 'price', 'scale']


@admin.register(SalesPay)
class SalesPayAdmin(admin.ModelAdmin):
    list_display = ['sales', 'method', 'created_at']
    fields = ['sales', 'method']
    list_filter = ['method', 'created_at']
