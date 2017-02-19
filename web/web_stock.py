#!/usr/bin/env python
# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
def stock(request):
    return render_to_response('stock/main.html', RequestContext(request, {'stock_active': 1}))


@login_required
def allocate(request):
    return render_to_response('stock/allocate.html', RequestContext(request, {'stock_active': 1}))
