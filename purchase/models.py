#!/usr/bin/env python
# coding: utf-8

from django.db import models

from custom.models import Provider
from  product.models import Product

# Create your models here.
from stock.models import Stock


class PurchaseDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name="采购产品")
    num = models.IntegerField(verbose_name="采购数量")
    price = models.FloatField(verbose_name="采购价格")

    def __unicode__(self):
        return u'%s*%s只' % (self.product.name, self.num)

    class Meta:
        verbose_name_plural = "采购详情"
        verbose_name = "采购详情"


class Purchase(models.Model):
    provider = models.ForeignKey(Provider, verbose_name="供应商")
    stock = models.ForeignKey(Stock, verbose_name="仓库")
    detail = models.ManyToManyField(PurchaseDetail, verbose_name="产品")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __unicode__(self):
        return u'%s的订单-%s' % (self.provider, self.date)

    @property
    def date(self):
        return self.created_at.date()

    @property
    def total_products(self):
        return self.detail.all().count()

    @property
    def total_nums(self):
        total = 0
        for item in self.detail.all():
            total += item.num
        return total

    @property
    def total_prices(self):
        total = 0
        for item in self.detail.all():
            total += item.num * item.price
        return total

    class Meta:
        verbose_name_plural = "采购"
        verbose_name = "采购"

# class PurchaseDetailShip(models.Model):
#     purchase = models.ForeignKey(Purchase, verbose_name="采购产品")
#     detail = models.ForeignKey(PurchaseDetail, verbose_name="详情")
#
#     def __unicode__(self):
#         return u'%s 详情' % self.purchase
#
#     class Meta:
#         verbose_name_plural = "采购详情"
#         verbose_name = "采购详情"
