#!/usr/bin/env python
# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext


def purchase(request):
    return render_to_response('purchase/main.html', RequestContext(request))


def new(request):
    if request.method == 'GET':
        return render_to_response('purchase/new.html', RequestContext(request))


def refunds(request):
    return render_to_response('purchase/refunds.html', RequestContext(request))
