#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
register = template.Library()


@register.filter
def month_to_upper(key):
    return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][key.month - 1]


@register.filter(name='list_filter')
def list_filter(keys):
    try:
        if len(keys) >= 2:
            return keys[0] + keys[1]
        else:
            try:
                return keys[0]
            except:
                return ''
    except Exception as e:
        print e
