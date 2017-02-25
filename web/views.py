#!/usr/bin/env python
# coding: utf-8
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.utils.timezone import now, timedelta

from product.models import Product
from purchase.models import Purchase
from sales.models import Sales, SalesPay
from django.db.models import Sum

from stock.models import ProductNum


def stock_warns():
    cnt = 0
    prs = Product.objects.all()
    for item in prs:
        procnt = ProductNum.objects.filter(product=item.id).aggregate(procnt=Sum('num'))
        if not procnt['procnt'] or procnt['procnt'] < item.min_stock:
            # print item.name, procnt['procnt']
            cnt += 1
    return cnt


@login_required
def index(request):
    start = now().date()
    end = start + timedelta(days=1)
    purchases = Purchase.objects.all().filter(created_at__range=(start, end)).count()
    sales = Sales.objects.all().filter(created_at__range=(start, end)).count()
    pays = SalesPay.objects.all().filter(created_at__range=(start, end)).count()
    warns = stock_warns()
    return render_to_response('index.html',
                              RequestContext(request,
                                             {'purchases': purchases, 'sales': sales, 'pays': pays, 'warns': warns}))


def login(request):
    if request.method == 'GET':
        return render_to_response('account/login.html', RequestContext(request))
    else:
        username = request.POST.get('user', '')
        password = request.POST.get('password', '')
        next = request.GET.get('next', '/')
        if not username or not password:
            return render_to_response('account/login.html', RequestContext(request, {'error': '请输入用户名和密码'}))
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            request.session.set_expiry(0)  # 用户关闭浏览器session就会失效
            return HttpResponseRedirect(next)
        else:
            return render_to_response('account/login.html', RequestContext(request, {'error': '用户名密码错误'}))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')
