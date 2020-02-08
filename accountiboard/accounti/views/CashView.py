from django.http import JsonResponse
import json, jdatetime, datetime
from accounti.models import *

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'
DUPLICATE_CASH = 'دو صندوق باز وجود دارد. با تیم فنی تماس بگیرید.'
NO_CASH = 'صندوق بازی وجود ندارد.'
OLD_CASH = 'انقضای صندوق گذشته است.'
UNSETTLED_INVOICE = "فاکتور تسویه نشده وجود دارد."


def get_all_cash(request):
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
        all_cashes = Cash.objects.filter(branch=branch_obj).order_by('id')[:100]

        all_cashes_json_data = []

        for cash in all_cashes:
            cash_start_date = cash.created_date_time.date()
            cash_start_jalali_date = jdatetime.date.fromgregorian(day=cash_start_date.day, month=cash_start_date.month,
                                                                  year=cash_start_date.year)
            cash_start_time = cash.created_date_time.time()
            if cash.ended_date_time:
                cash_end_date = cash.ended_date_time.date()
                cash_end_jalali_date = jdatetime.date.fromgregorian(day=cash_end_date.day, month=cash_end_date.month,
                                                                    year=cash_end_date.year)
                cash_end_time = cash.ended_date_time.time()
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
                'is_closed': cash.is_close
            })

        return JsonResponse({"response_code": 2, 'all_cashes': all_cashes_json_data})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def close_cash(request):
    if request.method == "POST":
        now = datetime.datetime.now()
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
        employee_obj = Employee.objects.filter(phone=username).first()
        current_cash = Cash.objects.filter(branch=branch_obj, is_close=0)

        if current_cash.count() == 1:
            all_invoices_from_this_cash = InvoiceSales.objects.filter(cash_desk=current_cash.first(), is_settled=False)
            if all_invoices_from_this_cash.count():
                return JsonResponse({"response_code": 3, 'error_msg': UNSETTLED_INVOICE})
            current_cash_obj = current_cash.first()
            current_cash_obj.is_close = 1
            current_cash_obj.employee = employee_obj
            current_cash_obj.ended_date_time = now
            current_cash_obj.save()
            return JsonResponse({"response_code": 2})
        else:
            return JsonResponse({"response_code": 3, 'error_msg': DUPLICATE_CASH})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def open_cash(request):
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
        new_cash = Cash(branch=branch_obj)
        new_cash.save()

        return JsonResponse({"response_code": 2})

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
        elif (datetime.datetime.today().date() - current_cash_obj.created_date_time.date()).days:
            return JsonResponse({"response_code": 3, 'error_msg': OLD_CASH, 'error_mode': 'OLD_CASH'})
        if current_cash.count() == 1:
            return JsonResponse({"response_code": 2})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})

