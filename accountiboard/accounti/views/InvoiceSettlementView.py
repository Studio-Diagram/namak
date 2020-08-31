from django.http import JsonResponse
from accounti.models import *
from datetime import datetime
import jdatetime, json
from accountiboard.constants import *


def create_new_invoice_settlement(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_settlement_id = rec_data['id']

        if invoice_settlement_id == 0:
            supplier_id = rec_data['supplier_id']
            payment_amount = rec_data['payment_amount']
            username = rec_data['username']
            settle_type = rec_data['settle_type']
            backup_code = rec_data['backup_code']
            branch_id = rec_data['branch_id']
            invoice_date = rec_data['date']
            factor_number = rec_data['factor_number']
            banking_id = rec_data.get('banking_id')
            stock_id = rec_data.get('stock_id')

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
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

            if stock_id:
                try:
                    stock_obj = Stock.objects.get(pk=stock_id)
                except:
                    return JsonResponse({"error_msg": STOCK_NOT_FOUND}, status=404)
            else:
                stock_obj = None

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
                stock=stock_obj,
            )
            new_invoice.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_invoices(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch_id']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
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
                'banking': invoice.banking.name,
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_pays(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = InvoiceSettlement.objects.filter(supplier__name__contains=search_word)
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
                'created_time': jalali_date.strftime("%Y/%m/%d")
            })
        return JsonResponse({"response_code": 2, 'pays': pays})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def delete_invoice_settlement(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoiceSettlement.objects.get(pk=invoice_id)

        invoice_obj.delete()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})