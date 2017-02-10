#!/usr/bin/env python
# coding: utf-8

from django.db import models

from custom.models import Custom
from  product.models import Product


# Create your models here.


class PurchaseDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name="采购产品")
    num = models.IntegerField(verbose_name="采购数量")

    def __unicode__(self):
        return '%s(%d)' % (self.product.name, self.num)

    class Meta:
        verbose_name_plural = "采购详情"
        verbose_name = "采购详情"


class Purchase(models.Model):
    custom = models.ForeignKey(Custom, verbose_name="供应商")
    items = models.ManyToManyField(PurchaseDetail, verbose_name="产品", through='PurchaseDetailShip')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __unicode__(self):
        return u'%s 订单-%d' % (self.custom, self.id)

    class Meta:
        verbose_name_plural = "采购"
        verbose_name = "采购"


class PurchaseDetailShip(models.Model):
    purchase = models.ForeignKey(Purchase, verbose_name="采购产品")
    detail = models.ForeignKey(PurchaseDetail, verbose_name="详情")

    def __unicode__(self):
        return u'%s 详情' % self.purchase

    class Meta:
        verbose_name_plural = "采购详情"
        verbose_name = "采购详情"
