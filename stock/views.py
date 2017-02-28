#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render

# Create your views here.
from purchase.models import Purchase
from sales.models import Refunds, Sales
from stock.models import Allocate


def update_stock_list(stock, product, num):
    for item in stock:
        if item['id'] == product.id:
            item['num'] += num
            return
    stock.append({'id': product.id, 'name': product.name, 'num': num, 'min': product.min_stock})


def calc_stock(sid):
    stock = []
    # 添加所有的采购
    ps = Purchase.objects.filter(stock=sid)
    for p in ps:
        for detail in p.detail.all():
            update_stock_list(stock, detail.product, detail.num)
    # 添加所有调拨入
    al = Allocate.objects.filter(dest_stock=sid)
    for a in al:
        for detail in a.nums.all():
            update_stock_list(stock, detail.product, detail.num)
    # 添加所有退货
    re = Refunds.objects.filter(stock=sid)
    for r in re:
        for detail in r.detail.all():
            update_stock_list(stock, detail.product, detail.num)
    # 减去所有调拨出
    src_al = Allocate.objects.filter(source_stock=sid)
    for a in src_al:
        for detail in a.nums.all():
            update_stock_list(stock, detail.product, detail.num * -1)
    # 减去所有销售
    sal = Sales.objects.filter(stock=sid)
    for s in sal:
        for detail in s.detail.all():
            update_stock_list(stock, detail.product, detail.num * -1)
    return sorted(stock, key=lambda st: st['name'])


def add_stock_detail(stock, product, num, type, date):
    stock.append({'name': product.name, 'num': num, 'type': type, 'date': date})


def detail_stock(sid):
    stock = []
    # 添加所有的采购
    ps = Purchase.objects.filter(stock=sid)
    for p in ps:
        for detail in p.detail.all():
            add_stock_detail(stock, detail.product, detail.num, '采购', p.created_at)
    # 添加所有调拨入
    al = Allocate.objects.filter(dest_stock=sid)
    for a in al:
        for detail in a.nums.all():
            add_stock_detail(stock, detail.product, detail.num, '调拨入库', a.created_at)
    # 添加所有退货
    re = Refunds.objects.filter(stock=sid)
    for r in re:
        for detail in r.detail.all():
            add_stock_detail(stock, detail.product, detail.num, '退货', r.created_at)
    # 减去所有调拨出
    src_al = Allocate.objects.filter(source_stock=sid)
    for a in src_al:
        for detail in a.nums.all():
            add_stock_detail(stock, detail.product, detail.num, '调拨出库', a.created_at)
    # 减去所有销售
    sal = Sales.objects.filter(stock=sid)
    for s in sal:
        for detail in s.detail.all():
            add_stock_detail(stock, detail.product, detail.num, '销售', s.created_at)
    return sorted(stock, key=lambda st: st['date'])
