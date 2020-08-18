from datetime import datetime
from django.views import View
from django.shortcuts import render
from accounti.models import *

class AdminNewsView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        all_news_q = LatestNews.objects.all()
        all_news_list = []

        for i, news in enumerate(all_news_q):
            all_news_list.append(
                {
                    'number': i + 1,
                    'highlight': True if i % 2 == 0 else False,
                    'news_title': news.title,
                    'news_text': news.text,
                    'news_link': news.link,
                    'news_datetime': news.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
                }
            )
         
        context['all_news'] = all_news_list

        return render(request, 'admin_panel_news.html', context)

