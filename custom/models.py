#!/usr/bin/env python
# coding: utf-8

from django.db import models


# Create your models here.

class Custom(models.Model):
    C_TP = (
        (0, u'代理'),
        (1, u'终端')
    )
    name = models.CharField(max_length=128, verbose_name="客户名字", db_index=True)
    type = models.IntegerField(choices=C_TP, blank=False, default=1, verbose_name='客户类型')
    tel = models.CharField(max_length=20, verbose_name="客户电话")
    addr = models.CharField(max_length=128, verbose_name="客户地址")
    other = models.CharField(max_length=128, verbose_name="其他信息", blank=True)

    @property
    def get_type(self):
        for item in self.C_TP:
            if item[0] == self.type:
                return item[1]

    def __unicode__(self):
        return u'%s-%s-%s' % (self.name, self.get_type, self.tel)

    class Meta:
        verbose_name_plural = "客户信息"
        verbose_name = "客户信息"
