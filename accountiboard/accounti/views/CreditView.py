from django.http import JsonResponse
import json
from datetime import datetime
from accounti.models import *
from django.db.models import Sum

DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'
INVOICE_NOT_EXIST = "فاکتور وجود ندارد."
MEMBER_NOT_SELCETD = "عضوی به این فاکتور وصل نشده است."
CREDIT_CATEGORY_NOT_HANDLED = "این دسته‌بندی برای اعتبار بررسی نشده است."
GAME_PER_POINT_PRICE = 5000


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

    if invoice_object.member.card_number == "0000":
        return JsonResponse({"response_code": 3, "error_msg": MEMBER_NOT_SELCETD})

    all_member_credits = Credit.objects.filter(member=invoice_object.member, expire_time__gte=datetime.now())
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
