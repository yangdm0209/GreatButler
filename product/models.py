#!/usr/bin/env python
# coding: utf-8

from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name="名字", db_index=True)
    price_cost = models.FloatField(verbose_name="进货价")
    price_wholesale = models.FloatField(verbose_name="批发售价", blank=True)
    price_retail = models.FloatField(verbose_name="终端售价")
    specification = models.CharField(max_length=128, verbose_name="规格", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    other = models.CharField(max_length=128, verbose_name='其他信息', blank=True)
    min_stock = models.IntegerField(verbose_name='最小库存', blank=True)

    def __unicode__(self):
        return self.name

    @property
    def date(self):
        return self.created_at.date()

    class Meta:
        verbose_name_plural = "产品信息"
        verbose_name = "产品信息"
