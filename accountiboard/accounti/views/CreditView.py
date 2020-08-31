from django.http import JsonResponse
import json
from datetime import datetime
from accounti.models import *
import jdatetime, random
from accountiboard.constants import *


def get_all_credits_data_from_user(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    member_id = rec_data['member_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    if not member_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    try:
        member_object = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return JsonResponse({"response_code": 3, "error_msg": MEMBER_NOT_EXIST})

    all_credit_data = []
    all_credits_from_user = Credit.objects.filter(member=member_object)
    for credit in all_credits_from_user:
        expire_jalali_date = jdatetime.date.fromgregorian(day=credit.expire_time.day, month=credit.expire_time.month,
                                                          year=credit.expire_time.year)
        start_jalali_date = jdatetime.date.fromgregorian(day=credit.start_time.day, month=credit.start_time.month,
                                                         year=credit.start_time.year)

        all_credit_data.append({
            "credit_categories": str(credit.credit_categories),
            "expire_date": expire_jalali_date.strftime("%Y/%m/%d"),
            "expire_time": credit.expire_time.strftime("%H:%M"),
            "start_date": start_jalali_date.strftime("%Y/%m/%d"),
            "start_time": credit.start_time.strftime("%H:%M"),
            "total_price": credit.total_price,
            "used_price": credit.used_price,
            "kind": credit.gift_code.gift_code_supplier.name if credit.gift_code else "دستی"
        })
    return JsonResponse({"response_code": 2, "all_credits": all_credit_data})


def create_credit(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    member_id = rec_data['member_id']
    credit_category = rec_data['credit_category']
    expire_date = rec_data['expire_date']
    expire_time = rec_data['expire_time']
    start_date = rec_data['start_date']
    start_time = rec_data['start_time']
    total_credit = rec_data['total_credit']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    if not credit_category or not expire_date or not expire_time or not total_credit or not start_time or not start_date:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    try:
        member_object = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return JsonResponse({"response_code": 3, "error_msg": MEMBER_NOT_EXIST})

    expire_date_split = expire_date.split('/')
    expire_time_split = expire_time.split(':')
    expire_date_g = jdatetime.datetime(int(expire_date_split[2]), int(expire_date_split[1]),
                                       int(expire_date_split[0]), int(expire_time_split[0]),
                                       int(expire_time_split[1]), 0).togregorian()

    start_date_split = start_date.split('/')
    start_time_split = start_time.split(':')
    start_date_g = jdatetime.datetime(int(start_date_split[2]), int(start_date_split[1]),
                                      int(start_date_split[0]), int(start_time_split[0]),
                                      int(start_time_split[1]), 0).togregorian()
    new_credit = Credit(member=member_object, total_price=total_credit, expire_time=expire_date_g,
                        start_time=start_date_g,
                        credit_categories=[credit_category])
    new_credit.save()
    return JsonResponse({"response_code": 2})


def perform_credit_on_invoice_sale(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    invoice_id = rec_data['invoice_id']
    used_credit_price = 0

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    try:
        invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    except InvoiceSales.DoesNotExist:
        return JsonResponse({"response_code": 3, "error_msg": INVOICE_NOT_EXIST})

    if not invoice_object.member:
        return JsonResponse({"response_code": 3, "error_msg": MEMBER_NOT_SELCETD})

    all_member_credits = Credit.objects.filter(member=invoice_object.member, expire_time__gte=datetime.now(),
                                               start_time__lte=datetime.now())
    for credit in all_member_credits:
        if credit.total_price == credit.used_price:
            continue

        used_credit_price = credit_handler(credit, invoice_object)
        if used_credit_price == "NO_CATEGORY":
            return JsonResponse({"response_code": 3, "error_msg": CREDIT_CATEGORY_NOT_HANDLED})

        if used_credit_price > 0:
            credit.used_price = used_credit_price
            credit.save()
            new_credit_to_invoice = CreditToInvoiceSale(credit=credit, invoice_sale=invoice_object,
                                                        used_price=used_credit_price)
            new_credit_to_invoice.save()

    return JsonResponse({"response_code": 2, 'used_credit': used_credit_price})


def credit_handler(credit_object, invoice_object):
    total_price_can_use_credit = 0
    total_credit = credit_object.total_price - credit_object.used_price
    for category in credit_object.credit_categories:
        if category == "BAR":
            total_price_can_use_credit += bar_credit_handler(invoice_object)
        elif category == "KITCHEN":
            total_price_can_use_credit += kitchen_credit_handler(invoice_object)
        elif category == "OTHER":
            total_price_can_use_credit += other_credit_handler(invoice_object)
        elif category == "SHOP":
            total_price_can_use_credit += shop_product_credit_handler(invoice_object)
        elif category == "GAME":
            total_price_can_use_credit += game_credit_handler(invoice_object)
        else:
            return "NO_CATEGORY"

    if total_credit >= total_price_can_use_credit:
        used_credit = total_price_can_use_credit
    else:
        used_credit = total_credit

    return used_credit


def bar_credit_handler(invoice_object):
    all_bar_item_to_invoice_sale = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object,
                                                                          menu_item__menu_category__kind="BAR")
    sum_all_items = 0
    for menu_item in all_bar_item_to_invoice_sale:
        sum_all_items += menu_item.numbers * int(menu_item.menu_item.price)

    return sum_all_items


def kitchen_credit_handler(invoice_object):
    all_kitchen_item_to_invoice_sale = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object,
                                                                              menu_item__menu_category__kind="KITCHEN")
    sum_all_items = 0
    for menu_item in all_kitchen_item_to_invoice_sale:
        sum_all_items += menu_item.numbers * int(menu_item.menu_item.price)

    return sum_all_items


def other_credit_handler(invoice_object):
    all_other_item_to_invoice_sale = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object,
                                                                            menu_item__menu_category__kind="OTHER")
    sum_all_items = 0
    for menu_item in all_other_item_to_invoice_sale:
        sum_all_items += menu_item.numbers * int(menu_item.menu_item.price)

    return sum_all_items


def shop_product_credit_handler(invoice_object):
    all_shop_item_to_invoice_sale = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_object)
    sum_all_items = 0
    for shop_p in all_shop_item_to_invoice_sale:
        sum_all_items += shop_p.numbers * shop_p.shop_product.price

    return sum_all_items


