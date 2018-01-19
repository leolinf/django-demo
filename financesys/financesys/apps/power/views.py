# -*- coding:utf-8 -*-
import time
import datetime
import jieba
import jieba.analyse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from models import Data, User
from forms import LoginForm, RegForm
from django.views.decorators.cache import cache_page
# Create your views here.


def do_login(request):
    '''登陆'''
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    # 指定默认的登录验证方式
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        print e
    return render(request, 'login.html', locals())


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
        raise Http404
    return redirect(request.META['HTTP_REFERER'])


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            if request.POST['password'] != request.POST['password_again']:
                return render(request, 'reg.html', {"reason": u"两次密码不相同"})
            if request.POST['username'] in User.objects.values_list('username', flat=True):
                return render(request, 'reg.html', {"reason": u"用户已存在"})
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),)
                user.save()
                # 登录
                # 指定默认的登录验证方式
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                if '/power/login/' in request.POST.get('source_url') or\
                        '/power/reg/' in request.POST.get('source_url'):
                    return redirect('/home/')
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        print e
    return render(request, 'reg.html', locals())


@cache_page(60 * 3)
@login_required(login_url='/power/login/')
def quanzhong(request):
    '''关键词权重展示'''
    now = int(time.time())
    week_now = now - 604800
    ltime = time.localtime(week_now)
    this_time = datetime.datetime.now()
    week_time = time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    texts = Data.objects(release_time__gte=week_time, release_time__lt=this_time).sum('title')
    findWords = jieba.analyse.extract_tags(texts, topK=15, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    keyword = {}
    weight = []
    a = 0
    for wd, weights in findWords:
        keyword['data{0}'.format(a)] = wd
        weight.append(weights)
        a += 1
    return render(request, 'quanzhong.html', {"keyword": keyword, "weight": weight})


class TongJi(LoginRequiredMixin, View):
    '''统计展示'''
    login_url = '/power/login/'

    def get(self, request, *args, **kwargs):
        now =int(1000 * time.time())
        show_news = Data.objects.order_by("-release_time")
        # 浏览量排行
        try:
            a = 0; b = 0; c = 0
            for page_view in show_news:
                release_times = page_view.release_time
                TimeArray = time.strptime(str(release_times), "%Y-%m-%d %H:%M:%S")
                timestamp = int(1000 * (time.mktime(TimeArray)))
                if timestamp > now - 259200000 and timestamp < now:
                    if page_view['relationship'] == 1:
                        a += 1
                    elif page_view['relationship'] == 2:
                        b += 1
                    elif page_view['relationship'] == 3:
                        c += 1
            aa=0; bb=0; cc=0
            for page_view in show_news:
                release_times = page_view.release_time
                TimeArray = time.strptime(str(release_times), "%Y-%m-%d %H:%M:%S")
                timestamp = int(1000 * (time.mktime(TimeArray)))
                if timestamp > now - 604800000 and timestamp < now:
                    if page_view['relationship'] == 1:
                        aa += 1
                    elif page_view['relationship'] == 2:
                        bb += 1
                    elif page_view['relationship'] == 3:
                        cc += 1
        except Exception as e:
            print e
            return render(request, 'failure.html', {"reason": u"没有相关新闻"})
        return render(request, 'tongji.html', {"a": a, 'b': b, 'c': c, 'aa': aa, 'bb': bb, 'cc': cc})


class Setting(LoginRequiredMixin, View):
    '''站点监控'''
    login_url = '/power/login/'

    def get(self, request, *args, **kwargs):
        return render(request, 'category.html', {})
