"""tide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tide.settings import (
    DEBUG,
    MEDIA_URL,
    MEDIA_ROOT
)
from django.conf.urls.static import static
from django.urls import re_path
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('app.user.urls')),
    url(r'^authorize/login/$', obtain_jwt_token),
    url(r'^authorize/refresh-token/$', refresh_jwt_token),
]

if DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    from django.contrib.staticfiles import views
    schema_view = get_swagger_view(title="docs")
    urlpatterns += [
        url(r'^restframework/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^$', schema_view),
    ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]
