from django.http import JsonResponse
from django.shortcuts import render
import json, jdatetime
from accounti.models import *
from datetime import datetime, timedelta, date
from django.db.models import Sum
import logging

logger = logging.getLogger("accounti_info")
logger_specific_bug = logging.getLogger("specific_bug")
WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'
IN_GAME = "در حال بازی"
END_GAME = "بازی تمام شده"
WAIT_GAME = "منتظر بازی"
ORDERED = "سفارش داده"
NOT_ORDERED = "سفارش نداده"
DO_NOT_WANT_ORDER = "سفارش ندارد"
DO_NOT_WANT_GAME = "بازی نمی‌خواهد"
NO_SHOP_PRODUCTS_IN_STOCK = "محصول فروشی در انبار نیست."
WAIT_FOR_SETTLE = "منتظر تسویه"
PRICE_PER_POINT_IN_GAME = 5000
PRICE_PER_HOUR_IN_GAME = 100000
SECONDS_PER_POINT = 180
CHUNKS_PER_HOUR = 20
GUEST_LAST_NAME = "مهمان"
GUEST_FIRST_NAME = "مهمان"


def start_invoice_game(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch')
    invoice_id = rec_data.get('invoice_id')
    numbers = rec_data.get('numbers')
    card_number = rec_data.get('card_number')
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id or not numbers:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    if invoice_object.member:
        member_obj = invoice_object.member
    else:
        member_obj = Member.objects.get(card_number=card_number)
        invoice_object.member = member_obj

    new_game = Game(
        member=member_obj,
        start_time=datetime.strftime(datetime.now(), '%H:%M'),
        add_date=datetime.now(),
        numbers=numbers,
        branch_id=branch_id
    )
    new_game.save()
    new_invoice_to_game = InvoicesSalesToGame(
        game=new_game,
        invoice_sales=invoice_object
    )
    new_invoice_to_game.save()
    invoice_object.game_state = "PLAYING"
    invoice_object.save()

    return JsonResponse({"response_code": 2})


def change_game_state(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    invoice_id = rec_data['invoice_id']
    state = rec_data['state']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id or not state:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    invoice_object.game_state = state
    invoice_object.save()

    return JsonResponse({"response_code": 2})


def do_not_want_order(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    invoice_id = rec_data['invoice_id']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    invoice_object.is_do_not_want_order = True
    invoice_object.save()

    return JsonResponse({"response_code": 2})


def get_dashboard_quick_access_invoices(request):
    if not request.method == "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    cash_id = rec_data['cash_id']
    branch_id = rec_data['branch_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not cash_id or not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    branch_obj = Branch.objects.get(pk=branch_id)
    cash_obj = Cash.objects.get(pk=cash_id)

    all_invoices = InvoiceSales.objects.filter(branch=branch_obj, cash_desk=cash_obj, is_deleted=False,
                                               is_settled=False)
    playing_game_invoices_data = []
    wait_game_invoices_data = []
    end_game_invoices_data = []
    ordered_invoices_data = []
    not_order_invoices_data = []
    wait_for_settle_invoices_data = []
    for invoice in all_invoices:
        if invoice.game_state == "PLAYING":
            invoice_current_game = InvoicesSalesToGame.objects.filter(invoice_sales=invoice,
                                                                      game__end_time="00:00:00").first()
            playing_game_invoices_data.append({
                "customer_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                "numbers": invoice_current_game.game.numbers,
                "table_name": invoice.table.name,
                "game_id": invoice_current_game.game.pk
            })
        elif invoice.game_state == "END_GAME":
            end_game_invoices_data.append({
                "customer_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                "numbers": invoice.guest_numbers,
                "table_name": invoice.table.name,
                "invoice_id": invoice.pk
            })

        elif invoice.game_state == "WAIT_GAME":
            if not invoice.member:
                has_member = False
                card_number = ''
            else:
                has_member = True
                card_number = invoice.member.card_number

            wait_game_invoices_data.append({
                "customer_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                "numbers": invoice.guest_numbers,
                "table_name": invoice.table.name,
                "invoice_id": invoice.pk,
                "has_member": has_member,
                'member_name': invoice.member.first_name + " " + invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                "card_number": card_number,
                "player_numbers": 0
            })

        invoice_to_menu_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice).exclude(
            menu_item__menu_category__kind='OTHER')

        if invoice.ready_for_settle:
            wait_for_settle_invoices_data.append({
                "customer_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                "numbers": invoice.guest_numbers,
                "table_name": invoice.table.name,
                "invoice_id": invoice.pk,
                "total_price": invoice.total_price,
                "discount": invoice.discount,
                "tip": invoice.tip
            })
        else:
            if invoice_to_menu_items.count():
                ordered_invoices_data.append({
                    "customer_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                    "numbers": invoice.guest_numbers,
                    "table_name": invoice.table.name
                })
            else:
                if not invoice.is_do_not_want_order:
                    not_order_invoices_data.append({
                        "customer_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
                        "numbers": invoice.guest_numbers,
                        "table_name": invoice.table.name,
                        "invoice_id": invoice.pk
                    })

    return JsonResponse({"response_code": 2, "playing_game_invoices_data": playing_game_invoices_data,
                         "wait_game_invoices_data": wait_game_invoices_data,
                         "end_game_invoices_data": end_game_invoices_data,
                         "ordered_invoices_data": ordered_invoices_data,
                         "not_order_invoices_data": not_order_invoices_data,
                         "wait_for_settle_invoices_data": wait_for_settle_invoices_data})


def settle_invoice_sale(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    invoice_id = rec_data.get('invoice_id')
    cash = rec_data.get('cash')
    pos = rec_data.get('card')
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id or (not pos and not pos == 0) or (not cash and not cash == 0):
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    invoice_object.is_settled = 1
    invoice_object.cash = int(cash)
    invoice_object.pos = int(pos)
    invoice_object.settle_time = datetime.now()

    shop_products = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_object)
    for shop_product in shop_products:
        if get_detail_product_number(shop_product.shop_product.id) < int(shop_product.numbers):
            return JsonResponse({"response_code": 3, "error_msg": NO_SHOP_PRODUCTS_IN_STOCK})
    for shop_p in shop_products:
        shop_to_purchases = PurchaseToShopProduct.objects.filter(shop_product=shop_p.shop_product)
        unit_count = shop_p.numbers
        for purchase_to_shop in shop_to_purchases:
            if purchase_to_shop.buy_numbers + purchase_to_shop.return_numbers < purchase_to_shop.unit_numbers and unit_count != 0:
                buy_counter = 0
                for i in range(0, unit_count):
                    buy_counter += 1
                    purchase_to_shop.buy_numbers += 1
                    unit_count -= 1
                    purchase_to_shop.save()
                    if purchase_to_shop.buy_numbers == purchase_to_shop.unit_numbers:
                        break

                new_amani_sale = AmaniSale(invoice_sale_to_shop=shop_p,
                                           supplier=purchase_to_shop.invoice_purchase.supplier,
                                           sale_price=shop_p.shop_product.price,
                                           buy_price=purchase_to_shop.base_unit_price, created_date=datetime.now(),
                                           numbers=buy_counter)
                new_amani_sale.save()
                new_amani_to_purchase = AmaniSaleToInvoicePurchaseShopProduct(
                    amani_sale=new_amani_sale,
                    invoice_purchase_to_shop_product=purchase_to_shop,
                    numbers=buy_counter,
                )
                new_amani_to_purchase.save()

                if purchase_to_shop.invoice_purchase.settlement_type != "AMANi":
                    new_amani_sale.is_amani = False
                    new_amani_sale.save()

            elif unit_count == 0:
                break

    invoice_object.save()

    return JsonResponse({"response_code": 2})


def get_invoice(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    invoice_id = rec_data['invoice_id']
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    invoice_data = {
        'invoice_sales_id': invoice_object.pk,
        'table_id': invoice_object.table.pk,
        'table_name': invoice_object.table.name,
        'member_id': invoice_object.member.pk if invoice_object.member else 0,
        'guest_numbers': invoice_object.guest_numbers,
        'member_name': invoice_object.member.get_full_name() if invoice_object.member else GUEST_LAST_NAME,
        'member_data': invoice_object.member.get_full_name() if invoice_object.member else GUEST_LAST_NAME,
        'current_game': {
            'id': 0,
            'numbers': 0,
            'start_time': ''
        },
        'total_price': invoice_object.total_price,
        "discount": invoice_object.discount,
        "tip": invoice_object.tip,
        'menu_items_old': [],
        'shop_items_old': [],
        'games': [],
        'used_credit': 0,
        'total_credit': 0,
        'cash_amount': invoice_object.cash,
        "pos_amount": invoice_object.pos
    }
    invoice_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object)
    for game in invoice_games:
        if str(game.game.end_time) != "00:00:00":
            game_total_secs = (
                game.game.points / game.game.numbers * timedelta(seconds=SECONDS_PER_POINT)).total_seconds()
            hour_points = int(game_total_secs / 3600)
            min_points = int((game_total_secs / 60) % 60)
            if len(str(hour_points)) == 1:
                hour_points_string = "0" + str(hour_points)
            else:
                hour_points_string = str(hour_points)

            if len(str(min_points)) == 1:
                min_points_string = "0" + str(min_points)
            else:
                min_points_string = str(min_points)

            invoice_data['games'].append({
                'id': game.game.pk,
                'numbers': game.game.numbers,
                'start_time': game.game.start_time.strftime('%H:%M'),
                'end_time': game.game.end_time.strftime('%H:%M'),
                'points': "%s:%s'" % (hour_points_string, min_points_string),
                'total': game.game.points * PRICE_PER_POINT_IN_GAME
            })
        elif str(game.game.end_time) == "00:00:00":
            invoice_data['current_game']['id'] = game.game.pk
            invoice_data['current_game']['numbers'] = game.game.numbers
            invoice_data['current_game']['start_time'] = game.game.start_time

    invoice_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object)
    for item in invoice_items:
        invoice_data['menu_items_old'].append({
            'id': item.pk,
            'menu_item_id': item.menu_item_id,
            'name': item.menu_item.name,
            'price': item.menu_item.price,
            'nums': item.numbers,
            'total': int(item.menu_item.price) * int(item.numbers),
            'description': item.description
        })
    invoice_shops = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_object)
    for item in invoice_shops:
        invoice_data['shop_items_old'].append({
            'id': item.pk,
            'name': item.shop_product.name,
            'price': item.shop_product.price,
            'nums': item.numbers,
            'total': int(item.shop_product.price) * int(item.numbers),
            'description': item.description
        })

    sum_all_used_credit_on_this_invoice = CreditToInvoiceSale.objects.filter(invoice_sale=invoice_object).aggregate(
        Sum('used_price'))

    if sum_all_used_credit_on_this_invoice['used_price__sum']:
        invoice_data['used_credit'] = sum_all_used_credit_on_this_invoice['used_price__sum']

    if invoice_object.member:
        total_member_credit = Credit.objects.filter(member=invoice_object.member,
                                                    expire_time__gte=datetime.now()).aggregate(
            total_credit=(Sum('total_price') - Sum('used_price')))
        if total_member_credit['total_credit']:
            invoice_data['total_credit'] = total_member_credit['total_credit']

    return JsonResponse({"response_code": 2, "invoice": invoice_data})


def get_all_today_invoices(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data.get('username')
    branch_id = rec_data.get('branch_id')
    cash_id = rec_data.get('cash_id')

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not branch_id or not cash_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    all_invoices = InvoiceSales.objects.filter(branch_id=branch_id, cash_desk_id=cash_id, is_deleted=False).order_by(
        "is_settled")
    all_invoices_list = []
    for invoice in all_invoices:
        if invoice.settle_time:
            st_time = invoice.settle_time.time()
        else:
            st_time = 0

        invoice_to_menu_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice).exclude(
            menu_item__menu_category__kind='OTHER')

        if invoice.ready_for_settle:
            invoice_status = {"status": "WAIT_FOR_SETTLE", "text": WAIT_FOR_SETTLE}
        else:
            if invoice_to_menu_items.count():
                invoice_status = {"status": "ORDERED", "text": ORDERED}
            else:
                if invoice.is_do_not_want_order:
                    invoice_status = {"status": "DO_NOT_WANT_ORDER", "text": DO_NOT_WANT_ORDER}
                else:
                    invoice_status = {"status": "NOT_ORDERED", "text": NOT_ORDERED}

        sum_all_used_credit_on_this_invoice = CreditToInvoiceSale.objects.filter(
            invoice_sale=invoice).aggregate(
            Sum('used_price'))

        all_invoices_list.append({
            "invoice_id": invoice.pk,
            "guest_name": invoice.member.last_name if invoice.member else GUEST_LAST_NAME,
            "table_name": invoice.table.name,
            "guest_nums": invoice.guest_numbers,
            "total_price": invoice.total_price,
            "discount": invoice.discount,
            "tip": invoice.tip,
            "settle_time": st_time,
            "is_settled": invoice.is_settled,
            "game_status": {"status": invoice.game_state, "text": invoice.get_game_state_display()},
            "invoice_status": invoice_status,
            'used_credit': sum_all_used_credit_on_this_invoice['used_price__sum']
        })

    return JsonResponse({"response_code": 2, "all_today_invoices": all_invoices_list})


def get_menu_items_from_invoice_sales(invoice_sale_id):
    invoice_object = InvoiceSales.objects.get(pk=invoice_sale_id)
    menu_items_objects = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object)
    data = []
    for menu_item in menu_items_objects:
        data.append({
            'id': menu_item.menu_item.pk,
            'name': menu_item.menu_item.name,
            'price': menu_item.menu_item.price,
            'nums': menu_item.numbers,
            'total': menu_item.numbers * menu_item.menu_item.price,
            'description': menu_item.description
        })
    return data


