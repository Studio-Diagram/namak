from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
import json
from accounti.models import *
from accountiboard.constants import *

class ChangeListOrderView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        menu_cat_id = rec_data.get('menu_cat_id')
        change_type = rec_data.get('change_type')
        branch_id = rec_data.get('branch_id')

        if not menu_cat_id:
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=403)

        all_menu_categories_current_branch = MenuCategory.objects.filter(branch=branch_id).order_by('list_order')
        all_menu_categories_list = [x for x in all_menu_categories_current_branch]

        if not all_menu_categories_list:
            JsonResponse({"error_msg": MENU_CATEGORY_NOT_FOUND}, status=403)

        for i, menu_cat in enumerate(all_menu_categories_list):
            if menu_cat_id == menu_cat.id:
                current_menu_cat_index = i
                break

        if change_type == 'UP':
            if current_menu_cat_index == 0:
                return JsonResponse({})
            else:
                temp = all_menu_categories_list[current_menu_cat_index]
                all_menu_categories_list[current_menu_cat_index] = all_menu_categories_list[current_menu_cat_index - 1]
                all_menu_categories_list[current_menu_cat_index - 1] = temp

        elif change_type == 'DOWN':
            if current_menu_cat_index == len(all_menu_categories_list) - 1:
                return JsonResponse({})
            else:
                temp = all_menu_categories_list[current_menu_cat_index]
                all_menu_categories_list[current_menu_cat_index] = all_menu_categories_list[current_menu_cat_index + 1]
                all_menu_categories_list[current_menu_cat_index + 1] = temp

        # check if have to reorder all:
        if len({x.list_order for x in all_menu_categories_list}) < len(all_menu_categories_list):
            for i, menu_cat in enumerate(all_menu_categories_list):
                menu_cat.list_order = i
                menu_cat.save()
        # otherwise just update the two affected menu_categories:
        else:
            if change_type == 'UP':
                temp = all_menu_categories_list[current_menu_cat_index - 1].list_order
                all_menu_categories_list[current_menu_cat_index - 1].list_order = all_menu_categories_list[current_menu_cat_index].list_order
                all_menu_categories_list[current_menu_cat_index].list_order = temp
                all_menu_categories_list[current_menu_cat_index - 1].save()
                all_menu_categories_list[current_menu_cat_index].save()
            elif change_type == 'DOWN':
                temp = all_menu_categories_list[current_menu_cat_index + 1].list_order
                all_menu_categories_list[current_menu_cat_index + 1].list_order = all_menu_categories_list[current_menu_cat_index].list_order
                all_menu_categories_list[current_menu_cat_index].list_order = temp
                all_menu_categories_list[current_menu_cat_index + 1].save()
                all_menu_categories_list[current_menu_cat_index].save()

        return JsonResponse({})


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
