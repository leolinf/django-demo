# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from weibit.users import views


urlpatterns = [
    url(
        r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippets_list'
    ),
    url(
        r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippets'
    ),
    url(
        r'^api-auth',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(
        r'^api-token-auth',
        obtain_jwt_token
    )
]
