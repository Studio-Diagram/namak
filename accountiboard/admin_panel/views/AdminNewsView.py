from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from admin_panel.forms.CreateNewsForm import *
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
                    'news_id': news.id,
                    'news_title': news.title,
                    'news_text': news.text,
                    'news_link': news.link,
                    'news_datetime': news.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
                }
            )
         
        context['all_news'] = all_news_list

        return render(request, 'admin_panel_news.html', context)


class AdminNewsCreateView(View):

    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = CreateNewsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            LatestNews.objects.create(
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                link = form.cleaned_data['link'],
            )

            # redirect to a new URL:
            return HttpResponseRedirect('/onward/news/')


    def get(self, request, *args, **kwargs):
        form = CreateNewsForm()
        return render(request, 'admin_panel_news_create.html', {'form': form})



class AdminNewsDeleteView(View):

    def post(self, request, latestnews_id, *args, **kwargs):
        try:
            current_news = LatestNews.objects.get(pk=latestnews_id)
        except:
            return HttpResponse("Error 404: news with that id was not found", status=404)

        current_news.delete()

        return HttpResponseRedirect('/onward/news/')

