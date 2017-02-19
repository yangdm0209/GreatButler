#!/usr/bin/env python
# coding: utf-8

from django.db import models

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