def get_games_from_invoice_sales(invoice_sale_id):
    invoice_object = InvoiceSales.objects.get(pk=invoice_sale_id)
    games_objects = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object)
    data = []
    for game in games_objects:
        data.append({
            'start_time': game.game.start_time,
            'end_time': game.game.start_time,
            'credit_used': game.game.credit_used,
            'numbers': game.game.numbers,
            'points': game.game.points,
        })
    return data


def get_detail_product_number(shop_product_id):
    shop_product = ShopProduct.objects.get(id=shop_product_id)

    # All Shop Product in all Invoice Purchases
    sum_all_shop_p_numbers_invoice_purchases = PurchaseToShopProduct.objects.filter(
        shop_product=shop_product).aggregate(Sum('unit_numbers'))

    # All Shop Product in all Invoice return (Customer to Cafe)
    sum_all_shop_p_numbers_invoice_return_c_to_cafe = InvoiceReturn.objects.filter(
        shop_product=shop_product, return_type="CUSTOMER_TO_CAFE").aggregate(Sum('numbers'))

    # All Shop Products in Invoice return Cafe to Supplier
    sum_all_shop_p_numbers_invoice_return_cafe_to_s = InvoiceReturn.objects.filter(
        shop_product=shop_product, return_type="CAFE_TO_SUPPLIER").aggregate(Sum('numbers'))

    # All Shop Products in Amani Sales
    sum_all_shop_p_numbers_amani_sales = AmaniSale.objects.filter(
        invoice_sale_to_shop__shop_product=shop_product).aggregate(Sum('numbers'))

    if not sum_all_shop_p_numbers_invoice_purchases['unit_numbers__sum']:
        sum_all_shop_p_numbers_invoice_purchases['unit_numbers__sum'] = 0
    if not sum_all_shop_p_numbers_invoice_return_c_to_cafe['numbers__sum']:
        sum_all_shop_p_numbers_invoice_return_c_to_cafe['numbers__sum'] = 0
    if not sum_all_shop_p_numbers_invoice_return_cafe_to_s['numbers__sum']:
        sum_all_shop_p_numbers_invoice_return_cafe_to_s['numbers__sum'] = 0
    if not sum_all_shop_p_numbers_amani_sales['numbers__sum']:
        sum_all_shop_p_numbers_amani_sales['numbers__sum'] = 0

    real_shop_p_num = (sum_all_shop_p_numbers_invoice_purchases['unit_numbers__sum'] +
                       sum_all_shop_p_numbers_invoice_return_c_to_cafe[
                           'numbers__sum']) - (
                          sum_all_shop_p_numbers_invoice_return_cafe_to_s['numbers__sum'] +
                          sum_all_shop_p_numbers_amani_sales['numbers__sum'])

    return real_shop_p_num


