from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from datetime import datetime, timedelta
from django.views import View
from django.shortcuts import get_object_or_404


class AddBranchView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
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
                guest_pricing=guest_pricing,
                organization=CafeOwner.objects.get(user_id=request.payload.get('sub_id')).organization
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


class GetBranchesView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']
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


class SearchBranchView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = Branch.objects.filter(name__contains=search_word, organization=request.payload.get('sub_organization'))
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


class BranchView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS, branch_disable=True)
    def get(self, request, branch_id, *args, **kwargs):
        branch = get_object_or_404(Branch, pk=branch_id)
        branch_data = {
            'id': branch.pk,
            'name': branch.name,
            'address': branch.address,
            'start_working_time': branch.start_working_time.strftime("%H:%M"),
            'end_working_time': branch.end_working_time.strftime("%H:%M"),
            'game_data': [json.loads(game_data_single_object) for game_data_single_object in branch.game_data],
            'min_paid_price': branch.min_paid_price,
            'guest_pricing': branch.guest_pricing
        }
        return JsonResponse({'branch': branch_data})

    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def put(self, request, branch_id, *args, **kwargs):
        branch = get_object_or_404(Branch, pk=branch_id)
        allowed_keys = {'name', 'address', 'start_working_time', 'end_working_time',
                        'min_paid_price', 'guest_pricing', 'game_data'}
        rec_data = json.loads(request.read().decode('utf-8'))

        for key in rec_data:
            if key in allowed_keys:
                if key == 'start_working_time' or key == 'end_working_time':
                    setattr(branch, key, datetime.strptime(rec_data.get(key), '%H:%M'))
                elif key == "game_data":
                    setattr(branch, key, [json.dumps({
                        "which_hour": game_data_object.get('which_hour'),
                        "price_per_hour": game_data_object.get('price_per_hour')
                    }) for game_data_object in rec_data.get(key)])
                else:
                    setattr(branch, key, rec_data.get(key))

        branch.save()

        branch_data = {
            'id': branch.pk,
            'name': branch.name,
            'address': branch.address,
            'start_working_time': branch.start_working_time.strftime("%H:%M"),
            'end_working_time': branch.end_working_time.strftime("%H:%M"),
            'game_data': [json.loads(game_data_single_object) for game_data_single_object in branch.game_data],
            'min_paid_price': branch.min_paid_price,
            'guest_pricing': branch.guest_pricing
        }
        return JsonResponse({'branch': branch_data})


class GetWorkingTimeForReserveView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'],
                                       USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

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
