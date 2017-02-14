#!/usr/bin/env python
# coding: utf-8
from stock.models import Stock


def get_stocks():
    stocks=[]
    for s in Stock.objects.all():
        stocks.append(s)
    return stocks