def game_credit_handler(invoice_object):
    all_game_item_to_invoice_sale = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object).exclude(
        game__end_time="00:00:00")
    sum_all_items = 0
    for game in all_game_item_to_invoice_sale:
        sum_all_items += game.game.points * GAME_PER_POINT_PRICE

    return sum_all_items


def check_gift_code(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    gift_code = rec_data['gift_code']
    gift_code = gift_code.lower()
    member_id = rec_data['member_id']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    if not gift_code:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    try:
        member_object = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return JsonResponse({"response_code": 3, "error_msg": MEMBER_NOT_EXIST})

    try:
        gift_code_object = GiftCode.objects.get(name=gift_code)
    except GiftCode.DoesNotExist:
        return JsonResponse({"response_code": 3, "error_msg": GIFT_CODE_NOT_EXIST})

    if not gift_code_object.number_will_use:
        return JsonResponse({"response_code": 3, "error_msg": GIFT_CODE_NOT_USABLE})

    if gift_code_object.expire_time < datetime.now():
        return JsonResponse({"response_code": 3, "error_msg": GIFT_CODE_NOT_USABLE})

    new_credit = Credit(member=member_object, total_price=gift_code_object.price,
                        expire_time=gift_code_object.expire_time,
                        credit_categories=gift_code_object.credit_categories, gift_code=gift_code_object)
    new_credit.save()
    gift_code_object.number_will_use -= 1
    gift_code_object.number_used += 1
    gift_code_object.save()
    return JsonResponse({"response_code": 2})


def create_gift_code_manual(request):
    if request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "POST REQUEST!"})
    s = "abcdefghijklmnopqrstuvwxyz0123456789"
    gift_len = 5
    code_supplier = GiftCodeSupplier.objects.get(name="پاندا")
    expire_date = jdatetime.datetime(1399, 6, 31, 23, 59, 59).togregorian()
    data = []

    for i in range(4):
        if i == 0:
            category = ["KITCHEN"]
            expensive_price = 500000
            mid_price = 350000
            cheap_price = 200000
        elif i == 1:
            category = ["BAR"]
            expensive_price = 400000
            mid_price = 300000
            cheap_price = 150000
        elif i == 2:
            category = ["GAME"]
            expensive_price = 250000
            mid_price = 150000
            cheap_price = 80000
        elif i == 3:
            category = ["SHOP"]
            expensive_price = 600000
            mid_price = 400000
            cheap_price = 200000
        else:
            break

        for hard in range(2):
            code = "".join(random.sample(s, gift_len))
            new_code = GiftCode(name=code, expire_time=expire_date, gift_code_supplier=code_supplier,
                                credit_categories=category, price=expensive_price)
            new_code.save()
            data.append({
                "code_name": code,
                "expire_date": expire_date,
                "kind": category,
                "price": expensive_price,
                "supplier": "PANDA"
            })
        for mid in range(3):
            code = "".join(random.sample(s, gift_len))
            new_code = GiftCode(name=code, expire_time=expire_date, gift_code_supplier=code_supplier,
                                credit_categories=category, price=mid_price)
            new_code.save()
            data.append({
                "code_name": code,
                "expire_date": expire_date,
                "kind": category,
                "price": mid_price,
                "supplier": "PANDA"
            })
        for easy in range(5):
            code = "".join(random.sample(s, gift_len))
            new_code = GiftCode(name=code, expire_time=expire_date, gift_code_supplier=code_supplier,
                                credit_categories=category, price=cheap_price)
            new_code.save()
            data.append({
                "code_name": code,
                "expire_date": expire_date,
                "kind": category,
                "price": cheap_price,
                "supplier": "PANDA"
            })

    return JsonResponse({"response_code": 2, "created": data})
