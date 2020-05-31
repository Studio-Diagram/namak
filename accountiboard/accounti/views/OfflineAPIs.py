from django.http import JsonResponse
import json
from accounti.models import *
from django.db import IntegrityError
from datetime import datetime, timedelta
import jdatetime
from accountiboard.constants import *


def status_of_server(request):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})
    return JsonResponse({"response_code": 2})


def sync_member_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    organization_object = Branch.objects.get(id=branch).organization
    have_to_add_objects = Member.objects.filter(pk__gt=last_uuid, organization=organization_object).order_by('pk')
    have_to_add_data = [{
        "last_name": item.last_name,
        "card_number": item.card_number,
        "p_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'members': have_to_add_data})


def sync_menu_category_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = MenuCategory.objects.filter(pk__gt=last_uuid, branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "kind": item.kind,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'menu_categories': have_to_add_data})


def sync_menu_item_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = MenuItem.objects.filter(pk__gt=last_uuid, menu_category__branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "price": item.price,
        "is_deleted": item.is_delete,
        "menu_category_id": item.menu_category.pk,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'menu_items': have_to_add_data})


def sync_printer_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = Printer.objects.filter(pk__gt=last_uuid, branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'printers': have_to_add_data})


def sync_printer_to_category_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = PrinterToCategory.objects.filter(pk__gt=last_uuid, printer__branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "printer_id": item.printer_id,
        "menu_category_id": item.menu_category_id
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'printer_to_category_data': have_to_add_data})


def sync_table_category_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = TableCategory.objects.filter(pk__gt=last_uuid, branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'table_categories': have_to_add_data})


def sync_table_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = Table.objects.filter(pk__gt=last_uuid, category__branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "name": item.name,
        "table_category_id": item.category_id,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'tables': have_to_add_data})


def sync_employee_list(request, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = EmployeeToBranch.objects.filter(branch_id=branch).order_by('pk')
    have_to_add_data = [{
        "phone": item.employee.user.phone,
        "password": item.employee.user.password,
        "server_primary_key": item.employee.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'employees': have_to_add_data})


def sync_branch_list(request, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})

    have_to_add_objects = Branch.objects.filter(id=branch)
    have_to_add_data = [{
        "name": item.name,
        "start_working_time": item.start_working_time,
        "end_working_time": item.end_working_time,
        "server_primary_key": item.pk
    } for item in have_to_add_objects]

    return JsonResponse({"response_code": 2, 'branches': have_to_add_data})


def sync_cash_list(request, last_uuid, branch):
    if request.method != "GET":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    if last_uuid == "" or last_uuid is None:
        return JsonResponse({"response_code": 4, "error_msg": UUID_EMPTY_ERROR})
    elif branch == "" or branch is None:
        return JsonResponse({"response_code": 4, "error_msg": BRANCH_EMPTY_ERROR})

    have_to_add_objects = Cash.objects.filter(pk__gt=last_uuid, is_close=0, branch_id=branch).order_by('pk')
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


