#!/usr/bin/env python
# coding: utf-8
import json

from custom.models import Provider, Custom


def get_providers():
    return Provider.objects.all()


def get_customs():
    return Custom.objects.all()
