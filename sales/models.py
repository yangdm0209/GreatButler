#!/usr/bin/env python
# coding: utf-8


from django.db import models

# Create your models here.
from custom.models import Custom
from product.models import Product
from stock.models import Stock


class SalesDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name="销售产品")
    num = models.IntegerField(verbose_name="销售数量")
    price = models.FloatField(verbose_name="销售价格")
    scale = models.FloatField(verbose_name="折扣率", default=1)

    def __unicode__(self):
        return self.product

    class Meta:
        verbose_name_plural = "销售详情"
        verbose_name = "销售详情"


class Sales(models.Model):
    PAY_STS = (
        (0, '未支付'), (1, '已支付')
    )
    custom = models.ForeignKey(Custom, verbose_name="客户")
    stock = models.ForeignKey(Stock, verbose_name="仓库")
    detail = models.ManyToManyField(SalesDetail, verbose_name="产品")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    total_products = models.IntegerField(verbose_name="合计品项")
    total_nums = models.IntegerField(verbose_name="合计数目")
    total_prices = models.FloatField(verbose_name="合计金额")
    pay_status = models.IntegerField(verbose_name="支付状态", choices=PAY_STS, default=0)

    def __unicode__(self):
        return u'%s 订单-%s' % (self.custom, self.id)

    class Meta:
        verbose_name_plural = "销售"
        verbose_name = "销售"


class SalesPay(models.Model):
    PAY_METHOD = (
        (0, '现金'), (1, '微信'), (2, '支付宝'), (3, '其他'),
    )
    sales = models.ForeignKey(Sales, verbose_name="订单")
    method = models.IntegerField(verbose_name="支付方式", choices=PAY_METHOD, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='支付时间')

    class Meta:
        verbose_name_plural = "订单支付"
        verbose_name = "订单支付"
