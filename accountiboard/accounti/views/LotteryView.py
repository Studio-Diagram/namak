from django.http import JsonResponse
import json, jdatetime
from accounti.models import *
from random import randint

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def do_lottery(lot_data):
    print(lot_data)
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
    final_winner_num_luck = randint(1, all_luck_points_sum)
    for lot in lot_data:
        if final_winner_num_luck in lot['numbers_luck']:
            final_winner_card_number = lot['card_number']
            return final_winner_card_number


def lottery(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    start_date = rec_data['start_date']
    end_date = rec_data['end_date']
    prize = rec_data['prize']
    if not start_date or not end_date or not prize:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    start_date_split = start_date.split('/')
    start_date_g = jdatetime.date(int(start_date_split[2]), int(start_date_split[1]),
                                  int(start_date_split[0])).togregorian()

    end_date_split = end_date.split('/')
    end_date_g = jdatetime.date(int(end_date_split[2]), int(end_date_split[1]),
                                int(end_date_split[0])).togregorian()

    all_games = Game.objects.filter(add_date__gte=start_date_g, add_date__lte=end_date_g).order_by('add_date').exclude(
        member__card_number='0000')

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
    user = Member.objects.filter(card_number=winner).first()
    new_lot = Lottery(user=user, prize=prize, start_date=start_date_g, end_date=end_date_g)
    new_lot.save()

    return JsonResponse({"response_code": 2})


def lottery_list(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    all_lot = Lottery.objects.all().order_by("-id")[:100]
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


def give_prize(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    lottery_id = rec_data['lottery_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    lot_obj = Lottery.objects.filter(pk=lottery_id).first()
    lot_obj.is_give_prize = 1
    lot_obj.save()

    return JsonResponse({"response_code": 2})


def eslah(request):
    s = Supplier.objects.get(name="قنبر علی ( ما دمک سابق )")
    all_i_p = PurchaseToShopProduct.objects.filter(invoice_purchase__supplier=s)
    for i in all_i_p:
        if i.buy_numbers != i.unit_numbers:
            i.buy_numbers = i.unit_numbers
        i.save()
    return JsonResponse({"response_code": 2})
