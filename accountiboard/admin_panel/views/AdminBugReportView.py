from datetime import datetime
from django.views import View
from django.shortcuts import render
from accounti.models import *
from accountiboard.settings import MEDIA_ROOT

class AdminBugReportsView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        all_bugreports_q = BugReport.objects.all()
        all_bugreports_list = []

        for i, bugreport in enumerate(all_bugreports_q):
            all_bugreports_list.append(
                {
                    'number': i + 1,
                    'highlight': True if i % 2 == 0 else False,
                    'bugreport_title': bugreport.title,
                    'bugreport_text': bugreport.text,
                    'bugreport_user': f'{bugreport.user.last_name} {bugreport.user.first_name}',
                    'bugreport_image': bugreport.image,
                    'bugreport_datetime': bugreport.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
                }
            )
         
        context['all_bugreports'] = all_bugreports_list

        return render(request, 'admin_panel_bugreport.html', context)
