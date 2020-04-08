from django.http import JsonResponse
import json
from accounti.models import *
from django.db import IntegrityError

UUID_EMPTY_ERROR = "UUID is empty!"
METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
DUPLICATE_MEMBER_ENTRY = "شماره تلفن یا کارت تکراری است."
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."


def status_of_server(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    return JsonResponse({"response_code": 2})


def sync_member_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Member.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "last_name": item.last_name,
        "card_number": item.card_number,
        "p_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'members': have_to_add_data})


def sync_menu_category_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = MenuCategory.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "kind": item.kind,
        "list_order": item.list_order,
        "p_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'members': have_to_add_data})


def create_member(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    member_id = rec_data.get('member_id')
    first_name = rec_data.get('first_name')
    last_name = rec_data.get('last_name')
    card_number = rec_data.get('card_number')
    card_number = card_number.replace("؟", "")
    card_number = card_number.replace("٪", "")
    card_number = card_number.replace("?", "")
    card_number = card_number.replace("%", "")
    year_of_birth = rec_data.get('year_of_birth')
    month_of_birth = rec_data.get('month_of_birth')
    day_of_birth = rec_data.get('day_of_birth')
    intro = rec_data.get('intro')
    phone = rec_data.get('phone')

    if not first_name:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not last_name:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not card_number:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not year_of_birth:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not month_of_birth:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not day_of_birth:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not phone:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not intro:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    if member_id == 0:
        try:
            new_member = Member(
                first_name=first_name,
                last_name=last_name,
                card_number=card_number,
                year_of_birth=year_of_birth,
                month_of_birth=month_of_birth,
                day_of_birth=day_of_birth,
                phone=phone,
                intro=intro
            )
            new_member.save()

        except IntegrityError as e:
            if 'unique constraint' in e.args[0]:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

    return JsonResponse({"response_code": 2})
