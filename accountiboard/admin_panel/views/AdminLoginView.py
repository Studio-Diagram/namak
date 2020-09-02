from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from admin_panel.forms.LoginForm import *
from accounti.models import *
from django.contrib.auth import authenticate


class AdminLoginView(View):

    def post(self, request, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        auth_error = False
        # check whether it's valid:
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_staff:
                request.session['admin_is_logged_in'] = user.username
            else:
                auth_error = True
                return render(request, 'admin_panel_login.html', {'form': form, 'auth_error':auth_error})

            # redirect to a new URL:
            return HttpResponseRedirect('/onward/')


    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'admin_panel_login.html', {'form': form})

class AdminLogoutView(View):

    def get(self, request, *args, **kwargs):
        request.session.flush()
        form = LoginForm()
        return render(request, 'admin_panel_login.html', {'form': form})