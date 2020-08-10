from accountiboard.constants import *
from accountiboard.custom_permissions import *
from accounti.models import *
from django.views import View
import jdatetime


class LatestNewsView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], 
                                      USER_ROLES['ACCOUNTANT'], USER_ROLES['CASHIER'],
                                      USER_ROLES['STAFF'], USER_ROLES['ADMIN']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):

        all_news_queryset = LatestNews.objects.all()
        all_news_list = [{
                        'title': x.title,
                        'text' : x.text,
                        'link' : x.link,
                        'datetime' : jdatetime.datetime.fromgregorian(
                                                            day=x.datetime.day,
                                                            month=x.datetime.month,
                                                            year=x.datetime.year,
                                                            hour=x.datetime.hour,
                                                            minute=x.datetime.minute
                                    ).strftime('%Y/%m/%d %H:%M')
            } for x in all_news_queryset]

        return JsonResponse({'results': all_news_list}, status=200)


    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['ADMIN']},
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        title = rec_data.get('title')
        text = rec_data.get('text')
        link = rec_data.get('link')

        if not title or not text:
            return JsonResponse({'error_msg': 'title and text are required fields'}, status=400)

        current_news = LatestNews.objects.create(
            title = title,
            text = text,
            link = link,
        )

        return JsonResponse({'created_news': {
                        'title': current_news.title,
                        'text' : current_news.text,
                        'link' : current_news.link,
        }}, status=200)