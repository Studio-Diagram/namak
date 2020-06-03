from django.http import JsonResponse
import json
from accounti.models import *
from datetime import datetime, timedelta
from accountiboard.constants import *


def add_branch(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    correct_mins = ["00", "15", "30", "45"]
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data.get('branch_id')
    name = rec_data.get('name')
    address = rec_data.get('address')
    start_time = rec_data.get('start_time')
    end_time = rec_data.get('end_time')
    min_paid_price = rec_data.get('min_paid_price')
    guest_pricing = rec_data.get('guest_pricing')
    game_data = rec_data.get('game_data')
    game_data_list = []
    # TODO: Adding Organization
    if not name or not address or not start_time or not end_time:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    if start_time.split(":")[1] not in correct_mins or end_time.split(":")[1] not in correct_mins:
        return JsonResponse({"response_code": 3, "error_msg": WRONG_TIME_REGEX})

    if game_data and min_paid_price:
        game_data_list = [json.dumps({
            "which_hour": game_data_object.get('which_hour'),
            "price_per_hour": game_data_object.get('price_per_hour')
        }) for game_data_object in game_data]

    if branch_id == 0:
        new_branch = Branch(
            name=name,
            address=address,
            start_working_time=datetime.strptime(start_time, '%H:%M'),
            end_working_time=datetime.strptime(end_time, '%H:%M'),
            min_paid_price=min_paid_price,
            game_data=game_data_list if game_data_list else None,
            guest_pricing=guest_pricing
        )
        new_branch.save()

        return JsonResponse({"response_code": 2})
    else:
        old_branch = Branch.objects.get(pk=branch_id)
        old_branch.name = name
        old_branch.address = address
        old_branch.start_working_time = datetime.strptime(start_time, '%H:%M')
        old_branch.end_working_time = datetime.strptime(end_time, '%H:%M')
        old_branch.min_paid_price = min_paid_price
        old_branch.game_data = game_data_list
        old_branch.guest_pricing = guest_pricing
        old_branch.save()
        return JsonResponse({"response_code": 2})


def get_branches(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    branches = Branch.objects.filter(organization=Branch.objects.get(pk=branch_id).organization)
    branches_data = []
    for branch in branches:
        branches_data.append({
            'id': branch.pk,
            'name': branch.name,
            'address': branch.address,
            'start_time': branch.start_working_time.strftime("%H:%M"),
            'end_time': branch.end_working_time.strftime("%H:%M")
        })
    return JsonResponse({"response_code": 2, 'branches': branches_data})


def search_branch(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']
        if not request.session.get('is_logged_in', None) == username:
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
                'start_time': branch.start_working_time.strftime("%H:%M"),
                'end_time': branch.end_working_time.strftime("%H:%M")
            })
        return JsonResponse({"response_code": 2, 'branches': branches})
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def get_branch(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    branch_id = rec_data['branch']
    branch = Branch.objects.get(pk=branch_id)
    branch_data = {
        'id': branch.pk,
        'name': branch.name,
        'address': branch.address,
        'start_time': branch.start_working_time.strftime("%H:%M"),
        'end_time': branch.end_working_time.strftime("%H:%M"),
        'game_data': [json.loads(game_data_single_object) for game_data_single_object in branch.game_data],
        'min_paid_price': branch.min_paid_price,
        'guest_pricing': branch.guest_pricing
    }
    return JsonResponse({"response_code": 2, 'branch': branch_data})


def get_working_time_for_reserve(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch']

    if not username:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not request.session.get('is_logged_in', None) == username:
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
