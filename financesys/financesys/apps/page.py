#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
分页函数
'''

from django.core.paginator import Paginator, EmptyPage, InvalidPage


def pages(request, queryset, perPage=8):
    '''分页函数，每页默认8条'''
    paginators = Paginator(queryset, perPage)
    try:
        pages = int(request.GET.get('page', 1))
        queryset = paginators.page(pages)
    except (EmptyPage, InvalidPage):
        queryset = paginators.page(1)
    return queryset
