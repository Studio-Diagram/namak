from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
import json
from accounti.models import *
from accountiboard.constants import *


def reorder_model_objects(all_menu_categories_list, current_menu_cat_index, index_offset):
    temp = all_menu_categories_list[current_menu_cat_index]
    all_menu_categories_list[current_menu_cat_index] = all_menu_categories_list[current_menu_cat_index - 1]
    all_menu_categories_list[current_menu_cat_index + index_offset] = temp

def swap_list_orders(all_menu_categories_list, current_menu_cat_index, index_offset):
    temp = all_menu_categories_list[current_menu_cat_index + index_offset].list_order
    all_menu_categories_list[current_menu_cat_index + index_offset].list_order = all_menu_categories_list[current_menu_cat_index].list_order
    all_menu_categories_list[current_menu_cat_index].list_order = temp
    all_menu_categories_list[current_menu_cat_index + index_offset].save()
    all_menu_categories_list[current_menu_cat_index].save()

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
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        all_menu_categories_current_branch = MenuCategory.objects.filter(branch=branch_id).order_by('list_order')
        all_menu_categories_list = [menu_category for menu_category in all_menu_categories_current_branch]

        if not all_menu_categories_list:
            JsonResponse({"error_msg": MENU_CATEGORY_NOT_FOUND}, status=403)

        if len({menu_category.list_order for menu_category in all_menu_categories_list}) < len(all_menu_categories_list):
            reorder = True
        else:
            reorder = False

        for i, menu_cat in enumerate(all_menu_categories_list):
            if menu_cat_id == menu_cat.id:
                current_menu_cat_index = i
                break

        if change_type == 'UP':
            if current_menu_cat_index == 0:
                return JsonResponse({})
            else:
                if reorder:
                    reorder_model_objects(all_menu_categories_list, current_menu_cat_index, -1)
                else:
                    swap_list_orders(all_menu_categories_list, current_menu_cat_index, -1)

        elif change_type == 'DOWN':
            if current_menu_cat_index == len(all_menu_categories_list) - 1:
                return JsonResponse({})
            else:
                if reorder:
                    reorder_model_objects(all_menu_categories_list, current_menu_cat_index, 1)
                else:
                    swap_list_orders(all_menu_categories_list, current_menu_cat_index, 1)

        if reorder:
            for i, menu_cat in enumerate(all_menu_categories_list):
                menu_cat.list_order = i
                menu_cat.save()

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
