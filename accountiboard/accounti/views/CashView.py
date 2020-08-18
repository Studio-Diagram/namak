from django.http import JsonResponse
import json, jdatetime
from datetime import datetime
from accounti.models import *
from django.db.models import Sum
from functools import wraps
from accountiboard.constants import *


def get_all_cash(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
    rec_data = json.loads(request.read().decode('utf-8'))
    branch_id = rec_data['branch_id']
    username = rec_data['username']

    if not username:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not branch_id:
        return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    branch_obj = Branch.objects.get(pk=branch_id)
    all_cashes = Cash.objects.filter(branch=branch_obj).order_by('-id')[:100]

    all_cashes_json_data = []

    for cash in all_cashes:
        all_invoice_sales_cash_total_income = InvoiceSales.objects.filter(cash_desk=cash, is_deleted=False,
                                                                          is_settled=True).aggregate(
            Sum('total_price'))

        cash_start_date = cash.created_date_time.date()
        cash_start_jalali_date = jdatetime.date.fromgregorian(day=cash_start_date.day, month=cash_start_date.month,
                                                              year=cash_start_date.year)
        cash_start_time = cash.created_date_time.time().strftime("%H:%M")
        if cash.ended_date_time:
            cash_end_date = cash.ended_date_time.date()
            cash_end_jalali_date = jdatetime.date.fromgregorian(day=cash_end_date.day, month=cash_end_date.month,
                                                                year=cash_end_date.year)
            cash_end_time = cash.ended_date_time.time().strftime("%H:%M")
            cash_final_end_date = cash_end_jalali_date.strftime("%Y/%m/%d")
        else:
            cash_final_end_date = ''
            cash_end_time = ''

        all_cashes_json_data.append({
            'id': cash.pk,
            'start_date': cash_start_jalali_date.strftime("%Y/%m/%d"),
            'end_date': cash_final_end_date,
            'start_time': cash_start_time,
            'end_time': cash_end_time,
            'is_closed': cash.is_close,
            'total_income': all_invoice_sales_cash_total_income['total_price__sum'] if
            all_invoice_sales_cash_total_income['total_price__sum'] else 0
        })

    return JsonResponse({"response_code": 2, 'all_cashes': all_cashes_json_data})


def close_cash(request):
    if request.method == "POST":
        now = datetime.now()
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch_id']
        username = rec_data['username']
        if 'night_report_inputs' not in rec_data.keys():
            night_report_inputs = {
                "current_money_in_cash": 0,
                "income_report": 0,
                "outcome_report": 0,
                "event_tickets": 0
            }
        else:
            night_report_inputs = rec_data['night_report_inputs']

        if not username:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        if night_report_inputs['income_report'] == "" or night_report_inputs['outcome_report'] == "" \
                or night_report_inputs['event_tickets'] == "" or night_report_inputs['current_money_in_cash'] == "":
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if not night_report_inputs['income_report'] \
                or not night_report_inputs['outcome_report'] \
                or not night_report_inputs['event_tickets'] \
                or not night_report_inputs['current_money_in_cash']:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        user_object = User.objects.filter(phone=username).first()
        current_cash = Cash.objects.filter(branch=branch_obj, is_close=0)

        if current_cash.count() == 1:
            all_invoices_from_this_cash = InvoiceSales.objects.filter(cash_desk=current_cash.first(), is_settled=False,
                                                                      is_deleted=False)
            if all_invoices_from_this_cash.count():
                return JsonResponse({"response_code": 3, 'error_msg': UNSETTLED_INVOICE})
            current_cash_obj = current_cash.first()
            current_cash_obj.is_close = 1
            current_cash_obj.employee = user_object
            current_cash_obj.ended_date_time = now
            current_cash_obj.current_money_in_cash = night_report_inputs['current_money_in_cash']
            current_cash_obj.income_report = night_report_inputs['income_report']
            current_cash_obj.outcome_report = night_report_inputs['outcome_report']
            current_cash_obj.event_tickets = night_report_inputs['event_tickets']
            current_cash_obj.save()
            return JsonResponse({"response_code": 2})
        else:
            return JsonResponse({"response_code": 3, 'error_msg': DUPLICATE_CASH})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def open_cash(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']
        username = rec_data['username']

        if not username:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        branch_obj = Branch.objects.get(pk=branch_id)
        new_cash = Cash(branch=branch_obj)
        new_cash.save()

        return JsonResponse({"response_code": 2, "new_cash_id": new_cash.id})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def check_cash_exist(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch_id']
        username = rec_data['username']

        if not username:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

        branch_obj = Branch.objects.get(pk=branch_id)
        current_cash = Cash.objects.filter(branch=branch_obj, is_close=0)
        current_cash_obj = current_cash.first()

        if current_cash.count() == 0:
            return JsonResponse({"response_code": 3, 'error_msg': NO_CASH, 'error_mode': 'NO_CASH'})
        elif (datetime.today().date() - current_cash_obj.created_date_time.date()).days:
            return JsonResponse({"response_code": 3, 'error_msg': OLD_CASH, 'error_mode': 'OLD_CASH'})
        if current_cash.count() == 1:
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
