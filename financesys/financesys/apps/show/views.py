# -*- coding:utf-8 -*-
import time
import datetime
import jieba
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from financesys.apps.page import pages
from django.conf import settings
from models import Data


now = 1000 * int(time.time())


def global_setting(request):
    '''模板全局变量'''
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    show_news = Data.objects.order_by("-release_time")
    import_news = []
    for new in show_news:
        if len(import_news) == 6:
            break
        if new.relationship == 2:
            import_news.append(new)
    importest_news = []
    for new in show_news:
        if len(importest_news) == 6:
            break
        if new.relationship == 3:
            importest_news.append(new)
    # 浏览量排行
    data = []
    for page_view in show_news:
        release_times = page_view.release_time
        TimeArray = time.strptime(str(release_times), "%Y-%m-%d %H:%M:%S")
        timestamp = int(1000 * (time.mktime(TimeArray)))
        if timestamp > now - 43200000 and timestamp < now:
            data.append(page_view)

    page_view_sort = sorted(data, key=lambda n: n['page_view'])
    page_views = page_view_sort[-6:][::-1]
    year = int(str(datetime.datetime.now())[0: 4])
    month = str(datetime.datetime.now())[5: 7]
    if int(month) == 1:
        last_month = 12
        last_last_month = last_month - 1
    else:
        last_month = int(month) - 1
        if last_month == 1:
            last_last_month = 12
        else:
            last_last_month = last_month - 1
    month_list = [int(month), last_month, last_last_month]
    return locals()


class ShowNews(View):
    '''展示新闻'''

    def get(self, request, *args, **kwargs):
        key = u'最新新闻展示'
        news = Data.objects().order_by("-release_time")
        try:
            article_list = pages(request, news)
        except Exception as e:
            print e
            raise Http404("news error")
        return render(request, 'index.html', {"article_list": article_list, "key": key})


class NewsDetail(View):
    '''新闻详情展示'''

    def get(self, request, *args, **kwargs):
        client_id = request.GET.get('id', None)
        try:
            news = Data.objects(id=client_id)[0]
        except Exception as e:
            print e
            return render(request, 'failure.html', {"reason": u"没有相关新闻"})
        return render(request, 'article.html', locals())


class ImportantShow(View):
    '''重要新闻展示'''

    def get(self, request, *args, **kwargs):
        key = u'最新重要新闻展示'
        important_news = Data.objects.all().order_by('-release_time')
        impt_news = []
        for important_new in important_news:
            if important_new.relationship == 2:
                impt_news.append(important_new)
        try:
            article_list = pages(request, impt_news)
        except Exception as e:
            print e
            return render(request, 'failure.html', {"reason": u"没有相关新闻"})
        return render(request, 'index.html', {"article_list": article_list, "key": key})


class MostImportantShow(View):
    '''特别重要展示'''

    def get(self, request, *args, **kwargs):
        key = u'最新特别重要新闻展示'
        important_news = Data.objects.all().order_by('-release_time')
        impt_news = []
        for important_new in important_news:
            if important_new.relationship == 3:
                impt_news.append(important_new)
        try:
            article_list = pages(request, impt_news)
        except Exception as e:
            print e
            return render(request, 'failure.html', {"reason": u"没有相关新闻"})
        return render(request, 'index.html', {"article_list": article_list, "key": key})


class TodaySort(View):
    '''当天浏览排行'''

    def get(self, request, *args, **kwargs):
        key = u'24小时内新闻浏览量排行展示'
        show_news = Data.objects.order_by("-release_time")
        # 浏览量排行
        data = []
        for page_view in show_news:
            release_times = page_view.release_time
            TimeArray = time.strptime(str(release_times), "%Y-%m-%d %H:%M:%S")
            timestamp = int(1000 * (time.mktime(TimeArray)))
            if timestamp > now - 43200000 and timestamp < now:
                data.append(page_view)

        page_view_sort = sorted(data, key=lambda n: n['page_view'])
        page_view_todays = page_view_sort[::-1]
        try:
            article_list = pages(request, page_view_todays)
        except Exception as e:
            print e
            return render(request, 'failure.html', {"reason": u"没有相关新闻"})
        return render(request, 'index.html', {"article_list": article_list, "key": key})


class MonthArchive(View):
    '''新闻归档'''

    def get(self, request, *args, **kwargs):
        this_month = datetime.datetime(int(year), int(month) + 1, 1)
        last_month = datetime.datetime(int(year), int(month), 1)
        archive_last_months = Data.objects(release_time__gte=last_month, release_time__lt=this_month)
        impt_news = []
        for important_new in archive_last_months:
            if important_new.relationship == 2:
                impt_news.append(important_new)
        try:
            article_list = pages(request, impt_news)
        except Exception as e:
            print e
            raise Http404("news error")
        return render(request, 'archive.html', {"article_list": article_list})


class Search(View):
    '''搜索功能'''

    def get(self, request, *args, **kwargs):
        key = u'关键词搜索展示'
        content_get = request.GET.get('keywords').split()
        content = ''.join(content_get)
        article_list = []
        if content:
            keywords = jieba.cut_for_search(content)
            for keyword in keywords:
                match = {'$or': [{"title": {"$regex": keyword}}, {"content": {"$regex": keyword}}]}
                article_list.append(match)
        article_list_sort = Data.objects(__raw__={'$and': article_list}).order_by('-release_time')
        try:
            article_list = pages(request, article_list_sort)
        except Exception as e:
            print e
            return redirect('/home/')

        return render(request, 'index.html', {"article_list": article_list, "key": key})


class Home(View):
    '''主页'''

    def get(self, request, *args, **kwargs):
        now_time = int(time.time())
        show_news = Data.objects().order_by("release_time").first().release_time
        TimeArray = time.strptime(str(show_news), "%Y-%m-%d %H:%M:%S")
        timestamp = int((time.mktime(TimeArray)))
        date_time = now_time - timestamp
        day = date_time / (60 * 60 * 24)
        hour = (date_time % (60 * 60 * 24)) / (60 * 60)
        minute = (date_time % (60 * 60 * 24)) / (60 * 60)
        second = (date_time % (60 * 60 * 24)) % (60 * 60) / 60
        return render(request, 'home.html', locals())
