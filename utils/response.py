#!/usr/bin/env python
# coding: utf-8
from django.http import JsonResponse


def success_response(data=None):
    result = {"msg": "success",
              "data": data if data else {}}
    return JsonResponse(result)


def failed_response(msg):
    result = {"msg": "failed",
              "data": msg if msg else "网络故障，请您稍后再试！"}
    return JsonResponse(result)


def need_login():
    return failed_response('用户未登录，请登录')
