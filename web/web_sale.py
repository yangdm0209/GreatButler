#!/usr/bin/env python
# coding: utf-8

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import csrf_exempt

from custom.custom_tool import get_customs
from custom.models import Custom
from product.models import Product
from sales.models import Sales, SalesDetail, SalesPay, Refunds
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
            s.save()
            for item in all['detail']:
                pro = SalesDetail()
                pro.product = Product.objects.get(id=item['pid'])
                pro.num = int(item['pnum'])
                pro.price = float(item['pprice'])
                pro.scale = float(item['pscale'])
                pro.save()
                s.detail.add(pro)
            s.save()
            return success_response('添加成功')


@login_required
def refunds(request):
    if request.method == 'GET':
        return render_to_response('sale/refunds.html', RequestContext(request, {'sale_active': 1,
                                                                            'customs': get_customs(),
                                                                            'stocks': get_stocks()}))
    else:
        data = request.POST.get('data')
        print data
        if not data:
            return failed_response('参数错误')
        else:
            all = json.loads(data)
            r = Refunds()
            r.custom = Custom.objects.get(id=all['custom'])
            r.stock = Stock.objects.get(id=all['stock'])
            r.save()
            for item in all['detail']:
                pro = SalesDetail()
                pro.product = Product.objects.get(id=item['pid'])
                pro.num = int(item['pnum'])
                pro.price = float(item['pprice'])
                pro.scale = float(item['pscale'])
                pro.save()
                r.detail.add(pro)
            r.save()
            return success_response('添加成功')


@login_required
def today_sales(request):
    start = now().date()
    end = start + timedelta(days=1)
    sales = Sales.objects.all().filter(created_at__range=(start, end)).order_by('-id')
    return render_to_response('sale/list.html',
                              RequestContext(request, {'sale_active': 1, 'sales': sales, 'havelist': len(sales)}))


@login_required
def all_sales(request):
    sales = Sales.objects.all().order_by('-id')
    return render_to_response('sale/list.html', RequestContext(request, {'sale_active': 1, 'sales': sales, 'havelist': len(sales)}))


@login_required
def pay_sales(request):
    if request.method == 'GET':
        sales = Sales.objects.all().filter(pay_status=0)
        return render_to_response('sale/pay.html',
                                  RequestContext(request, {'sale_active': 1, 'sales': sales, 'unpay': len(sales)}))
    else:
        payid = request.POST.get('payid', '')
        method = request.POST.get('method', '')
        error = ''
        success = ''
        if not payid:
            error = '参数错误'
        else:
            sal = Sales.objects.get(id=payid)
            if not sal:
                error = "订单不存在"
            else:
                sp = SalesPay()
                sp.sales = sal
                sp.method = method
                sp.save()
                success = "付款成功"
        sales = Sales.objects.all().filter(pay_status=0)
        return render_to_response('sale/pay.html',
                                  RequestContext(request, {'sale_active': 1, 'sales': sales, 'unpay': len(sales),
                                                           'error': error, 'success': success}))
