# coding: utf-8

'''
不推荐 import * 的写法，这里是为了区分环境才这样写
'''

from .base_settings import *
try:
    from .settings_dev import *
    print("使用DEV配置")
except ImportError:
    from .settings_prod import *
    print("使用PROD配置")
