#!/usr/bin/env python
# coding: utf-8

# 把datetime转成字符串
import time
from datetime import datetime


def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")


# 把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d")


# 把字符串转成时间戳形式
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())


# 把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d", time.localtime(stamp))


# 把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())


# print string_toDatetime("2017-02-10")