from django.http import JsonResponse
import json, base64, random
from accounti.models import *
from django.db.models import Q
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
DUPLICATE_MEMBER_ENTRY = "شماره تلفن یا کارت تکراری است."

def add_member(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        member_id = rec_data['member_id']
        first_name = rec_data['first_name']
        last_name = rec_data['last_name']
        card_number = rec_data['card_number']
        year_of_birth = rec_data['year_of_birth']
        month_of_birth = rec_data['month_of_birth']
        day_of_birth = rec_data['day_of_birth']
        intro = rec_data['intro']
        phone = rec_data['phone']

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
            except Exception as e:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

            return JsonResponse({"response_code": 2})
        else:
            try:
                old_member = Member.objects.get(pk=member_id)
                old_member.first_name = first_name
                old_member.last_name = last_name
                old_member.card_number = card_number
                old_member.year_of_birth = year_of_birth
                old_member.month_of_birth = month_of_birth
                old_member.day_of_birth = day_of_birth
                old_member.phone = phone
                old_member.intro = intro
                old_member.save()
            except Exception as e:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_members(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        members = Member.objects.all()
        members_data = []
        for member in members:
            members_data.append({
                'id': member.pk,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'phone': member.phone,
            })
        return JsonResponse({"response_code": 2, 'members': members_data})


def search_member(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        branch_id = rec_data['branch']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Member.objects.filter(first_name__contains=search_word) | Member.objects.filter(
            last_name__contains=search_word)
        members = []
        for member in items_searched:
            members.append({
                'id': member.pk,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'phone': member.phone,
            })
        return JsonResponse({"response_code": 2, 'members': members})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_member(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        else:
            member_id = rec_data['member_id']
            card_number = rec_data['card_number']
            if member_id:
                member = Member.objects.get(pk=member_id)
                member_data = {
                    'id': member.pk,
                    'first_name': member.first_name,
                    'last_name': member.last_name,
                    'phone': member.phone,
                    'year_of_birth': member.year_of_birth,
                    'month_of_birth': member.month_of_birth,
                    'day_of_birth': member.day_of_birth,
                    'intro': member.intro,
                    'card_number': member.card_number,
                }
                return JsonResponse({"response_code": 2, 'member': member_data})
            if card_number:
                member = Member.objects.get(card_number=card_number)
                member_data = {
                    'id': member.pk,
                    'first_name': member.first_name,
                    'last_name': member.last_name,
                }
                return JsonResponse({"response_code": 2, 'member': member_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})



def add_old_member(request):
    import sqlite3
    if request.method == "POST":
        try:
            conn = sqlite3.connect("../db.sqlite3")
            cur = conn.cursor()
            cur.execute("SELECT * FROM cmanager_user")

            rows = cur.fetchall()

            for row in rows:
                try:
                    print(row)
                    first_name = row[1]
                    last_name = row[2]
                    card_number = row[3]
                    phone = row[4]
                    birth_year = row[5]
                    birth_month = row[6]
                    birth_day = row[7]
                    intro = row[8]
                    new_member = Member(
                        first_name=first_name,
                        last_name=last_name,
                        card_number=card_number,
                        phone=phone,
                        year_of_birth=birth_year,
                        month_of_birth=birth_month,
                        day_of_birth=birth_day,
                        intro=intro,
                    )
                    new_member.save()
                except Exception as e:
                    print(e)

            return JsonResponse({"response_code": 2})

        except Exception as e:
            print(e)
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
