#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import datetime
import django
from django.utils.timezone import make_aware

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRO_ABSPATH = os.path.abspath(os.path.join(BASE_DIR, '../'))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, PRO_ABSPATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greatButler.settings")
django.setup()

from purchase.models import Purchase, PurchaseDetail
from sales.models import Sales, SalesDetail, Refunds


def out_all():
    with open('out2.csv', 'wb') as fout:
        for item in Purchase.objects.all():
            for detail in item.detail.all():
                line = u'%s, %s, %s, %s, %s, %s\n' % (
                    u'采购', item.provider.name, detail.product.name, detail.product.price_cost, detail.num, item.date)
                fout.write(line.encode('utf-8'))
        for item in Sales.objects.all():
            for detail in item.detail.all():
                line = u'%s, %s, %s, %s, %s, %s, %s, %s\n' % (
                    u'销售', item.custom.name, detail.product.name, detail.product.price_cost, detail.num * -1, item.date,
                    item.stock.name, item.pay_status)
                fout.write(line.encode('utf-8'))
        for item in Refunds.objects.all():
            for detail in item.detail.all():
                line = u'%s, %s, %s, %s, %s, %s, %s\n' % (
                    u'退货', item.custom.name, detail.product.name, detail.product.price_cost, detail.num, item.date, item.stock.name)
                fout.write(line.encode('utf-8'))


#
# #把字符串转成datetime
# def string_toDatetime(string):
#     return datetime.strptime(string, "%Y-%m-%d %H")

def out_month():
    nums={}
    for item in Sales.objects.all().filter(created_at__gte=make_aware(datetime.datetime(2017, 3, 1))):
        for detail in item.detail.all():
            line = u'%s, %s, %s, %s, %s, %s, %s\n' % (
                u'销售', item.custom.name, detail.product.name, detail.product.price_cost, detail.num * -1, item.date,
                item.pay_status)
            if detail.product.name not in nums:
                nums[detail.product.name] = detail.num
            else:
                nums[detail.product.name] += detail.num
    for key in nums:
        print key, nums[key]

out_all()
