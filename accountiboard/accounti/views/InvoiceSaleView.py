from django.http import JsonResponse
from django.shortcuts import render
import json, base64, random, jdatetime
from accounti.models import *
from django.db.models import Q
import accountiboard.settings as settings
from PIL import Image
from io import BytesIO
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, date
from pytz import timezone

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
NO_SHOP_PRODUCTS_IN_STOCK = "محصول فروشی در انبار نیست."


def settle_invoice_sale(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        invoice_id = rec_data['invoice_id']
        cash = rec_data['cash']
        pos = rec_data['card']
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
        for shop_p in shop_products:
            shop_p.shop_product.real_numbers -= shop_p.numbers
            shop_p.save()
            shop_to_purchases = PurchaseToShopProduct.objects.filter(shop_product=shop_p.shop_product)
            unit_count = shop_p.numbers
            for purchase_to_shop in shop_to_purchases:
                if purchase_to_shop.buy_numbers < purchase_to_shop.unit_numbers and unit_count != 0:
                    buy_counter = 0
                    for i in range(0, unit_count):
                        buy_counter += 1
                        purchase_to_shop.buy_numbers += 1
                        purchase_to_shop.invoice_purchase.supplier.remainder += purchase_to_shop.base_unit_price
                        unit_count -= 1
                        purchase_to_shop.save()
                        purchase_to_shop.invoice_purchase.supplier.save()
                        if purchase_to_shop.buy_numbers == purchase_to_shop.unit_numbers:
                            break

                    new_amani_sale = AmaniSale(invoice_sale_to_shop=shop_p,
                                               supplier=purchase_to_shop.invoice_purchase.supplier,
                                               sale_price=shop_p.shop_product.price,
                                               buy_price=purchase_to_shop.base_unit_price, created_date=datetime.now(),
                                               numbers=buy_counter)
                    new_amani_sale.save()

                elif unit_count == 0:
                    break

        invoice_object.save()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_invoice(request):
    if request.method == "POST":
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
            'member_id': invoice_object.member.pk,
            'guest_numbers': invoice_object.guest_numbers,
            'member_name': invoice_object.member.first_name + " " + invoice_object.member.last_name,
            'member_data': invoice_object.member.first_name + " " + invoice_object.member.last_name,
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
        }
        invoice_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object)
        for game in invoice_games:
            if str(game.game.end_time) != "00:00:00":
                game_total_secs = (game.game.points / game.game.numbers * timedelta(seconds=225)).total_seconds()
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
                    'start_time': game.game.start_time,
                    'end_time': game.game.end_time,
                    'points': "%s:%s'" % (hour_points_string, min_points_string),
                    'total': game.game.points * 5000
                })
            elif str(game.game.end_time) == "00:00:00":
                invoice_data['current_game']['id'] = game.game.pk
                invoice_data['current_game']['numbers'] = game.game.numbers
                invoice_data['current_game']['start_time'] = game.game.start_time

        invoice_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object)
        for item in invoice_items:
            invoice_data['menu_items_old'].append({
                'id': item.pk,
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
        return JsonResponse({"response_code": 2, "invoice": invoice_data})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_today_invoices(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch_id']
        cash_id = rec_data['cash_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not cash_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        cash_obj = Cash.objects.get(pk=cash_id)

        all_invoices = InvoiceSales.objects.filter(branch=branch_obj, cash_desk=cash_obj).order_by("is_settled")
        all_invoices_list = []
        for invoice in all_invoices:
            if invoice.settle_time:
                st_time = invoice.settle_time.time()
            else:
                st_time = 0

            all_invoice_games = InvoicesSalesToGame.objects.filter(invoice_sales=invoice)
            if all_invoice_games.count():
                if all_invoice_games.filter(game__end_time="00:00:00").count():
                    game_status = {"status": "IN_GAME", "text": IN_GAME}
                else:
                    game_status = {"status": "END_GAME", "text": END_GAME}
            else:
                game_status = {"status": "WAIT_GAME", "text": WAIT_GAME}

            invoice_to_menu_items = InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice)
            if invoice_to_menu_items.count():
                invoice_status = {"status": "ORDERED", "text": ORDERED}
            else:
                invoice_status = {"status": "NOT_ORDERED", "text": NOT_ORDERED}

            all_invoices_list.append({
                "invoice_id": invoice.pk,
                "guest_name": invoice.member.last_name,
                "table_name": invoice.table.name,
                "guest_nums": invoice.guest_numbers,
                "total_price": invoice.total_price,
                "discount": invoice.discount,
                "tip": invoice.tip,
                "settle_time": st_time,
                "is_settled": invoice.is_settled,
                "game_status": game_status,
                "invoice_status": invoice_status
            })

        return JsonResponse({"response_code": 2, "all_today_invoices": all_invoices_list})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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


def create_new_invoice_sales(request):
    if request.method == "POST":
        new_invoice_id = 0
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_sales_id = rec_data['invoice_sales_id']
        new_game_id = 0

        if invoice_sales_id == 0:
            table_id = rec_data['table_id']
            member_id = rec_data['member_id']
            guest_numbers = rec_data['guest_numbers']
            current_game = rec_data['current_game']
            menu_items_new = rec_data['menu_items_new']
            shop_items_new = rec_data['shop_items_new']
            branch_id = rec_data['branch_id']
            cash_id = rec_data['cash_id']
            discount = rec_data['discount']
            tip = rec_data['tip']

            if not table_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            for shop_p in shop_items_new:
                shop_obj = ShopProduct.objects.get(pk=shop_p['id'])
                if shop_obj.real_numbers < int(shop_p['nums']):
                    return JsonResponse({"response_code": 3, "error_msg": NO_SHOP_PRODUCTS_IN_STOCK})

            cash_obj = Cash.objects.get(pk=cash_id)

            branch_obj = Branch.objects.get(pk=branch_id)
            table_obj = Table.objects.get(pk=table_id)

            if member_id == 0:
                # HardCode for Guest member
                member_obj = Member.objects.get(pk=1)
            else:
                member_obj = Member.objects.get(pk=member_id)

            new_invoice = InvoiceSales(
                branch=branch_obj,
                table=table_obj,
                guest_numbers=guest_numbers,
                member=member_obj,
                created_time=datetime.now(),
                cash_desk=cash_obj,
                discount=discount,
                tip=tip,
            )
            new_invoice.save()
            new_invoice_id = new_invoice.pk
            if current_game['start_time']:
                new_game = Game(
                    member=member_obj,
                    start_time=datetime.strptime(current_game['start_time'], '%H:%M'),
                    add_date=datetime.now(),
                    numbers=current_game['numbers']
                )
                new_game.save()
                new_game_id = new_game.pk
                new_invoice_to_game = InvoicesSalesToGame(
                    game=new_game,
                    invoice_sales=new_invoice
                )
                new_invoice_to_game.save()
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
                shop_obj.real_numbers -= int(shop['nums'])
                shop_obj.save()
                new_invoice.total_price += int(shop_obj.price) * int(shop['nums'])

            new_invoice.save()
            return JsonResponse({"response_code": 2, "new_game_id": new_game_id, "new_invoice_id": new_invoice_id})

        elif invoice_sales_id != 0:
            table_id = rec_data['table_id']
            member_id = rec_data['member_id']
            guest_numbers = rec_data['guest_numbers']
            current_game = rec_data['current_game']
            menu_items_new = rec_data['menu_items_new']
            shop_items_new = rec_data['shop_items_new']
            branch_id = rec_data['branch_id']
            discount = rec_data['discount']
            tip = rec_data['tip']

            branch_obj = Branch.objects.get(pk=branch_id)
            table_obj = Table.objects.get(pk=table_id)

            for shop_p in shop_items_new:
                shop_obj = ShopProduct.objects.get(pk=shop_p['id'])
                if shop_obj.real_numbers < int(shop_p['nums']):
                    return JsonResponse({"response_code": 3, "error_msg": NO_SHOP_PRODUCTS_IN_STOCK})

            if member_id == 0:
                # HardCode for Guest member
                member_obj = Member.objects.get(pk=1)
            else:
                member_obj = Member.objects.get(pk=member_id)

            old_invoice = InvoiceSales.objects.get(pk=invoice_sales_id)
            old_invoice.table = table_obj
            old_invoice.guest_numbers = guest_numbers
            old_invoice.member = member_obj

            if current_game['id'] == 0 and current_game['start_time']:
                new_game = Game(
                    member=member_obj,
                    start_time=datetime.strptime(current_game['start_time'], '%H:%M'),
                    add_date=datetime.now(),
                    numbers=current_game['numbers']
                )
                new_game.save()
                new_game_id = new_game.pk
                new_invoice_to_game = InvoicesSalesToGame(
                    game=new_game,
                    invoice_sales=old_invoice
                )
                new_invoice_to_game.save()

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
                shop_obj.real_numbers -= int(shop['nums'])
                shop_obj.save()
                old_invoice.total_price += int(shop_obj.price) * int(shop['nums'])

            old_invoice.discount = discount
            old_invoice.tip = tip
            old_invoice.save()
            new_invoice_id = old_invoice.pk
        return JsonResponse({"response_code": 2, "new_game_id": new_game_id, "new_invoice_id": new_invoice_id})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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


def end_current_game(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        game_id = rec_data['game_id']
        end_time = datetime.now().time()
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not game_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        else:
            game_object = Game.objects.get(pk=game_id)
            invoice_to_sales_object = InvoicesSalesToGame.objects.get(game=game_object)
            invoice_id = invoice_to_sales_object.invoice_sales.pk
            invoice_object = InvoiceSales.objects.get(pk=invoice_id)
            start_time = game_object.start_time
            game_object.end_time = end_time

            timedelta_start = timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)

            timedelta_end = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)

            t = timedelta_end - timedelta_start
            point = int(round(t.total_seconds() / 225))
            print(point)
            print(game_object.member.id)
            if game_object.member.id == 1:
                if point % 16 != 0:
                    print(2222222)
                    point = (int(point / 16) + 1) * 16
                    print(point)
            game_numbers = game_object.numbers

            game_object.points = point * game_numbers
            print(point * game_numbers)
            game_object.save()
            invoice_object.total_price += point * game_numbers * 5000
            invoice_object.save()
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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
                    game_total_secs = (game.game.points / game.game.numbers * timedelta(seconds=225)).total_seconds()
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
                        'total': game.game.points * 5000
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
                shop_product_obj.shop_product.real_numbers += shop_product_obj.numbers
                shop_product_obj.save()
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
                invoice_object.total_price -= int(game_obj.game.points) * 5000
                invoice_object.save()
                game_obj.delete()

            return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_today_status(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch_id']

        branch_obj = Branch.objects.get(pk=branch_id)

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

        status = {
            "all_sales_price": 0,
            "all_cash": 0,
            "all_pos": 0,
            "all_guests": 0,
            "all_tax": 0,
            "all_discount": 0,
            "all_tip": 0,
        }

        if now_time > time3am:
            all_invoices = InvoiceSales.objects.filter(branch=branch_obj, created_time__date=now_date)
            for invoice in all_invoices:
                if invoice.created_time.time() > time3am:
                    status['all_sales_price'] += invoice.total_price
                    status['all_cash'] += invoice.cash
                    status['all_pos'] += invoice.pos
                    status['all_guests'] += invoice.guest_numbers
                    status['all_tax'] += invoice.tax
                    status['all_discount'] += invoice.discount
                    status['all_tip'] += invoice.tip

        elif time0am < now_time < time3am:
            all_invoices_yesterday = InvoiceSales.objects.filter(branch=branch_obj, created_time__date=yesterday)
            for invoice in all_invoices_yesterday:
                if invoice.created_time.time() > time3am:
                    status['all_sales_price'] += invoice.total_price
                    status['all_cash'] += invoice.cash
                    status['all_pos'] += invoice.pos
                    status['all_guests'] += invoice.guest_numbers
                    status['all_tax'] += invoice.tax
                    status['all_discount'] += invoice.discount
                    status['all_tip'] += invoice.tip

            all_invoices_today = InvoiceSales.objects.filter(branch=branch_obj, created_time__date=now_date)
            for invoice in all_invoices_today:
                status['all_sales_price'] += invoice.total_price
                status['all_cash'] += invoice.cash
                status['all_pos'] += invoice.pos
                status['all_guests'] += invoice.guest_numbers
                status['all_tax'] += invoice.tax
                status['all_discount'] += invoice.discount
                status['all_tip'] += invoice.tip

        else:
            pass

        return JsonResponse({"response_code": 2, "all_today_status": status})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def calec_time(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        start_time = rec_data['start_time']
        end_time = datetime.now()
        timedelta_start = timedelta(hours=int(start_time.split(":")[0]), minutes=int(start_time.split(":")[1]),
                                    seconds=0)
        timedelta_end = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)
        t = timedelta_end - timedelta_start
        point = int(round(t.total_seconds() / 225))
        return JsonResponse({"response_code": 2, 'price': point * 5000})
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
    if request.method == "POST":
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
        print_data['customer_name'] = invoice_obj.member.last_name
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
                'item_price': 5000,
                'price': game.game.points * 5000
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
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def print_cash_with_template(request):
    if request.method == "GET":
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
        print_data['customer_name'] = invoice_obj.member.last_name
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
            game_total_secs = (game.game.points / game.game.numbers * timedelta(seconds=225)).total_seconds()
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
                'item_price': format(int(80000) * game.game.numbers, ',d'),
                'price': int(game.game.points * 5000)
            })
        all_shop_invoice = InvoicesSalesToShopProducts.objects.filter(invoice_sales=invoice_obj)
        for shop_p in all_shop_invoice:
            is_append = False
            for item in print_data['items']:
                if menu_item.menu_item.pk == item['item_id'] and item['item_kind'] == "SHOP":
                    item['numbers'] += menu_item.numbers
                    item['price'] += int(menu_item.menu_item.price) * int(menu_item.numbers)
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
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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
            'customer_name': invoice_obj.member.last_name,
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
