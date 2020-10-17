from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from accounti.models import *
from accountiboard.custom_permissions import *

class AdminView(View):

    @permission_decorator_class_based_simplified(session_authenticate_admin_panel)
    def get(self, request, *args, **kwargs):
        context = {}

        all_branches_q = Branch.objects.all()
        all_branches_list = []

        for i, branch in enumerate(all_branches_q):
            cafe_owner = branch.organization.cafeowner_set.first().user
            all_branches_list.append(
                {
                    'number': i + 1,
                    'highlight': True if i % 2 == 0 else False,
                    'branch_id': branch.id,
                    'branch_name': branch.name,
                    'branch_organization': branch.organization.name,
                    'branch_cafeowner': f'{cafe_owner.first_name} {cafe_owner.last_name}',
                }
            )
            
        context['all_branches'] = all_branches_list


        return render(request, 'admin_panel_main.html', context)

