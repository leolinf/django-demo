# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

from rest_framework.request import Request


class TestMiddleware:

    def __init__(self, get_response):
        print(get_response)
        self.get_response = get_response

    def __call__(self, request):
        print("start request")
        response = self.get_response(request)
        print(response)
        return response

    def process_request(self, request):
        print("test")


def get_user_jwt(request):
    user = get_user(request)
    if user.is_authenticated():
        return user
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        print('##########', user_jwt)
        if user_jwt is not None:
            return user_jwt[0]
    except:
        pass
    return user


class AuthenticationMiddlewareJWT(MiddlewareMixin):

    def process_request(self, request):
        a = hasattr(request, 'session')
        print('test')
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