def create_new_invoice_sales(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    invoice_sales_id = rec_data.get('invoice_sales_id')

    table_id = rec_data.get('table_id')
    member_id = rec_data.get('member_id')
    guest_numbers = rec_data.get('guest_numbers')
    current_game = rec_data.get('current_game')
    menu_items_new = rec_data.get('menu_items_new')
    shop_items_new = rec_data.get('shop_items_new')
    branch_id = rec_data.get('branch_id')
    cash_id = rec_data.get('cash_id')
    discount = rec_data.get('discount')
    tip = rec_data.get('tip')

    new_game_id = current_game.get('id')

    member_obj = None
    if member_id:
        member_obj = Member.objects.get(pk=member_id)

    if invoice_sales_id == 0:
        if tip == "" or discount == "":
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if not table_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if not guest_numbers and not guest_numbers == 0:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        for shop_p in shop_items_new:
            shop_obj = ShopProduct.objects.get(pk=shop_p['id'])
            if get_detail_product_number(shop_obj.id) < int(shop_p['nums']):
                return JsonResponse({"response_code": 3, "error_msg": NO_SHOP_PRODUCTS_IN_STOCK})

        cash_obj = Cash.objects.get(pk=cash_id)

        branch_obj = Branch.objects.get(pk=branch_id)
        table_obj = Table.objects.get(pk=table_id)

        new_invoice = InvoiceSales(
            branch=branch_obj,
            table=table_obj,
            guest_numbers=guest_numbers,
            created_time=datetime.now(),
            cash_desk=cash_obj,
            discount=discount,
            tip=tip,
            member=member_obj
        )

        new_invoice.save()

        new_invoice_id = new_invoice.pk
        if current_game['start_time']:
            new_game = Game(
                member=member_obj,
                start_time=datetime.strptime(current_game['start_time'], '%H:%M'),
                add_date=datetime.now(),
                numbers=current_game['numbers'],
                branch=branch_obj
            )
            new_game.save()
            new_game_id = new_game.pk
            new_invoice_to_game = InvoicesSalesToGame(
                game=new_game,
                invoice_sales=new_invoice
            )
            new_invoice_to_game.save()
            new_invoice.game_state = "PLAYING"
        for item in menu_items_new:
            item_obj = MenuItem.objects.get(pk=item['id'])
            new_item_to_invoice = InvoicesSalesToMenuItem(
                invoice_sales=new_invoice,
                menu_item=item_obj,
                numbers=item['nums'],
                description=item['description']
            )
            new_item_to_invoice.save()
            new_invoice.total_price += int(item_obj.price) * int(item['nums'])

        for shop in shop_items_new:
            shop_obj = ShopProduct.objects.get(pk=shop['id'])
            new_item_to_invoice = InvoicesSalesToShopProducts(
                invoice_sales=new_invoice,
                shop_product=shop_obj,
                numbers=shop['nums'],
                description=shop['description']
            )
            new_item_to_invoice.save()
            new_invoice.total_price += int(shop_obj.price) * int(shop['nums'])

        new_invoice.save()
        valid_total_price = get_invoice_sale_total_price(new_invoice.id)
        if valid_total_price != new_invoice.total_price:
            new_invoice.total_price = valid_total_price
            new_invoice.save()
            logger_specific_bug.info('%s : [WrongTotalPrice] Body field is: %s', str(datetime.now()), str(rec_data))
        logger.info('%s : [CreateNewInvoiceSale] Body field is: %s', str(datetime.now()), str(rec_data))
        return JsonResponse({"response_code": 2, "new_game_id": new_game_id, "new_invoice_id": new_invoice_id})

    elif invoice_sales_id != 0:
        if tip == "" or discount == "":
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        table_obj = Table.objects.get(pk=table_id)

        for shop_p in shop_items_new:
            shop_obj = ShopProduct.objects.get(pk=shop_p['id'])
            if get_detail_product_number(shop_obj.id) < int(shop_p['nums']):
                return JsonResponse({"response_code": 3, "error_msg": NO_SHOP_PRODUCTS_IN_STOCK})

        old_invoice = InvoiceSales.objects.get(pk=invoice_sales_id)
        old_invoice.table = table_obj
        old_invoice.guest_numbers = guest_numbers
        old_invoice.member = member_obj

        if current_game['id'] == 0 and current_game['start_time']:
            new_game = Game(
                member=member_obj,
                start_time=datetime.strptime(current_game['start_time'], '%H:%M'),
                add_date=datetime.now(),
                numbers=current_game['numbers'],
                branch=branch_obj
            )
            new_game.save()
            new_game_id = new_game.pk
            new_invoice_to_game = InvoicesSalesToGame(
                game=new_game,
                invoice_sales=old_invoice
            )
            new_invoice_to_game.save()
            old_invoice.game_state = "PLAYING"

        for item in menu_items_new:
            item_obj = MenuItem.objects.get(pk=item['id'])
            new_item_to_invoice = InvoicesSalesToMenuItem(
                invoice_sales=old_invoice,
                menu_item=item_obj,
                numbers=item['nums'],
                description=item['description']
            )
            new_item_to_invoice.save()
            old_invoice.total_price += int(item_obj.price) * int(item['nums'])

        for shop in shop_items_new:
            shop_obj = ShopProduct.objects.get(pk=shop['id'])
            new_item_to_invoice = InvoicesSalesToShopProducts(
                invoice_sales=old_invoice,
                shop_product=shop_obj,
                numbers=shop['nums'],
                description=shop['description']
            )

            new_item_to_invoice.save()
            old_invoice.total_price += int(shop_obj.price) * int(shop['nums'])

        old_invoice.discount = discount
        old_invoice.tip = tip
        old_invoice.save()
        new_invoice_id = old_invoice.pk
        valid_total_price = get_invoice_sale_total_price(old_invoice.id)
        if valid_total_price != old_invoice.total_price:
            old_invoice.total_price = valid_total_price
            old_invoice.save()
            logger_specific_bug.info('%s : [EditInvoiceSaleWrongTotalPRICE] Body field is: %s', str(datetime.now()),
                                     str(rec_data))
        logger.info('%s : [EditInvoiceSale] Body field is: %s', str(datetime.now()), str(rec_data))
        return JsonResponse({"response_code": 2, "new_game_id": new_game_id, "new_invoice_id": new_invoice_id})


def get_invoice_sale_total_price(invoice_id):
    total_price = 0
    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    all_invoice_to_menu_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object)
    for invoice_to_menu_item in all_invoice_to_menu_items:
        total_price += invoice_to_menu_item.numbers * int(invoice_to_menu_item.menu_item.price)

    all_invoice_to_shop_products = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_object)
    for invoice_to_shop_product in all_invoice_to_shop_products:
        total_price += invoice_to_shop_product.numbers * int(invoice_to_shop_product.shop_product.price)

    all_invoice_sales_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object).exclude(game__points=0)
    for invoice_to_game in all_invoice_sales_games:
        total_price += invoice_to_game.game.points * PRICE_PER_POINT_IN_GAME

    return total_price


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


