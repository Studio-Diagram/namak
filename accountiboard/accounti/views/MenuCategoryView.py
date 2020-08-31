from django.http import JsonResponse
import json
from accounti.models import *
from accountiboard.constants import *


def change_list_order(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    menu_cat_id = rec_data['menu_cat_id']
    change_type = rec_data['change_type']
    username = rec_data['username']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
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


def get_categires_base_on_kind(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    kind = rec_data['kind']
    username = rec_data['username']
    current_branch = rec_data['current_branch']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNAUTHENTICATED})
    if not kind:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    menu_cats = MenuCategory.objects.filter(kind=kind, branch=current_branch).values()

    return JsonResponse({"response_code": 2, "categories": list(menu_cats)})
