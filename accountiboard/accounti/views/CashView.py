from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
import json, jdatetime
from datetime import datetime
from accounti.models import *
from django.db.models import Sum
from functools import wraps
from accountiboard.constants import *
from django.shortcuts import get_object_or_404


class GetAllCashView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch_id']

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

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


class CloseCashView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        now = datetime.now()
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch_id']
        if 'night_report_inputs' not in rec_data.keys():
            night_report_inputs = {
                "current_money_in_cash": 0,
                "income_report": 0,
                "outcome_report": 0,
                "event_tickets": 0
            }
        else:
            night_report_inputs = rec_data['night_report_inputs']

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if night_report_inputs['income_report'] == "" or night_report_inputs['outcome_report'] == "" \
                or night_report_inputs['event_tickets'] == "" or night_report_inputs['current_money_in_cash'] == "":
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        if night_report_inputs['income_report'] == None \
                or night_report_inputs['outcome_report'] == None \
                or night_report_inputs['event_tickets'] == None \
                or night_report_inputs['current_money_in_cash'] == None:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        user_object = User.objects.filter(phone=request.payload['sub_phone']).first()
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


class OpenCashView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch']

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        new_cash = Cash(branch=branch_obj)
        new_cash.save()

        return JsonResponse({"response_code": 2, "new_cash_id": new_cash.id})


class CheckCashExistView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']})
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data['branch_id']

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        current_cash = Cash.objects.filter(branch=branch_obj, is_close=0)
        current_cash_obj = current_cash.first()

        if current_cash.count() == 0:
            return JsonResponse({"response_code": 3, 'error_msg': NO_CASH, 'error_mode': 'NO_CASH'})
        elif (datetime.today().date() - current_cash_obj.created_date_time.date()).days:
            unsettled_invoices = InvoiceSales.objects.filter(is_settled=0, cash_desk=current_cash_obj, is_deleted=0).count()
            if unsettled_invoices:
                return JsonResponse(
                    {"response_code": 3, 'error_msg': OLD_CASH_WITH_UNSETTLED_INVOICES, 'error_mode': 'OLD_CASH_WITH_UNSETTLED_INVOICES'})
            else:
                return JsonResponse({"response_code": 3, 'error_msg': OLD_CASH, 'error_mode': 'OLD_CASH'})
        if current_cash.count() == 1:
            return JsonResponse({"response_code": 2})


class InvoiceSalesByCashView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        {USER_PLANS_CHOICES['STANDARDNORMAL'], USER_PLANS_CHOICES['STANDARDBG'], USER_PLANS_CHOICES['ENTERPRISE']},
        branch_disable=True)
    def get(self, request, cash_id, *args, **kwargs):

        current_cash = get_object_or_404(Cash, pk=cash_id)

        all_branches_this_user = {branch['id'] for branch in request.payload['sub_branch_list']}

        if current_cash.branch.id not in all_branches_this_user:
            return JsonResponse({"error_msg": ACCESS_DENIED}, status=403)

        all_related_invoice_sales = InvoiceSales.objects.filter(cash_desk=current_cash)
        all_invoice_sales_total_price = all_related_invoice_sales.aggregate(Sum('total_price')).get('total_price__sum')
        all_related_invoice_sales_list = [{
            'id': invoice_sale.id,
            'cash': invoice_sale.cash,
            'total_price': invoice_sale.total_price,            
            'created_time': invoice_sale.created_time,
            'settle_time': invoice_sale.settle_time.time().strftime("%H:%M") if invoice_sale.settle_time else '',
            'settlement_type': invoice_sale.settlement_type,
            'guest_numbers': invoice_sale.guest_numbers,
            'member': invoice_sale.member.__str__() if invoice_sale.member else "مهمان",
            'branch': invoice_sale.branch.name,
            'table': invoice_sale.table.name,
        } for invoice_sale in all_related_invoice_sales]

        return JsonResponse({
            'id': current_cash.pk,
            'employee': current_cash.employee.get_full_name() if current_cash.employee else '',
            'current_money_in_cash': current_cash.current_money_in_cash,
            'created_date_time': jdatetime.datetime.fromgregorian(datetime=current_cash.created_date_time).strftime("%H:%M %Y/%m/%d") if
                current_cash.created_date_time else '',
            'ended_date_time': jdatetime.datetime.fromgregorian(datetime=current_cash.ended_date_time).strftime("%H:%M %Y/%m/%d") if
                current_cash.ended_date_time else '',
            'income_report': current_cash.income_report,
            'outcome_report': current_cash.outcome_report,
            'event_tickets': current_cash.event_tickets,
            'is_closed': current_cash.is_close,
            'all_sales_price': all_invoice_sales_total_price if all_invoice_sales_total_price else 0,
            'related_invoice_sales': all_related_invoice_sales_list,
        })
