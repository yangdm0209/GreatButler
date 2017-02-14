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
from web import views, web_purchase
from custom import views as customapi
from product import views as productapi

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
    url(r'^purchase/list/$', customapi.get_provider),

    # 销售相关

    # 仓库相关

    # 资金相关

    # 资料相关
]
