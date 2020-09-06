from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
import json
from accounti.models import *
from accountiboard.constants import *

class ChangeListOrderView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        menu_cat_id = rec_data.get('menu_cat_id')
        change_type = rec_data.get('change_type')

        if not menu_cat_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        menu_cat_obj = MenuCategory.objects.filter(id=menu_cat_id).first()
        menu_cat_order = menu_cat_obj.list_order
        if change_type == "UP":
            new_order = menu_cat_order - 1
            if new_order != 0:
                old_menu_cat_obj = MenuCategory.objects.filter(list_order=new_order).first()
                old_menu_cat_obj.list_order = menu_cat_order
                old_menu_cat_obj.save()
                menu_cat_obj.list_order = new_order
                menu_cat_obj.save()

        elif change_type == "DOWN":
            max_order_number = MenuCategory.objects.all().count()
            new_order = menu_cat_order + 1
            if new_order <= max_order_number:
                old_menu_cat_obj = MenuCategory.objects.filter(list_order=new_order).first()
                old_menu_cat_obj.list_order = menu_cat_order
                old_menu_cat_obj.save()
                menu_cat_obj.list_order = new_order
                menu_cat_obj.save()

        return JsonResponse({"response_code": 2})


class GetCategoriesBasedOnKindView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        kind = rec_data.get('kind')
        current_branch = rec_data.get('current_branch')

        if not kind:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        menu_cats = MenuCategory.objects.filter(kind=kind, branch=current_branch).values()

        return JsonResponse({"response_code": 2, "categories": list(menu_cats)})
