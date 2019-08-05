from django.http import JsonResponse
import json, base64, random
from accounti.models import *
import accountiboard.settings as settings
from PIL import Image
from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def add_table(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        table_id = rec_data['table_id']
        name = rec_data['name']

        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if table_id == 0:
            new_table = Table(
                name=name,
            )
            new_table.save()

            return JsonResponse({"response_code": 2})
        else:
            old_table = Table.objects.get(pk=table_id)
            old_table.name = name
            old_table.save()
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_table(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Table.objects.filter(name__contains=search_word)
        tables = []
        for table in items_searched:
            tables.append({
                'table_id': table.pk,
                'table_name': table.name,
            })
        return JsonResponse({"response_code": 2, 'tables': tables})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_table(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        table_id = rec_data['table_id']
        table = Table.objects.get(pk=table_id)
        table_data = {
            'table_id': table.pk,
            'table_name': table.name,
        }
        return JsonResponse({"response_code": 2, 'table': table_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
