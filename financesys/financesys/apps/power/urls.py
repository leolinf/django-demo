#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import TongJi, do_login, do_reg,\
    do_logout, quanzhong, Setting

urlpatterns = [
    url(r'^$', TongJi.as_view()),
    url(r'^login/$', do_login, name="do_login"),
    url(r'^reg/$', do_reg, name="do_reg"),
    url(r'^logout/$', do_logout, name="do_logout"),
    url(r'^quanzhong/$', quanzhong, name="quanzhong"),
    url(r'^setting/$', Setting.as_view())
]
