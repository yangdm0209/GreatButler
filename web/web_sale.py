#!/usr/bin/env python
# coding: utf-8

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from custom.custom_tool import get_customs
from stock.stock_tool import get_stocks


@login_required
def sale(request):
    return render_to_response('sale/main.html', RequestContext(request, {'sale_active': 1}))


@login_required
def new(request):
    if request.method == 'GET':
        return render_to_response('sale/new.html', RequestContext(request, {'sale_active': 1,
                                                                            'customs': get_customs(),
                                                                            'stocks': get_stocks()}))
    else:
        pass


@login_required
def refunds(request):
    return render_to_response('sale/refunds.html', RequestContext(request, {'sale_active': 1}))
