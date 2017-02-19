#!/usr/bin/env python
# coding: utf-8

from django.db import models


# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=20, verbose_name='区域')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '区域信息'
        verbose_name = '区域信息'


class CustomType(models.Model):
    name = models.CharField(max_length=64, verbose_name='客户类型')
    alias = models.CharField(max_length=2, verbose_name='类型代号')

    def __unicode__(self):
        return '%s: %s' % (self.alias, self.name)

    class Meta:
        verbose_name = '客户类型'
        verbose_name_plural = '客户类型'


class Custom(models.Model):
    # C_TP = (
    #     (u'A', u'A：配件批发商'),
    #     (u'B', u'B：手机数码配件店'),
    #     (u'C', u'C：手机店'),
    #     (u'D', u'D：手机连锁店'),
    #     (u'E', u'E：其他'),
    # )
    name = models.CharField(max_length=128, verbose_name='客户名称', db_index=True)
    type = models.ForeignKey(CustomType, verbose_name='客户类型')
    area = models.ForeignKey(Area, verbose_name='区域')
    contacts = models.CharField(max_length=64, verbose_name='联系人', db_index=True)
    tel = models.CharField(max_length=20, verbose_name='联系电话', db_index=True)
    addr = models.CharField(max_length=128, verbose_name='客户地址', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    other = models.CharField(max_length=128, verbose_name='其他信息', blank=True)

    def __unicode__(self):
        return u'%s(%s)' % (self.name, self.area)

    class Meta:
        verbose_name_plural = '客户信息'
        verbose_name = '客户信息'


class Saler(models.Model):
    name = models.CharField(max_length=64, verbose_name='名字', db_index=True)
    tel = models.CharField(max_length=20, verbose_name='联系电话', db_index=True)
    addr = models.CharField(max_length=128, verbose_name='家庭地址', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    other = models.CharField(max_length=128, verbose_name='其他信息', blank=True)

    def __unicode__(self):
        return self.name

    @property
    def date(self):
        return self.created_at.date()

    class Meta:
        verbose_name_plural = '业务员信息'
        verbose_name = '业务员信息'


class Provider(models.Model):
    name = models.CharField(max_length=64, verbose_name='供应商', db_index=True)
    tel = models.CharField(max_length=20, verbose_name='联系电话', db_index=True)
    addr = models.CharField(max_length=128, verbose_name='地址', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    other = models.CharField(max_length=128, verbose_name='其他信息', blank=True)

    def __unicode__(self):
        return self.name

    @property
    def date(self):
        return self.created_at.date()

    class Meta:
        verbose_name_plural = '供应商信息'
        verbose_name = '供应商信息'
