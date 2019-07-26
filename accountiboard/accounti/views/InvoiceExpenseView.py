from django.http import JsonResponse
from accounti.models import *
from datetime import datetime
import jdatetime, json

WRONG_USERNAME_OR_PASS = "نام کاربری یا رمز عبور اشتباه است."
USERNAME_ERROR = 'نام کاربری خود  را وارد کنید.'
PASSWORD_ERROR = 'رمز عبور خود را وارد کنید.'
NOT_SIMILAR_PASSWORD = 'رمز عبور وارد شده متفاوت است.'
DATA_REQUIRE = "اطلاعات را به شکل کامل وارد کنید."
SUPPLIER_REQUIRE = "تامین کننده وارد کنید."
PHONE_ERROR = 'شماره تلفن خود  را وارد کنید.'
UNATHENTICATED = 'لطفا ابتدا وارد شوید.'


def create_new_invoice_expense(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_expense_id = rec_data['id']

        if invoice_expense_id == 0:
            supplier_id = rec_data['supplier_id']
            expense_cat_id = rec_data['expense_cat_id']
            total_price = rec_data['total_price']
            settlement_type = rec_data['settlement_type']
            tax = rec_data['tax']
            services = rec_data['services']
            discount = rec_data['discount']
            username = rec_data['username']
            branch_id = rec_data['branch_id']

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            
            if not request.session['is_logged_in'] == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            
            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not total_price:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if supplier_id == 0:
                return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
            if not settlement_type:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not expense_cat_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if services[0]['service_name'] == '':
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            supplier_obj = Supplier.objects.get(pk=supplier_id)
            now_time = datetime.now()

            expense_cat_obj = ExpenseCategory.objects.get(pk=expense_cat_id)

            new_invoice = InvoiceExpense(
                branch=branch_obj,
                expense_category=expense_cat_obj,
                created_time=now_time,
                supplier=supplier_obj,
                price=total_price,
                tax=tax,
                discount=discount,
                settlement_type=settlement_type
            )
            new_invoice.save()

            for service in services:
                new_service = InvoiceExpenseToService(
                    service_name=service['service_name'],
                    description=service['description'],
                    price=service['price'],
                    invoice_expense=new_invoice
                )
                new_service.save()
            
            if settlement_type == "CREDIT":
                supplier_obj.remainder += int(total_price)
                supplier_obj.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def get_all_invoices(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        username = rec_data['username']
        branch_id = rec_data['branch_id']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not branch_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoiceExpense.objects.filter(branch=branch_obj)
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            invoices.append({
                'id': invoice.pk,
                'supplier_name': invoice.supplier.name,
                'settlement_type': invoice.get_settlement_type_display(),
                'expense_category': invoice.expense_category.name,
                'total_price': invoice.price,
                'date': jalali_date.strftime("%Y/%m/%d")
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def search_expense(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not search_word:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
        items_searched = InvoiceExpense.objects.filter(supplier__name__contains=search_word)
        expenses = []
        for expense in items_searched:
            invoice_date = expense.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            expenses.append({
                'id': expense.pk,
                'supplier_name': expense.supplier.name,
                'expense_category': expense.expense_category.name,
                'total_price': expense.price,
                'date': jalali_date.strftime("%Y/%m/%d")
            })
        return JsonResponse({"response_code": 2, 'expenses': expenses})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


def delete_invoice_expense(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        username = rec_data['username']

        if not request.session['is_logged_in'] == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoiceExpense.objects.get(pk=invoice_id)
        invoice_type = invoice_obj.settlement_type

        if invoice_type == "CASH":
            invoice_obj.delete()

        elif invoice_type == "CREDIT":
            invoice_obj.supplier.remainder -= invoice_obj.price
            invoice_obj.supplier.save()
            invoice_obj.delete()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})
