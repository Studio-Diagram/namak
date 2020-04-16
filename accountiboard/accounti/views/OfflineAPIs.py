from django.http import JsonResponse
import json
from accounti.models import *
from django.db import IntegrityError
from datetime import datetime, timedelta
import jdatetime

UUID_EMPTY_ERROR = "UUID is empty!"
METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
DUPLICATE_MEMBER_ENTRY = "شماره تلفن یا کارت تکراری است."
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."


def status_of_server(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    return JsonResponse({"response_code": 2})


def sync_member_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Member.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "last_name": item.last_name,
        "card_number": item.card_number,
        "p_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'members': have_to_add_data})


def sync_menu_category_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = MenuCategory.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "kind": item.kind,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'menu_categories': have_to_add_data})


def sync_menu_item_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = MenuItem.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "price": item.price,
        "is_deleted": item.is_delete,
        "menu_category_id": item.menu_category.pk,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'menu_items': have_to_add_data})


def sync_printer_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Printer.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'printers': have_to_add_data})


def sync_printer_to_category_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = PrinterToCategory.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "printer_id": item.printer_id,
        "menu_category_id": item.menu_category_id
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'printer_to_category_data': have_to_add_data})


def sync_table_category_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = TableCategory.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'table_categories': have_to_add_data})


def sync_table_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Table.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "table_category_id": item.category_id,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'tables': have_to_add_data})


def sync_employee_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Employee.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "phone": item.phone,
        "password": item.password,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'employees': have_to_add_data})


def sync_branch_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Branch.objects.filter(pk__gt=last_uuid).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "start_working_time": item.start_working_time,
        "end_working_time": item.end_working_time,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'branches': have_to_add_data})


def sync_cash_list(request, last_uuid):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Cash.objects.filter(pk__gt=last_uuid, is_close=0).order_by('pk')
    have_to_add_data = [{
        "created_date_time": item.created_date_time,
        "ended_date_time": item.ended_date_time,
        "income_report": item.income_report,
        "outcome_report": item.outcome_report,
        "current_money_in_cash": item.current_money_in_cash,
        "event_tickets": item.event_tickets,
        "employee_id": item.employee_id,
        "branch_id": item.branch_id,
        "is_close": item.is_close,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'cashes': have_to_add_data})


def sync_invoice_sales_list(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    have_to_add_data = []

    last_cash_object = Cash.objects.filter(is_close=0).last()
    if last_cash_object:
        have_to_add_objects = InvoiceSales.objects.filter(is_deleted=0, cash_desk=last_cash_object).order_by('pk')
        have_to_add_data = [{
            "factor_number": item.factor_number,
            "created_time": item.created_time,
            "cash": item.cash,
            "pos": item.pos,
            "employee_discount": item.employee_discount,
            "tax": item.tax,
            "settlement_type": item.settlement_type,
            "table_name": item.table.name,
            "guest_numbers": item.guest_numbers,
            "total_price": item.total_price,
            "discount": item.discount,
            "tip": item.tip,
            "settle_time": item.settle_time,
            "is_settled": item.is_settled,
            "ready_for_settle": item.ready_for_settle,
            "server_primary_key": item.pk,
            "member_id": item.member_id,
            "cash_id": item.cash_desk_id,
            "table_id": item.table_id,
            "branch_id": item.branch_id,
            "is_do_not_want_order": item.is_do_not_want_order,
            "game_state": item.game_state,
            "games_list": [{
                "member_id": game.game.member_id,
                "start_time": game.game.start_time,
                "end_time": game.game.end_time,
                "numbers": game.game.numbers,
                "points": game.game.points,
                "add_date": game.game.add_date,
                "server_primary_key_game": game.game_id,
                "server_primary_key_invoice_to_game": game.pk
            } for game in InvoicesSalesToGame.objects.filter(invoice_sales=item)],
            "menu_items_list": [{
                "menu_item_id": menu_item.menu_item_id,
                "numbers": menu_item.numbers,
                "description": menu_item.description,
                "is_print": menu_item.is_print,
                "server_primary_key_invoice_to_menu_item": menu_item.pk
            } for menu_item in InvoicesSalesToMenuItem.objects.filter(invoice_sales=item)]
        } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'invoices': have_to_add_data})


def sync_reserve_list(request, branch_id):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    now = datetime.now()
    now_time = now.time()
    now_date = datetime.now().date()

    branch = Branch.objects.get(pk=branch_id)

    end_work_time = branch.end_working_time

    after_midnight_hours = ['00', '01', '02', '03', '04', '05', '06']

    end_work_time_hour = end_work_time.strftime('%H')
    if now_time < end_work_time and end_work_time_hour in after_midnight_hours:
        yesterday = now_date - timedelta(1)
        today = jdatetime.date.fromgregorian(day=yesterday.day, month=yesterday.month,
                                             year=yesterday.year)
        today = today.strftime("%d/%m/%Y")
    else:
        today = jdatetime.date.fromgregorian(day=now_date.day, month=now_date.month,
                                             year=now_date.year)
        today = today.strftime("%d/%m/%Y")

    reserve_date_split = today.split('/')
    reserve_date_g = jdatetime.date(int(reserve_date_split[2]), int(reserve_date_split[1]),
                                    int(reserve_date_split[0])).togregorian()
    have_to_add_objects = Reservation.objects.filter(branch=branch, reserve_date__gte=reserve_date_g).exclude(
        reserve_state="call_waiting")

    have_to_add_data = [{
        "start_time": item.start_time,
        "end_time": item.end_time,
        "numbers": item.numbers,
        "reserve_date": item.reserve_date,
        "customer_name": item.customer_name,
        "phone": item.phone,
        "reserve_state": item.reserve_state,
        "branch_id": item.branch_id,
        "tables": [{
            "table_id": table.table_id,
            "server_primary_key_reserve_to_table": table.pk
        } for table in ReserveToTables.objects.filter(reserve=item)],
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'reserves': have_to_add_data})


def create_member(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

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

        except IntegrityError as e:
            if 'unique constraint' in e.args[0]:
                return JsonResponse({"response_code": 3, "error_msg": DUPLICATE_MEMBER_ENTRY})

    return JsonResponse({"response_code": 2})