def end_current_game(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    game_id = rec_data['game_id']
    end_time = datetime.now().time()
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not game_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    game_object = Game.objects.get(pk=game_id, end_time="00:00:00")
    invoice_to_sales_object = InvoicesSalesToGame.objects.get(game=game_object)
    invoice_id = invoice_to_sales_object.invoice_sales.pk
    invoice_object = InvoiceSales.objects.get(pk=invoice_id)
    start_time = game_object.start_time
    game_object.end_time = end_time

    timedelta_start = timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)

    timedelta_end = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)

    t = timedelta_end - timedelta_start
    point = int(round(t.total_seconds() / SECONDS_PER_POINT))
    if not game_object.member:
        if point % CHUNKS_PER_HOUR != 0:
            point = (int(point / CHUNKS_PER_HOUR) + 1) * CHUNKS_PER_HOUR
    game_numbers = game_object.numbers

    game_object.points = point * game_numbers
    game_object.save()
    invoice_object.total_price += point * game_numbers * PRICE_PER_POINT_IN_GAME
    invoice_object.game_state = "END_GAME"
    invoice_object.save()
    return JsonResponse({"response_code": 2})


def get_all_invoice_games(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        invoice_id = rec_data['invoice_id']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        else:
            invoice_object = InvoiceSales.objects.get(pk=invoice_id)
            invoice_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object)
            games = []
            for game in invoice_games:
                if str(game.game.end_time) != "00:00:00":
                    game_total_secs = (
                        game.game.points / game.game.numbers * timedelta(seconds=SECONDS_PER_POINT)).total_seconds()
                    hour_points = int(game_total_secs / 3600)
                    min_points = int((game_total_secs / 60) % 60)
                    if len(str(hour_points)) == 1:
                        hour_points_string = "0" + str(hour_points)
                    else:
                        hour_points_string = str(hour_points)

                    if len(str(min_points)) == 1:
                        min_points_string = "0" + str(min_points)
                    else:
                        min_points_string = str(min_points)
                    games.append({
                        'id': game.game.pk,
                        'numbers': game.game.numbers,
                        'start_time': game.game.start_time,
                        'end_time': game.game.end_time,
                        'points': "%s:%s'" % (hour_points_string, min_points_string),
                        'total': game.game.points * PRICE_PER_POINT_IN_GAME
                    })
            return JsonResponse({"response_code": 2, 'games': games})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def delete_items(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        invoice_id = rec_data['invoice_id']
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        else:
            invoice_object = InvoiceSales.objects.get(pk=invoice_id)
            employee = Employee.objects.get(phone=username)
            shops = rec_data['shop']
            menus = rec_data['menu']
            games = rec_data['game']
            message = rec_data['message']
            if not message:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not len(shops) and not len(menus) and not len(games):
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            for shop_id in shops:
                shop_product_obj = InvoicesSalesToShopProducts.objects.get(pk=shop_id)
                new_deleted = DeletedItemsInvoiceSales(
                    created_time=datetime.now(),
                    item_type="SHOP",
                    item_numbers=shop_product_obj.numbers,
                    message=message,
                    invoice_sales=invoice_object,
                    employee=employee
                )
                new_deleted.save()
                invoice_object.total_price -= int(shop_product_obj.shop_product.price) * int(shop_product_obj.numbers)
                invoice_object.save()
                shop_product_obj.delete()
            for menu_id in menus:
                menu_item_obj = InvoicesSalesToMenuItem.objects.get(pk=menu_id)
                new_deleted = DeletedItemsInvoiceSales(
                    created_time=datetime.now(),
                    item_type="MENU",
                    item_numbers=menu_item_obj.numbers,
                    message=message,
                    invoice_sales=invoice_object,
                    employee=employee
                )
                new_deleted.save()
                invoice_object.total_price -= int(menu_item_obj.menu_item.price) * int(menu_item_obj.numbers)
                invoice_object.save()
                menu_item_obj.delete()
            for game_id in games:
                game_obj = InvoicesSalesToGame.objects.get(pk=game_id)
                new_deleted = DeletedItemsInvoiceSales(
                    created_time=datetime.now(),
                    item_type="GAME",
                    item_numbers=game_obj.game.points,
                    message=message,
                    invoice_sales=invoice_object,
                    employee=employee
                )
                new_deleted.save()
                invoice_object.total_price -= int(game_obj.game.points) * PRICE_PER_POINT_IN_GAME
                invoice_object.save()
                game_obj.delete()

            return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_today_status(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    cash_id = rec_data['cash_id']

    branch_obj = Branch.objects.get(pk=branch_id)
    cash_obj = Cash.objects.filter(pk=cash_id, branch=branch_obj).first()

    now_date = datetime.now().date()
    now_time = datetime.now().time()

    datetime_object_3am = datetime.strptime('03:00:00', '%H:%M:%S')
    time3am = datetime.time(datetime_object_3am)

    datetime_object_0am = datetime.strptime('00:00:00', '%H:%M:%S')
    time0am = datetime.time(datetime_object_0am)

    yesterday = date.today() - timedelta(1)

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not cash_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    status = {
        "all_sales_price": 0,
        "all_cash": 0,
        "all_pos": 0,
        "all_guests": 0,
        "all_tax": 0,
        "all_discount": 0,
        "all_tip": 0,
        "all_bar": 0,
        "all_kitchen": 0,
        "all_other": 0,
        "all_purchase": 0,
        "all_expense": 0,
        "all_pays": 0,
        "all_games": 0,
        "all_sales": 0,
    }

    all_invoices = InvoiceSales.objects.filter(cash_desk=cash_obj, is_deleted=False)
    for invoice in all_invoices:
        status['all_sales_price'] += invoice.total_price
        status['all_cash'] += invoice.cash
        status['all_pos'] += invoice.pos
        status['all_guests'] += invoice.guest_numbers
        status['all_tax'] += invoice.tax
        status['all_discount'] += invoice.discount
        status['all_tip'] += invoice.tip
        all_invoice_menu_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice)
        for invoice_to_menu_item in all_invoice_menu_items:
            if invoice_to_menu_item.menu_item.menu_category.kind == "BAR":
                status['all_bar'] += invoice_to_menu_item.numbers * int(invoice_to_menu_item.menu_item.price)
            elif invoice_to_menu_item.menu_item.menu_category.kind == "KITCHEN":
                status['all_kitchen'] += invoice_to_menu_item.numbers * int(invoice_to_menu_item.menu_item.price)
            elif invoice_to_menu_item.menu_item.menu_category.kind == "OTHER":
                status['all_other'] += invoice_to_menu_item.numbers * int(invoice_to_menu_item.menu_item.price)

        all_invoice_shop_products = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice)
        for invoice_to_shop_p in all_invoice_shop_products:
            all_amani_sale = AmaniSale.objects.filter(invoice_sale_to_shop=invoice_to_shop_p)
            for amani_sale in all_amani_sale:
                status['all_sales'] += amani_sale.numbers * amani_sale.sale_price

        all_invoice_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice)
        for invoice_to_game in all_invoice_games:
            status['all_games'] += invoice_to_game.game.points * PRICE_PER_POINT_IN_GAME

    if now_time > time3am:
        all_invoice_purchase = InvoicePurchase.objects.filter(branch=branch_obj, created_time__date=now_date)
        for invoice in all_invoice_purchase:
            if invoice.created_time.time() > time3am:
                status['all_purchase'] += invoice.total_price

        all_invoice_expense = InvoiceExpense.objects.filter(branch=branch_obj, created_time__date=now_date)
        for invoice in all_invoice_expense:
            if invoice.created_time.time() > time3am:
                status['all_expense'] += invoice.price

        all_invoice_pays = InvoiceSettlement.objects.filter(branch=branch_obj, created_time__date=now_date)
        for invoice in all_invoice_pays:
            if invoice.created_time.time() > time3am:
                status['all_pays'] += invoice.payment_amount

    elif time0am < now_time < time3am:
        all_invoice_purchase_y = InvoicePurchase.objects.filter(branch=branch_obj, created_time__date=yesterday)
        for invoice in all_invoice_purchase_y:
            if invoice.created_time.time() > time3am:
                status['all_purchase'] += invoice.total_price

        all_invoice_purchase_t = InvoicePurchase.objects.filter(branch=branch_obj, created_time__date=now_date)
        for invoice in all_invoice_purchase_t:
            status['all_purchase'] += invoice.total_price

        all_invoice_expense_y = InvoiceExpense.objects.filter(branch=branch_obj, created_time__date=yesterday)
        for invoice in all_invoice_expense_y:
            if invoice.created_time.time() > time3am:
                status['all_expense'] += invoice.price

        all_invoice_expense_t = InvoiceExpense.objects.filter(branch=branch_obj, created_time__date=now_date)
        for invoice in all_invoice_expense_t:
            status['all_expense'] += invoice.price

        all_invoice_pays_y = InvoiceSettlement.objects.filter(branch=branch_obj, created_time__date=yesterday)
        for invoice in all_invoice_pays_y:
            if invoice.created_time.time() > time3am:
                status['all_pays'] += invoice.payment_amount

        all_invoice_pays_t = InvoiceSettlement.objects.filter(branch=branch_obj, created_time__date=now_date)
        for invoice in all_invoice_pays_t:
            status['all_pays'] += invoice.payment_amount

    return JsonResponse({"response_code": 2, "all_today_status": status})


