#!/usr/bin/env python
# coding: utf-8
import json

from custom.models import Provider


def get_providers():
    providers = []
    for p in Provider.objects.all():
        providers.append(p)
    return providers
