#!/usr/bin/env python
# coding: utf-8

"""greatButler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from web import views, web_purchase, web_stock
from custom import views as customapi
from product import views as productapi
from web import web_sale

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/logout/$', views.logout),

    # 产品相关
    url(r'^product/list/$', productapi.get_products),

    # 采购相关
    url(r'^purchase/$', web_purchase.purchase),
    url(r'^purchase/new/$', web_purchase.new),
    url(r'^purchase/refunds/$', web_purchase.refunds),
    url(r'^purchase/today/list/$', web_purchase.today_purchase),
    url(r'^purchase/list/$', web_purchase.all_purchase),

    # 销售相关
    url(r'^sale/$', web_sale.sale),
    url(r'^sale/new/$', web_sale.new),
    url(r'^sale/refunds/$', web_sale.refunds),
    url(r'^sale/today/list/$', web_sale.today_sales),
    url(r'^sale/list/$', web_sale.all_sales),
    url(r'^sale/pay/$', web_sale.pay_sales),

    # 仓库相关
    url(r'^stock/$', web_stock.stock),
    url(r'^stock/allocate/$', web_stock.allocate),
    url(r'^stock/list/$', web_stock.list),
    url(r'^stock/all/list/$', web_stock.all_list),

    # 资金相关

    # 资料相关
]