def sync_reserves_from_offline(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    have_to_delete = rec_data.get('have_to_delete')
    Reservation.objects.filter(pk__in=have_to_delete).delete()
    all_reserves_data = rec_data.get("all_reserves_data")
    for item in all_reserves_data:
        branch_object = Branch.objects.get(pk=item['branch_id'])
        new_reserve = Reservation(
            start_time=item['start_time'],
            end_time=item['end_time'],
            numbers=item['numbers'],
            reserve_date=item['reserve_date'],
            customer_name=item['customer_name'],
            phone=item['phone'],
            reserve_state=item['reserve_state'],
            branch=branch_object
        )
        new_reserve.save()
        for reserve_to_table in item['tables']:
            table_object = Table.objects.get(pk=reserve_to_table['table_id'])
            new_reserve_to_table = ReserveToTables(
                reserve=new_reserve,
                table=table_object
            )
            new_reserve_to_table.save()
    return JsonResponse({"response_code": 2})


def sync_invoice_sales_from_offline(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    all_cash_data = rec_data.get('all_cash_desk_data')
    for cash_desk in all_cash_data:
        cash_server_primary_key = cash_desk.get("cash_server_primary_key")
        created_date_time = cash_desk.get("created_date_time")
        ended_date_time = cash_desk.get("ended_date_time")
        income_report = cash_desk.get("income_report")
        outcome_report = cash_desk.get("outcome_report")
        event_tickets = cash_desk.get("event_tickets")
        current_money_in_cash = cash_desk.get("current_money_in_cash")
        employee_phone = cash_desk.get("employee")
        branch_server_primary_key = cash_desk.get("branch_server_primary_key")
        is_close = cash_desk.get("is_close")

        if employee_phone:
            user_object = User.objects.get(phone=employee_phone)
        else:
            user_object = None

        if cash_server_primary_key:
            cash_desk_object = Cash.objects.get(id=cash_server_primary_key)
            if is_close:
                cash_desk_object.is_close = 1
                cash_desk_object.ended_date_time = ended_date_time
                cash_desk_object.current_money_in_cash = current_money_in_cash
                cash_desk_object.income_report = income_report
                cash_desk_object.outcome_report = outcome_report
                cash_desk_object.event_tickets = event_tickets
                cash_desk_object.employee = user_object
                cash_desk_object.save()
        else:
            new_cash = Cash(
                created_date_time=created_date_time,
                ended_date_time=ended_date_time,
                income_report=income_report,
                outcome_report=outcome_report,
                event_tickets=event_tickets,
                current_money_in_cash=current_money_in_cash,
                branch_id=branch_server_primary_key,
                is_close=is_close,
                employee=user_object
            )
            new_cash.save()
            cash_desk['cash_server_primary_key'] = new_cash.id

    for item in rec_data.get('all_invoices_data'):
        invoice_id = item.get('server_primary_key')
        branch_object = Branch.objects.get(pk=item['branch_id'])
        invoice_cash_server_primary_key = item['cash_id']
        invoice_cash_offline_id = item['cash_offline_id']
        if invoice_cash_server_primary_key:
            cash_object = Cash.objects.get(id=invoice_cash_server_primary_key)
        else:
            for cash_desk in all_cash_data:
                if cash_desk['cash_offline_id'] == invoice_cash_offline_id:
                    cash_object = Cash.objects.get(id=cash_desk['cash_server_primary_key'])

        if item.get("member_id"):
            member_object = Member.objects.get(pk=item['member_id'])
        elif item.get("member_card_number"):
            member_object = Member.objects.get(card_number=item.get("member_card_number"))
        else:
            member_object = None
        table_object = Table.objects.get(pk=item['table_id'])

        if invoice_id == 0:
            invoice_object = InvoiceSales(
                factor_number=item['factor_number'],
                created_time=item['created_time'],
                settle_time=item['settle_time'],
                cash=item['cash'],
                pos=item['pos'],
                discount=item['discount'],
                employee_discount=item['employee_discount'],
                tax=item['tax'],
                tip=item['tip'],
                settlement_type=item['settlement_type'],
                guest_numbers=item['guest_numbers'],
                is_settled=item['is_settled'],
                total_price=item['total_price'],
                member=member_object,
                table=table_object,
                ready_for_settle=item['ready_for_settle'],
                cash_desk=cash_object,
                branch=branch_object,
                is_do_not_want_order=item['is_do_not_want_order'],
                game_state=item['game_state'],
                is_deleted=item['is_delete']
            )
            invoice_object.save()

        else:
            invoice_object = InvoiceSales.objects.get(pk=invoice_id)
            invoice_object.factor_number = item['factor_number']
            invoice_object.created_time = item['created_time']
            invoice_object.settle_time = item['settle_time']
            invoice_object.cash = item['cash']
            invoice_object.pos = item['pos']
            invoice_object.discount = item['discount']
            invoice_object.employee_discount = item['employee_discount']
            invoice_object.tax = item['tax']
            invoice_object.tip = item['tip']
            invoice_object.settlement_type = item['settlement_type']
            invoice_object.guest_numbers = item['guest_numbers']
            invoice_object.is_settled = item['is_settled']
            invoice_object.total_price = item['total_price']
            invoice_object.member = member_object
            invoice_object.table = table_object
            invoice_object.ready_for_settle = item['ready_for_settle']
            invoice_object.cash_desk = cash_object
            invoice_object.branch = branch_object
            invoice_object.is_do_not_want_order = item['is_do_not_want_order']
            invoice_object.game_state = item['game_state']
            invoice_object.is_deleted = item['is_delete']
            invoice_object.save()

            InvoicesSalesToGame.objects.filter(invoice_sales=invoice_object).delete()
            InvoicesSalesToMenuItem.objects.filter(invoice_sales=invoice_object).delete()

        if item['is_delete']:
            DeletedInvoiceSale(invoice_sale=invoice_object, description=item['delete_description']).save()

        for game in item['games_list']:
            if item.get("member_id"):
                game_member_object = Member.objects.get(pk=game.get('member_id'))
            else:
                game_member_object = Member.objects.get(card_number=game.get("member_card_number"))
            new_game = Game(
                member=game_member_object,
                start_time=game['start_time'],
                end_time=game['end_time'],
                numbers=game['numbers'],
                points=game['points'],
                add_date=game['add_date'],
                branch=branch_object
            )
            new_game.save()
            new_invoice_to_game = InvoicesSalesToGame(
                invoice_sales=invoice_object,
                game=new_game
            )
            new_invoice_to_game.save()

        for menu_item in item['menu_items_list']:
            menu_item_object = MenuItem.objects.get(pk=menu_item['menu_item_id'])
            new_invoice_to_menu_item = InvoicesSalesToMenuItem(
                invoice_sales=invoice_object,
                menu_item=menu_item_object,
                numbers=menu_item['numbers'],
                description=menu_item['description'],
                is_print=menu_item['is_print']
            )
            new_invoice_to_menu_item.save()

    return JsonResponse({"response_code": 2})
