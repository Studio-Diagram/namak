from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
import json, jdatetime
from accounti.models import *
from random import randint
from accountiboard.constants import *

def do_lottery(lot_data):
    all_luck_points_sum = 0
    sum_list = []
    for lot in lot_data:
        all_luck_points_sum += int(lot['luck_points'])
        lot['numbers_luck'] = []
    for i in range(1, all_luck_points_sum + 1):
        sum_list.append(i)
    for lot in lot_data:
        for j in range(0, int(lot['luck_points'])):
            num_luck = randint(0, len(sum_list) - 1)
            lot['numbers_luck'].append(sum_list.pop(num_luck))

    if all_luck_points_sum == 0:
        return False
    final_winner_num_luck = randint(1, all_luck_points_sum)
    for lot in lot_data:
        if final_winner_num_luck in lot['numbers_luck']:
            final_winner_card_number = lot['card_number']
            return final_winner_card_number


class LotteryView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        start_date = rec_data.get('start_date')
        end_date = rec_data.get('end_date')
        prize = rec_data.get('prize')
        branch_id = rec_data.get('branch')
        if not start_date or not end_date or not prize or not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        organization_object = Branch.objects.get(id=branch_id).organization
        start_date_split = start_date.split('/')
        start_date_g = jdatetime.date(int(start_date_split[2]), int(start_date_split[1]),
                                      int(start_date_split[0])).togregorian()

        end_date_split = end_date.split('/')
        end_date_g = jdatetime.date(int(end_date_split[2]), int(end_date_split[1]),
                                    int(end_date_split[0])).togregorian()

        branches_this_organization = Branch.objects.filter(organization=organization_object)

        all_games = Game.objects.filter(branch__in=branches_this_organization, add_date__gte=start_date_g, add_date__lte=end_date_g).order_by('add_date').exclude(
            member=None)

        # all_games = Game.objects.filter(add_date__gte=start_date_g, add_date__lte=end_date_g).order_by('add_date').exclude(
        #     member=None)

        lottery_data = []
        for game in all_games:
            is_user_exist_lottery_data = False
            for lot in lottery_data:
                if game.member.card_number == lot['card_number']:
                    is_user_exist_lottery_data = True
                    if game.add_date in lot['days']:
                        lot['luck_points'] += float(game.points) * lot['multiplier'] / float(16)
                    else:
                        if lot['multiplier'] != 3:
                            lot['multiplier'] += 1
                        lot['days'].append(game.add_date)
                        lot['luck_points'] += float(game.points) * lot['multiplier'] / float(16)
            if not is_user_exist_lottery_data:
                lottery_data.append({
                    'card_number': game.member.card_number,
                    'multiplier': 1,
                    'days': [game.add_date],
                    'luck_points': float(game.points) / float(16)
                })
        winner = do_lottery(lottery_data)
        if winner:
            user = Member.objects.filter(card_number=winner).first()
            Lottery(user=user, prize=prize, start_date=start_date_g, end_date=end_date_g,
                              organization=organization_object).save()
        else:
            return JsonResponse({"response_code": 3, "error_msg": LOTTERY_CAN_NOT_BE_DONE})

        return JsonResponse({"response_code": 2})


class LotteryListView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch')

        organization_object = Branch.objects.get(id=branch_id).organization
        all_lot = Lottery.objects.filter(organization=organization_object).order_by("-id")[:100]
        all_lot_data = []
        for lot in all_lot:
            start_date = lot.start_date
            start_jalali_date = jdatetime.date.fromgregorian(day=start_date.day, month=start_date.month,
                                                             year=start_date.year)
            end_date = lot.end_date
            end_jalali_date = jdatetime.date.fromgregorian(day=end_date.day, month=end_date.month,
                                                           year=end_date.year)
            all_lot_data.append({
                'id': lot.pk,
                'start_date': start_jalali_date.strftime("%Y/%m/%d"),
                'end_date': end_jalali_date.strftime("%Y/%m/%d"),
                'name': lot.user.first_name + " " + lot.user.last_name,
                'prize': lot.prize,
                'is_give': lot.is_give_prize
            })

        return JsonResponse({"response_code": 2, "lotteries": all_lot_data})


class GivePrizeView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        lottery_id = rec_data.get('lottery_id')

        lot_obj = Lottery.objects.filter(pk=lottery_id).first()
        lot_obj.is_give_prize = 1
        lot_obj.save()

        return JsonResponse({"response_code": 2})
