from django.http import JsonResponse
import json, base64, random
from accounti.models import *
import accountiboard.settings as settings
from PIL import Image
from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def add_branch(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch_id']
        name = rec_data['name']
        address = rec_data['address']
        start_time = rec_data['start_time']
        end_time = rec_data['end_time']

        if not name:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not address:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not start_time:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not end_time:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if branch_id == 0:
            new_branch = Branch(
                name=name,
                address=address,
                start_working_time=datetime.strptime(start_time, '%H:%M'),
                end_working_time=datetime.strptime(end_time, '%H:%M')
            )
            new_branch.save()

            return JsonResponse({"response_code": 2})
        else:
            old_branch = Branch.objects.get(pk=branch_id)
            old_branch.name = name
            old_branch.address = address
            old_branch.start_working_time = datetime.strptime(start_time, '%H:%M')
            old_branch.end_working_time = datetime.strptime(end_time, '%H:%M')
            old_branch.save()
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_branches(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        branches = Branch.objects.all()
        branches_data = []
        for branch in branches:
            branches_data.append({
                'id': branch.pk,
                'name': branch.name,
                'address': branch.address,
                'start_time': branch.start_working_time,
                'end_time': branch.end_working_time
            })
        return JsonResponse({"response_code": 2, 'branches': branches_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_branch(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Branch.objects.filter(name__contains=search_word)
        branches = []
        for branch in items_searched:
            branches.append({
                "id": branch.pk,
                "name": branch.name,
                'address': branch.address,
                'start_time': branch.start_working_time,
                'end_time': branch.end_working_time
            })
        return JsonResponse({"response_code": 2, 'branches': branches})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_branch(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        branch_id = rec_data['branch_id']
        branch = Branch.objects.get(pk=branch_id)
        branch_data = {
            'id': branch.pk,
            'name': branch.name,
            'address': branch.address,
            'start_time': branch.start_working_time,
            'end_time': branch.end_working_time
        }
        return JsonResponse({"response_code": 2, 'branch': branch_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_working_time_for_reserve(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch']

        if not username:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        branch = Branch.objects.get(pk=branch_id)

        start_time = datetime.strptime(branch.start_working_time.strftime("%H:%M"), "%H:%M")
        end_time = datetime.strptime(branch.end_working_time.strftime("%H:%M"), "%H:%M") + timedelta(minutes=15)
        working_data = []

        while start_time.time() != end_time.time():
            if start_time.strftime("%M") == '00':
                working_data.append({
                    'time': start_time.strftime("%H:%M"),
                    'hour': start_time.strftime("%H"),
                    'minute': start_time.strftime("%M"),
                    'is_hour': 1
                })
            else:
                working_data.append({
                    'time': start_time.strftime("00:%M"),
                    'hour': start_time.strftime("%H"),
                    'minute': start_time.strftime("%M"),
                    'is_hour': 0
                })
            start_time = datetime.strptime(start_time.strftime("%H:%M"), "%H:%M") + timedelta(minutes=15)

        return JsonResponse({"response_code": 2, 'working_data': working_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

