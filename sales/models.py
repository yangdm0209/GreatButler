#!/usr/bin/env python
# coding: utf-8


from django.db import models

# Create your models here.
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from custom.models import Custom
from product.models import Product
from stock.models import Stock


class SalesDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name="销售产品")
    num = models.IntegerField(verbose_name="销售数量")
    price = models.FloatField(verbose_name="销售价格")
    scale = models.FloatField(verbose_name="折扣率", default=1)

    def __unicode__(self):
        return u'%s*%s只' % (self.product.name, self.num)

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
    pay_status = models.IntegerField(verbose_name="支付状态", choices=PAY_STS, default=0)

    def __unicode__(self):
        return u'%s的订单-%s' % (self.custom, self.date)

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
            total += item.num * item.price * item.scale
        return total

    class Meta:
        verbose_name_plural = "销售"
        verbose_name = "销售"


class Refunds(models.Model):
    custom = models.ForeignKey(Custom, verbose_name="客户")
    stock = models.ForeignKey(Stock, verbose_name="仓库")
    detail = models.ManyToManyField(SalesDetail, verbose_name="产品")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __unicode__(self):
        return u'%s的退货-%s' % (self.custom, self.date)

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
            total += item.num * item.price * item.scale
        return total

    class Meta:
        verbose_name_plural = "退货"
        verbose_name = "退货"


class SalesPay(models.Model):
    PAY_METHOD = (
        (0, '现金'), (1, '微信'), (2, '支付宝'), (3, '其他'),
    )
    sales = models.ForeignKey(Sales, verbose_name="订单")
    method = models.IntegerField(verbose_name="支付方式", choices=PAY_METHOD, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='支付时间')

    @property
    def date(self):
        return self.created_at.date()

    class Meta:
        verbose_name_plural = "销售收款"
        verbose_name = "销售收款"


# 增加销售付款时更新订单状态为已付款
@receiver(post_save, sender=SalesPay, dispatch_uid="update_sales_paysts")
def update_sales_when_pay(sender, instance, **kwargs):
    instance.sales.pay_status = 1
    instance.sales.save()


# 删除销售付款时更新订单状态为已付款
@receiver(pre_delete, sender=SalesPay, dispatch_uid="delete_sales_paysts")
def update_sales_when_delete(sender, instance, **kwargs):
    instance.sales.pay_status = 0
    instance.sales.save()


# 有销售时更新库存
@receiver(post_save, sender=Sales, dispatch_uid="update_stock_sales")
def update_stock_when_sale(sender, instance, **kwargs):
    stock = instance.stock
    for item in instance.detail.all():
        stock.dec(item.product.id, item.num)

# 有退货时更新库存
@receiver(post_save, sender=Refunds, dispatch_uid="update_stock_refunds")
def update_stock_when_refund(sender, instance, **kwargs):
    stock = instance.stock
    for item in instance.detail.all():
        stock.add(item.product.id, item.num)