#!/usr/bin/env python
# coding: utf-8

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from custom.custom_tool import get_customs
from custom.models import Custom
from product.models import Product
from sales.models import Sales, SalesDetail
from stock.models import Stock
from stock.stock_tool import get_stocks
from utils.response import failed_response, success_response


@login_required
def sale(request):
    return render_to_response('sale/main.html', RequestContext(request, {'sale_active': 1}))


@csrf_exempt
@login_required
def new(request):
    if request.method == 'GET':
        return render_to_response('sale/new.html', RequestContext(request, {'sale_active': 1,
                                                                            'customs': get_customs(),
                                                                            'stocks': get_stocks()}))
    else:
        data = request.POST.get('data')
        print data
        if not data:
            return failed_response('参数错误')
        else:
            all = json.loads(data)
            s = Sales()
            s.custom = Custom.objects.get(id=all['custom'])
            s.stock = Stock.objects.get(id=all['stock'])
            s.total_products = 0
            s.total_nums = 0
            s.total_prices = 0
            s.save()
            for item in all['detail']:
                pro = SalesDetail()
                pro.product = Product.objects.get(id=item['pid'])
                pro.num = int(item['pnum'])
                pro.price = float(item['pprice'])
                pro.scale = float(item['pscale'])
                pro.save()
                s.total_products += 1
                s.total_nums += pro.num
                s.total_prices += pro.num * pro.price * pro.scale
                s.detail.add(pro)
            s.save()
            return success_response('添加成功')


@login_required
def refunds(request):
    return render_to_response('sale/refunds.html', RequestContext(request, {'sale_active': 1}))
