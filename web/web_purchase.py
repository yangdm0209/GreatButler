#!/usr/bin/env python
# coding: utf-8
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_exempt

from custom.custom_tool import get_providers
from custom.models import Provider
from product.models import Product
from purchase.models import Purchase, PurchaseDetail
from stock.models import Stock
from stock.stock_tool import get_stocks
from utils.response import failed_response, success_response


@login_required
def purchase(request):
    return render_to_response('purchase/main.html', RequestContext(request, {'purchase_active': 1}))


@csrf_exempt
@login_required
def new(request):
    if request.method == 'GET':
        return render_to_response('purchase/new.html',
                                  RequestContext(request, {'purchase_active': 1,
                                                           'providers': get_providers(),
                                                           'stocks': get_stocks()}))
    else:
        data = request.POST.get('data')
        if not data:
            return failed_response('参数错误')
        else:
            all = json.loads(data)
            p = Purchase()
            p.provider = Provider.objects.get(id=all['supporter'])
            p.stock = Stock.objects.get(id=all['stock'])
            p.save()
            for item in all['detail']:
                pro = PurchaseDetail()
                pro.product = Product.objects.get(id=item['pid'])
                pro.num = int(item['pnum'])
                pro.price = float(item['pprice'])
                pro.save()
                p.detail.add(pro)
            p.save()
            return success_response('添加成功')


@login_required
def refunds(request):
    return render_to_response('purchase/refunds.html', RequestContext(request, {'purchase_active': 1}))


@login_required
def today_purchase(request):
    start = now().date()
    end = start + timedelta(days=1)
    purchases = Purchase.objects.all().filter(created_at__range=(start, end)).order_by('-id')
    return render_to_response('purchase/list.html',
                              RequestContext(request, {'purchase_active': 1, 'purchases': purchases, 'havelist': len(purchases)}))


@login_required
def all_purchase(request):
    purchases = Purchase.objects.all().order_by('-id')
    return render_to_response('purchase/list.html',
                              RequestContext(request, {'purchase_active': 1, 'purchases': purchases, 'havelist': len(purchases)}))
