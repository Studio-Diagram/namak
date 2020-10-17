from accountiboard.constants import *
from accountiboard.custom_permissions import *
from accounti.models import *
from django.views import View
import jdatetime


class LatestNewsView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def get(self, request, *args, **kwargs):

        all_news_queryset = LatestNews.objects.all()
        all_news_list = [{
                        'title': x.title,
                        'text' : x.text,
                        'link' : x.link,
                        'datetime' : jdatetime.datetime.fromgregorian(
                                                            day=x.created_time.day,
                                                            month=x.created_time.month,
                                                            year=x.created_time.year,
                                                            hour=x.created_time.hour,
                                                            minute=x.created_time.minute
                                    ).strftime('%Y/%m/%d %H:%M')
            } for x in all_news_queryset]

        return JsonResponse({'results': all_news_list}, status=200)