def get_kitchen_sail_detail(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    cash_id = rec_data['cash_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not branch_id or not cash_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    branch_obj = Branch.objects.get(pk=branch_id)
    cash_obj = Cash.objects.filter(pk=cash_id, branch=branch_obj).first()
    sale_details = []

    all_invoices_menu_items_kitchen = InvoicesSalesToMenuItem.objects.filter(invoice_sales__is_deleted=False,
                                                                             invoice_sales__cash_desk=cash_obj,
                                                                             menu_item__menu_category__kind="KITCHEN").order_by(
        "menu_item__name")

    for menu_item in all_invoices_menu_items_kitchen:
        found_item = list(filter(lambda item: item['name'] == menu_item.menu_item.name, sale_details))
        if found_item:
            found_item[0]['numbers'] += menu_item.numbers
        else:
            sale_details.append({
                "name": menu_item.menu_item.name,
                "numbers": menu_item.numbers
            })

    sale_details = sorted(sale_details, key=lambda i: i['numbers'], reverse=True)
    return JsonResponse({"response_code": 2, "sale_details": sale_details})


def get_bar_sail_detail(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    cash_id = rec_data['cash_id']
    menu_category_id = rec_data['menu_category_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not branch_id or not cash_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    branch_obj = Branch.objects.get(pk=branch_id)
    cash_obj = Cash.objects.filter(pk=cash_id, branch=branch_obj).first()
    sale_details = []

    all_invoices_menu_items_bar = InvoicesSalesToMenuItem.objects.filter(invoice_sales__is_deleted=False,
                                                                         invoice_sales__cash_desk=cash_obj,
                                                                         menu_item__menu_category__kind="BAR").order_by(
        "menu_item__name")

    if menu_category_id:
        all_invoices_menu_items_bar = all_invoices_menu_items_bar.filter(menu_item__menu_category__id=menu_category_id)

    for menu_item in all_invoices_menu_items_bar:
        found_item = list(filter(lambda item: item['name'] == menu_item.menu_item.name, sale_details))
        if found_item:
            found_item[0]['numbers'] += menu_item.numbers
        else:
            sale_details.append({
                "name": menu_item.menu_item.name,
                "Category_name": menu_item.menu_item.menu_category.name,
                "numbers": menu_item.numbers
            })

    sale_details = sorted(sale_details, key=lambda i: i['numbers'], reverse=True)
    return JsonResponse({"response_code": 2, "sale_details": sale_details})


def get_other_sail_detail(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    cash_id = rec_data['cash_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not branch_id or not cash_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    branch_obj = Branch.objects.get(pk=branch_id)
    cash_obj = Cash.objects.filter(pk=cash_id, branch=branch_obj).first()
    sale_details = []

    all_invoices_menu_items_other = InvoicesSalesToMenuItem.objects.filter(invoice_sales__is_deleted=False,
                                                                           invoice_sales__cash_desk=cash_obj,
                                                                           menu_item__menu_category__kind="OTHER").order_by(
        "menu_item__name")

    for menu_item in all_invoices_menu_items_other:
        found_item = list(filter(lambda item: item['name'] == menu_item.menu_item.name, sale_details))
        if found_item:
            found_item[0]['numbers'] += menu_item.numbers
        else:
            sale_details.append({
                "name": menu_item.menu_item.name,
                "numbers": menu_item.numbers
            })

    sale_details = sorted(sale_details, key=lambda i: i['numbers'], reverse=True)

    return JsonResponse({"response_code": 2, "sale_details": sale_details})


def calec_time(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        start_time = rec_data['start_time']
        end_time = datetime.now()
        timedelta_start = timedelta(hours=int(start_time.split(":")[0]), minutes=int(start_time.split(":")[1]),
                                    seconds=0)
        timedelta_end = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)
        t = timedelta_end - timedelta_start
        point = int(round(t.total_seconds() / SECONDS_PER_POINT))
        return JsonResponse({"response_code": 2, 'price': point * PRICE_PER_POINT_IN_GAME})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def print_after_save(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        activate_is_print = rec_data['activate_is_print']
        invoice_obj = InvoiceSales.objects.get(pk=invoice_id)
        print_data = {
            'is_customer_print': 0,
            'invoice_id': invoice_obj.pk,
            'table_name': invoice_obj.table.name,
            'data': []
        }
        all_printers = Printer.objects.all().order_by("id")
        for printer in all_printers:
            print_data['data'].append({
                'printer_name': printer.name,
                'items': []
            })
        all_menu_item_invoice = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_obj, is_print=0)
        for menu_item in all_menu_item_invoice:
            printer_obj = PrinterToCategory.objects.filter(menu_category=menu_item.menu_item.menu_category)
            for printer in printer_obj:
                for real_printer in print_data['data']:
                    if real_printer['printer_name'] == printer.printer.name:
                        real_printer['items'].append({
                            'name': menu_item.menu_item.name,
                            'numbers': menu_item.numbers,
                            'description': menu_item.description,
                            'price': int(menu_item.menu_item.price) * int(menu_item.numbers)
                        })
                        break

                if activate_is_print:
                    menu_item.is_print = 1
                    menu_item.save()

        return JsonResponse({"response_code": 2, 'printer_data': print_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def print_cash(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    print_data = {
        'is_customer_print': 1,
        'invoice_id': '',
        'table_name': '',
        'customer_name': '',
        'printers': ['Cash'],
        'items': []
    }
    invoice_id = rec_data['invoice_id']
    invoice_obj = InvoiceSales.objects.get(pk=invoice_id)
    print_data['customer_name'] = invoice_obj.member.last_name if invoice_obj.member else GUEST_LAST_NAME
    print_data['invoice_id'] = invoice_obj.pk
    print_data['table_name'] = invoice_obj.table.name
    all_menu_item_invoice = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_obj)
    for menu_item in all_menu_item_invoice:
        print_data['items'].append({
            'name': menu_item.menu_item.name,
            'numbers': menu_item.numbers,
            'item_price': menu_item.menu_item.price,
            'price': int(menu_item.menu_item.price) * int(menu_item.numbers)
        })
    all_game_invoice = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_obj)
    for game in all_game_invoice:
        print_data['items'].append({
            'name': 'بازی',
            'numbers': game.game.numbers,
            'item_price': PRICE_PER_POINT_IN_GAME,
            'price': game.game.points * PRICE_PER_POINT_IN_GAME
        })
    all_shop_invoice = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_obj)
    for shop_p in all_shop_invoice:
        print_data['items'].append({
            'name': shop_p.shop_product.name,
            'numbers': shop_p.numbers,
            'item_price': shop_p.shop_product.price,
            'price': shop_p.numbers * shop_p.shop_product.price
        })
    return JsonResponse({"response_code": 2, 'printer_data': print_data})


def print_cash_with_template(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    now_time = jdatetime.datetime.now()
    print_data = {
        'is_customer_print': 1,
        'invoice_id': '',
        'factor_number': '',
        'table_name': '',
        'customer_name': '',
        'printers': ['Cash'],
        'items': [],
        'total_price': '',
        'service': 0,
        'tax': 0,
        'discount': 0,
        'payable': 0,
        'time': now_time.strftime("%H:%M"),
        'date': now_time.strftime("%Y/%m/%d"),
    }
    invoice_id = request.GET['invoice_id']
    invoice_obj = InvoiceSales.objects.get(pk=invoice_id)
    print_data['customer_name'] = invoice_obj.member.last_name if invoice_obj.member else GUEST_LAST_NAME
    print_data['invoice_id'] = invoice_obj.pk
    print_data['factor_number'] = invoice_obj.pk * 1234
    print_data['table_name'] = invoice_obj.table.name
    print_data['total_price'] = format(int(invoice_obj.total_price), ',d')
    print_data['discount'] = format(int(invoice_obj.discount), ',d')
    print_data['payable'] = format(int(invoice_obj.total_price - invoice_obj.discount), ',d')
    all_menu_item_invoice = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_obj)
    for menu_item in all_menu_item_invoice:
        is_append = False
        for item in print_data['items']:
            if menu_item.menu_item.pk == item['item_id'] and item['item_kind'] == "MENU":
                item['numbers'] += menu_item.numbers
                item['price'] += int(menu_item.menu_item.price) * int(menu_item.numbers)
                is_append = True
                break
        if not is_append:
            print_data['items'].append({
                'item_id': menu_item.menu_item.pk,
                'item_kind': 'MENU',
                'name': menu_item.menu_item.name,
                'numbers': menu_item.numbers,
                'item_price': format(int(menu_item.menu_item.price), ',d'),
                'price': int(menu_item.menu_item.price) * int(menu_item.numbers)
            })

    all_game_invoice = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_obj)
    for game in all_game_invoice:
        game_total_secs = (
            game.game.points / game.game.numbers * timedelta(seconds=SECONDS_PER_POINT)).total_seconds()
        hour_points = int(game_total_secs / 3600)
        min_points = int((game_total_secs / 60) % 60)
        if len(str(hour_points)) == 1:
            hour_points_string = "0" + str(hour_points)
        else:
            hour_points_string = str(hour_points)

        if len(str(min_points)) == 1:
            min_points_string = "0" + str(min_points)
        else:
            min_points_string = str(min_points)

        print_data['items'].append({
            'item_id': game.game.pk,
            'item_kind': 'GAME',
            'name': 'بازی %d نفره' % game.game.numbers,
            'numbers': "%s:%s'" % (hour_points_string, min_points_string),
            'item_price': format(int(PRICE_PER_HOUR_IN_GAME) * game.game.numbers, ',d'),
            'price': int(game.game.points * PRICE_PER_POINT_IN_GAME)
        })
    all_shop_invoice = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_obj)
    for shop_p in all_shop_invoice:
        is_append = False
        for item in print_data['items']:
            if shop_p.shop_product.pk == item['item_id'] and item['item_kind'] == "SHOP":
                item['numbers'] += shop_p.numbers
                item['price'] += int(shop_p.shop_product.price) * int(shop_p.numbers)
                is_append = True
                break
        if not is_append:
            print_data['items'].append({
                'item_id': shop_p.shop_product.pk,
                'item_kind': 'SHOP',
                'name': shop_p.shop_product.name,
                'numbers': shop_p.numbers,
                'item_price': format(int(shop_p.shop_product.price), ',d'),
                'price': int(shop_p.numbers * shop_p.shop_product.price)
            })

    for price_item in print_data['items']:
        price_item['price'] = format(price_item['price'], ",d")
    return render(request, "invoice_cash.html", {"invoice_data": print_data})


def print_after_save_template(request):
    if request.method == "GET":
        now_time = jdatetime.datetime.now()
        invoice_id = request.GET['invoice_id']
        printer_name = request.GET['printer_name']
        invoice_obj = InvoiceSales.objects.get(pk=invoice_id)
        print_data = {
            'is_customer_print': 0,
            'invoice_id': invoice_obj.pk,
            'factor_number': invoice_obj.pk * 1234,
            'printer_name': printer_name,
            'table_name': invoice_obj.table.name,
            'customer_name': invoice_obj.member.last_name if invoice_obj.member else GUEST_LAST_NAME,
            'guest_numbers': invoice_obj.guest_numbers,
            'time': now_time.strftime("%H:%M"),
            'date': now_time.strftime("%Y/%m/%d"),
            'items': []
        }
        all_menu_item_invoice = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_obj, is_print=0).order_by(
            'menu_item__menu_category__kind')
        for menu_item in all_menu_item_invoice:
            printer_obj = PrinterToCategory.objects.filter(menu_category=menu_item.menu_item.menu_category)
            for printer in printer_obj:
                if printer_name == printer.printer.name:
                    print_data['items'].append({
                        'name': menu_item.menu_item.name,
                        'numbers': menu_item.numbers,
                        'description': menu_item.description,
                        'price': int(menu_item.menu_item.price) * int(menu_item.numbers)
                    })
                    break

        return render(request, 'invoice_not_cash.html', {'invoice_data': print_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def ready_for_settle(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    invoice_id = rec_data['invoice_id']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    invoice_obj = InvoiceSales.objects.filter(id=invoice_id).first()
    invoice_obj.ready_for_settle = True
    invoice_obj.save()
    return JsonResponse({"response_code": 2})


def delete_invoice(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    branch_id = rec_data['branch_id']
    invoice_id = rec_data['invoice_id']
    description = rec_data['description']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    invoice_obj = InvoiceSales.objects.filter(id=invoice_id).first()
    invoice_obj.is_deleted = True

    new_invoice_deleted = DeletedInvoiceSale(
        invoice_sale=invoice_obj,
        description=description,
    )
    new_invoice_deleted.save()
    invoice_obj.save()
    return JsonResponse({"response_code": 2})


def get_all_invoices_with_date(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    data_list = []
    all_invoices = InvoiceSales.objects.filter(created_time__gte=datetime.strptime("10/5/2019", '%m/%d/%Y'))
    for item in all_invoices:
        shops_list = []
        all_shops = InvoicesSalesToShopProducts.objects.filter(invoice_sales=item)
        for shop in all_shops:
            shops_list.append({
                "shop_name": shop.shop_product.name,
                "shop_price": shop.shop_product.price,
                "shop_number": shop.numbers,
            })
        if len(all_shops) > 0:
            data_list.append({
                "invoice_number": item.pk,
                "shop_products": shops_list
            })
    return JsonResponse({"response_code": 2, "data": data_list})


def edit_payment_invoice_sale(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']
    invoice_data = rec_data['invoice_data']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
    if not invoice_data:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

    invoice_obj = InvoiceSales.objects.get(id=invoice_data['invoice_id'])
    invoice_obj.cash = invoice_data['cash']
    invoice_obj.pos = invoice_data['pos']
    invoice_obj.save()
    return JsonResponse({"response_code": 2})


def night_report_template(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": "POST REQUEST!"})

    jdatetime.set_locale('fa_IR')
    report_data = {}
    cash_id = request.GET['cash_id']

    try:
        cash_object = Cash.objects.get(pk=cash_id)
    except Cash.DoesNotExist:
        return JsonResponse({"response_code": 4, "error_msg": "No Cash!"})

    cash_open_date = cash_object.created_date_time
    jalali_date_create = jdatetime.date.fromgregorian(day=cash_open_date.day, month=cash_open_date.month,
                                                      year=cash_open_date.year)
    all_invoice_in_cash_desk = InvoiceSales.objects.filter(cash_desk=cash_object)
    sum_total_price = all_invoice_in_cash_desk.aggregate(Sum("total_price"))
    sum_cash = all_invoice_in_cash_desk.aggregate(Sum("cash"))
    sum_pos = all_invoice_in_cash_desk.aggregate(Sum("pos"))
    sum_tip = all_invoice_in_cash_desk.aggregate(Sum("tip"))
    sum_discount = all_invoice_in_cash_desk.aggregate(Sum("discount"))
    report_data['created_date'] = jalali_date_create.strftime("%Y/%m/%d")
    report_data['day_of_the_week'] = jalali_date_create.strftime("%A")
    report_data['total_price'] = format(int(sum_total_price['total_price__sum']) - int(sum_discount['discount__sum']),
                                        ",d")
    report_data['cash'] = format(int(sum_cash['cash__sum']), ",d")
    report_data['pos'] = format(int(sum_pos['pos__sum']), ",d")
    report_data['tip'] = format(int(sum_tip['tip__sum']), ",d")
    report_data['income_report'] = format(cash_object.income_report, ",d")
    report_data['outcome_report'] = format(cash_object.outcome_report, ",d")
    report_data['event_tickets'] = format(cash_object.event_tickets, ",d")
    report_data['current_money_in_cash'] = format(cash_object.current_money_in_cash, ",d")
    report_data['total_cash_desk'] = (int(sum_total_price['total_price__sum']) - int(
        sum_discount['discount__sum'])) - int(
        sum_pos['pos__sum']) - cash_object.outcome_report - cash_object.event_tickets + cash_object.income_report + int(
        sum_tip['tip__sum'])
    report_data['difference'] = cash_object.current_money_in_cash - report_data['total_cash_desk']
    report_data['total_cash_desk'] = format(report_data['total_cash_desk'], ',d')
    report_data['difference'] = format(report_data['difference'], ',d')
    return render(request, 'night_report.html', {"report_data": report_data})
