#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from views import (ShowNews,
                   NewsDetail,
                   ImportantShow,
                   MostImportantShow,
                   TodaySort,
                   MonthArchive,
                   Search,
                   Home)

urlpatterns = [
    url(r'^$',
        Home.as_view(),
        name="home",
        ),
    url(r'^home/$',
        ShowNews.as_view()
        ),
    url(r'^home/detail/$',
        NewsDetail.as_view()
        ),
    url(r'^home/important/$',
        ImportantShow.as_view()
        ),
    url(r'^home/most_important/$',
        MostImportantShow.as_view()
        ),
    url(r'^home/today_sort/$',
        TodaySort.as_view()
        ),
    url(r'^home/archive/$',
        MonthArchive.as_view()
        ),
    url(r'^home/search/$',
        Search.as_view()
        ),
]
