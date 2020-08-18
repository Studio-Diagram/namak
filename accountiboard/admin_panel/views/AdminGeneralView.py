from django.views import View
from django.shortcuts import render

class AdminView(View):

    def get(self, request, *args, **kwargs):
        context = {'first_name' : 'woo'}
        return render(request, 'admin_panel_main2.html', context)

