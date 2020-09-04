from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from accounti.models import *
from accountiboard.settings import MEDIA_ROOT
from accountiboard.custom_permissions import *

class AdminBugReportsView(View):

    @permission_decorator_class_based_simplified(session_authenticate_admin_panel)
    def get(self, request, *args, **kwargs):
        context = {}

        all_bugreports_q = BugReport.objects.all()
        all_bugreports_list = []

        for i, bugreport in enumerate(all_bugreports_q):
            all_bugreports_list.append(
                {
                    'number': i + 1,
                    'highlight': True if i % 2 == 0 else False,
                    'bugreport_id': bugreport.id,
                    'bugreport_title': bugreport.title,
                    'bugreport_text': bugreport.text,
                    'bugreport_user': f'{bugreport.user.first_name} {bugreport.user.last_name}',
                    'bugreport_image': bugreport.image,
                    'bugreport_datetime': bugreport.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
                }
            )
         
        context['all_bugreports'] = all_bugreports_list

        return render(request, 'admin_panel_bugreport.html', context)


class AdminBugReportsDetailView(View):

    @permission_decorator_class_based_simplified(session_authenticate_admin_panel)
    def get(self, request, bugreport_id, *args, **kwargs):
        context = {}

        try:
            current_bugreport = BugReport.objects.get(pk=bugreport_id)
        except:
            return HttpResponse("Error 404: bugreport with that id was not found", status=404)

        context['bugreport'] = {
            'bugreport_title': current_bugreport.title,
            'bugreport_text': current_bugreport.text,
            'bugreport_user': f'{current_bugreport.user.first_name} {current_bugreport.user.last_name}',
            'bugreport_image': current_bugreport.image,
            'bugreport_datetime': current_bugreport.created_time.strftime("%m/%d/%Y, %H:%M:%S"),
        }  

        return render(request, 'admin_panel_bugreport_detail.html', context)
