#!/usr/bin/env python
# coding: utf-8

from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from stock.models import ProductNum, Stock


@admin.register(ProductNum)
class ProductNumAdmin(admin.ModelAdmin):
    list_display = ['product', 'num', 'belong_stock']

    def belong_stock(self, obj):
        stock = ''
        for s in obj.stock.all():
            stock += s.name
        return mark_safe(stock)

    belong_stock.short_description = '所属仓库'


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'belong', 'detail_table']
    field = ['name', 'belong', 'nums']
    list_display_links = ['name']
    search_fields = ['name']

    def detail_table(self, obj):
        html = '''
        <table class="table table-bordered">
            <caption style="font-size:18px; text-align:center;"><strong>库存清单</strong></caption>
            <thead>
            <tr>
                <th>名称</th>
                <th>数量</th>
            </tr>
            </thead>
            <tbody>
        '''
        for pro in obj.nums.all():
            html += '<tr><td><a href="/admin/product/product/%s/">%s</a></td><td>%s</td></tr>' % (
                pro.product.id, pro.product, pro.num)
        html += '</tbody></table>'
        html += '''<div>
                    <div class="col-sm-4"><strong>合计品项：&nbsp;</strong><span id="totalPros">%s</span>项</div>
                    <div class="col-sm-4"><strong>合计数目：&nbsp;</strong><span id="totalNums">%s</span>只</div>
                </div>''' % (obj.total_products, obj.total_nums)
        return mark_safe(html)

    detail_table.short_description = '详情'
