from django.http import JsonResponse
import json
from accounti.models import *
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.db import IntegrityError
from accountiboard.constants import *
from accountiboard.custom_permissions import *


def add_member(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

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
    branch_id = rec_data.get('branch')

    method = "None"
    member_primary_key = 0

    if not first_name or not last_name or not card_number or not year_of_birth or not month_of_birth \
            or not day_of_birth or not phone or not intro or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if member_id == 0:
        organization_object = Branch.objects.get(id=branch_id).organization
        try:
            new_member = Member(
                first_name=first_name,
                last_name=last_name,
                card_number=card_number,
                year_of_birth=year_of_birth,
                month_of_birth=month_of_birth,
                day_of_birth=day_of_birth,
                phone=phone,
                intro=intro,
                organization=organization_object
            )
            new_member.save()

            method = "create"
            member_primary_key = new_member.pk

        except IntegrityError as e:
            if 'unique constraint' in e.args[0]:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

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

            method = "edit"
            member_primary_key = old_member.pk

        except IntegrityError as e:
            if 'unique constraint' in e.args[0]:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

    return JsonResponse({"response_code": 2, "created_member": {
        "last_name": last_name,
        "card_number": card_number,
        "method": method,
        "member_primary_key": member_primary_key
    }})


def get_members(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data.get('branch')
    organization_object = Branch.objects.get(id=branch_id).organization
    members = Member.objects.filter(organization=organization_object).order_by("-id")[:100]
    members_data = []
    for member in members:
        members_data.append({
            'id': member.pk,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'phone': member.phone,
            'card_number': member.card_number,
        })
    return JsonResponse({"response_code": 2, 'members': members_data})


def search_member(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    search_word = rec_data['search_word']
    username = rec_data['username']
    branch_id = rec_data['branch']
    organization_object = Branch.objects.get(id=branch_id).organization
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not search_word:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    items_searched = Member.objects.annotate(
        full_name=Concat('first_name', V(' '), 'last_name')).filter(
        full_name__contains=search_word, organization=organization_object)
    members = []
    for member in items_searched:
        members.append({
            'id': member.pk,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'phone': member.phone,
            'card_number': member.card_number,
        })
    return JsonResponse({"response_code": 2, 'members': members})


@permission_decorator(session_authenticate, {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER']})
def get_member(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data['branch']

    if rec_data.get('member_id'):
        member_id = rec_data['member_id']
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

    elif rec_data.get('card_number'):
        card_number = rec_data['card_number']
        card_number = card_number.replace("؟", "")
        card_number = card_number.replace("٪", "")
        card_number = card_number.replace("?", "")
        card_number = card_number.replace("%", "")
        
        organization_object = Branch.objects.get(id=branch_id).organization
        member = Member.objects.filter(card_number=card_number, organization=organization_object).first()
        if member:
            member_data = {
                'id': member.pk,
                'first_name': member.first_name,
                'last_name': member.last_name,
            }
            return JsonResponse({"response_code": 2, 'member': member_data})
        else:
            return JsonResponse({"response_code": 3, 'error_msg': MEMBER_NOT_FOUND})
