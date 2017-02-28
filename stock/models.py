#!/usr/bin/env python
# coding: utf-8

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import Product
from custom.models import Saler


# Create your models here.

class ProductNum(models.Model):
    product = models.ForeignKey(Product, verbose_name='产品')
    num = models.IntegerField(verbose_name='库存')

    def __unicode__(self):
        return u'%s*%s' % (self.product.name, self.num)

    class Meta:
        verbose_name_plural = "产品库存"
        verbose_name = "产品库存"


class Stock(models.Model):
    name = models.CharField(max_length=128, verbose_name='仓库名字', db_index=True)
    belong = models.ForeignKey(Saler, verbose_name='业务员')
    nums = models.ManyToManyField(ProductNum, verbose_name='库存', related_name='stock')

    def __unicode__(self):
        return self.name

    @property
    def total_products(self):
        return self.nums.all().count()

    @property
    def total_nums(self):
        total = 0
        for item in self.nums.all():
            total += item.num
        return total

    def add(self, id, num):
        add_flg = False
        for item in self.nums.all():
            if item.product.id == id:
                item.num += num
                item.save()
                add_flg = True
                break
        if not add_flg:
            pro = ProductNum()
            pro.product = Product.objects.get(id=id)
            pro.num = num
            pro.save()
            self.nums.add(pro)
        self.save()

    def dec(self, id, num):
        add_flg = False
        for item in self.nums.all():
            if item.product.id == id:
                item.num -= num
                item.save()
                add_flg = True
                break
        if not add_flg:
            pro = ProductNum()
            pro.product = Product.objects.get(id=id)
            pro.num = num * -1
            pro.save()
            self.nums.add(pro)
        self.save()

    class Meta:
        verbose_name_plural = "仓库库存"
        verbose_name = "仓库库存"


class AllocateNum(models.Model):
    product = models.ForeignKey(Product, verbose_name='产品')
    num = models.IntegerField(verbose_name='数量')

    def __unicode__(self):
        return u'%s*%s' % (self.product.name, self.num)

    class Meta:
        verbose_name_plural = "调拨产品"
        verbose_name = "调拨产品"


class Allocate(models.Model):
    source_stock = models.ForeignKey(Stock, verbose_name="转出仓库", related_name='source')
    dest_stock = models.ForeignKey(Stock, verbose_name="转入仓库", related_name='dest')
    nums = models.ManyToManyField(AllocateNum, verbose_name="调拨产品", related_name='allocate')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return u'%s调入%s' % (self.source_stock.name, self.dest_stock.name)

    @property
    def total_products(self):
        return self.nums.all().count()

    @property
    def total_nums(self):
        total = 0
        for item in self.nums.all():
            total += item.num
        return total

    class Meta:
        verbose_name_plural = "仓库调拨"
        verbose_name = "仓库调拨"


# 有调拨时更新库存
@receiver(post_save, sender=Allocate, dispatch_uid="update_stock_allocate")
def update_stock_when_allocate(sender, instance, **kwargs):
    source_stock = instance.source_stock
    dest_stock = instance.dest_stock
    for item in instance.nums.all():
        source_stock.dec(item.product.id, item.num)
        dest_stock.add(item.product.id, item.num)
