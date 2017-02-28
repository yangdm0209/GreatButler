#!/usr/bin/env python
# coding: utf-8
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from product.models import Product
from stock.models import Stock, Allocate, AllocateNum, ProductNum
from stock.views import calc_stock, detail_stock
from utils.response import failed_response, success_response


@login_required
def stock(request):
    return render_to_response('stock/main.html', RequestContext(request, {'stock_active': 1}))


@csrf_exempt
# @login_required
def allocate(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        return render_to_response('stock/allocate.html', RequestContext(request, {'stock_active': 1, 'stocks': stocks}))
    else:
        data = request.POST.get('data')
        if not data:
            return failed_response('参数错误')
        else:
            all = json.loads(data)
            al = Allocate()
            al.source_stock = Stock.objects.get(id=all['source_stock'])
            al.dest_stock = Stock.objects.get(id=all['dest_stock'])
            al.save()
            for item in all['detail']:
                pro = AllocateNum()
                pro.product = Product.objects.get(id=item['pid'])
                pro.num = int(item['pnum'])
                pro.save()
                al.nums.add(pro)
            al.save()
            return success_response('调拨成功')


@login_required
def list(request):
    ss = []
    stocks = Stock.objects.all()
    for s in stocks:
        ss.append({'name': s.name, 'pros': detail_stock(s.id)})
    return render_to_response('stock/detail.html',
                              RequestContext(request, {'stock_active': 1, 'stocks': ss, 'today': now().date()}))


@login_required
def all_list(request):
    ss = []
    stocks = Stock.objects.all()
    for s in stocks:
        ss.append({'name': s.name, 'pros': calc_stock(s.id)})
    return render_to_response('stock/list.html',
                              RequestContext(request, {'stock_active': 1, 'stocks': ss, 'today': now().date()}))
