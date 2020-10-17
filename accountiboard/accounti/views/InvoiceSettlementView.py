from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
from accounti.models import *
from datetime import datetime
import jdatetime, json
from accountiboard.constants import *


class CreateNewInvoiceSettlementView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_settlement_id = rec_data.get('id')

        if invoice_settlement_id == 0:
            supplier_id = rec_data.get('supplier_id')
            payment_amount = rec_data.get('payment_amount')
            settle_type = rec_data.get('settle_type')
            backup_code = rec_data.get('backup_code')
            branch_id = rec_data.get('branch_id')
            invoice_date = rec_data.get('date')
            factor_number = rec_data.get('factor_number')
            banking_id = rec_data.get('banking_id')

            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not payment_amount:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if supplier_id == 0:
                return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
            if not invoice_date:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not settle_type:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not factor_number:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not banking_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            supplier_obj = Supplier.objects.get(pk=supplier_id)
            now_time = datetime.now()

            if banking_id:
                try:
                    banking_obj = BankingBaseClass.objects.get(pk=banking_id)
                except:
                    return JsonResponse({"error_msg": BANKING_NOT_FOUND}, status=404)
            else:
                banking_obj = None

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
                                                datetime.now().second).togregorian()

            last_invoice_obj = InvoiceSettlement.objects.filter(branch=branch_obj).order_by('id').last()
            if last_invoice_obj:
                new_factor_number = last_invoice_obj.factor_number + 1
            else:
                new_factor_number = 1
            if new_factor_number != factor_number:
                return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

            new_invoice = InvoiceSettlement(
                branch=branch_obj,
                payment_amount=payment_amount,
                settle_type=settle_type,
                backup_code=backup_code,
                supplier=supplier_obj,
                created_time=invoice_date_g,
                factor_number=new_factor_number,
                banking=banking_obj,
            )
            new_invoice.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})


class GetAllInvoiceSettlementsView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch_id')

        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoiceSettlement.objects.filter(branch=branch_obj).order_by('-id')[:100]
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)

            invoices.append({
                'id': invoice.pk,
                'factor_number': invoice.factor_number,
                'supplier_name': invoice.supplier.name,
                'payment_amount': invoice.payment_amount,
                'settle_type': invoice.get_settle_type_display(),
                'backup_code': invoice.backup_code,
                'created_time': jalali_date.strftime("%Y/%m/%d"),
                'banking': invoice.banking.name if invoice.banking else "",
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})


class SearchPaysView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data.get('search_word')
        branch_id = rec_data.get('branch_id')

        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = InvoiceSettlement.objects.filter(supplier__name__contains=search_word, branch_id=branch_id).order_by(
            '-id')
        pays = []
        for pay in items_searched:
            invoice_date = pay.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            pays.append({
                'id': pay.pk,
                'factor_number': pay.factor_number,
                'supplier_name': pay.supplier.name,
                'payment_amount': pay.payment_amount,
                'settle_type': pay.get_settle_type_display(),
                'backup_code': pay.backup_code,
                'banking': pay.banking.name if pay.banking else "",
                'created_time': jalali_date.strftime("%Y/%m/%d")
            })
        return JsonResponse({"response_code": 2, 'pays': pays})


class DeleteInvoiceSettlementView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def delete(self, request, item_id, *args, **kwargs):
        invoice_obj = InvoiceSettlement.objects.get(pk=item_id)
        invoice_obj.delete()
        return JsonResponse({})
