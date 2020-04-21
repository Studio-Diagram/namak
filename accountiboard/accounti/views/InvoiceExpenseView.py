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
OTHER_SUPPLIER_REQUIRE = "در صورت خالی بودن تامین کننده باید تامین‌کننده‌ای با نام سایر در تامین کنندگان وارد نمایید."
FACTOR_NUMBER_INVALID = "شماره فاکتور تطابق ندارد."
METHOD_NOT_ALLOWED = "Method not allowed."


def create_new_invoice_expense(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_expense_id = rec_data['id']

        if invoice_expense_id == 0:
            supplier_id = rec_data['supplier_id']
            expense_tags = rec_data['expense_tags']
            expense_kind = rec_data['expense_kind']
            total_price = rec_data['total_price']
            settlement_type = rec_data['settlement_type']
            tax = rec_data['tax']
            services = rec_data['services']
            discount = rec_data['discount']
            invoice_date = rec_data['date']
            username = rec_data['username']
            branch_id = rec_data['branch_id']
            factor_number = rec_data['factor_number']

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

            if not branch_id:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not total_price:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not settlement_type:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not expense_kind:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not expense_tags:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if services[0]['service_name'] == '':
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not invoice_date:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not factor_number:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            if supplier_id == 0:
                supplier_obj = Supplier.objects.filter(name="سایر").first()
                if not supplier_obj:
                    return JsonResponse({"response_code": 3, "error_msg": OTHER_SUPPLIER_REQUIRE})
            else:
                supplier_obj = Supplier.objects.get(pk=supplier_id)

            branch_obj = Branch.objects.get(pk=branch_id)

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
                                                datetime.now().second).togregorian()

            last_invoice_obj = InvoiceExpense.objects.filter(branch=branch_obj).order_by('id').last()
            if last_invoice_obj:
                new_factor_number = last_invoice_obj.factor_number + 1
            else:
                new_factor_number = 1

            if new_factor_number != factor_number:
                return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

            new_invoice = InvoiceExpense(
                branch=branch_obj,
                created_time=invoice_date_g,
                expense_kind=expense_kind,
                supplier=supplier_obj,
                price=total_price,
                tax=tax,
                discount=discount,
                settlement_type=settlement_type,
                factor_number=new_factor_number
            )
            new_invoice.save()

            for tag in expense_tags:
                if "id" in tag:
                    tag_obj = ExpenseTag.objects.filter(id=tag['id']).first()
                else:
                    tag_obj = ExpenseTag(
                        name=tag['name']
                    )
                    tag_obj.save()

                new_tag_to_expense = ExpenseToTag(
                    invoice_expense=new_invoice,
                    tag=tag_obj
                )
                new_tag_to_expense.save()

            for service in services:
                new_service = InvoiceExpenseToService(
                    service_name=service['service_name'],
                    description=service['description'],
                    price=service['price'],
                    invoice_expense=new_invoice
                )
                new_service.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})

    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


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
        invoice_objects = InvoiceExpense.objects.filter(branch=branch_obj).order_by('-id')[:100]
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.created_time.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)
            invoices.append({
                'id': invoice.pk,
                'factor_number': invoice.factor_number,
                'supplier_name': invoice.supplier.name,
                'settlement_type': invoice.get_settlement_type_display(),
                'expense_category': invoice.get_expense_kind_display(),
                'total_price': invoice.price,
                'date': jalali_date.strftime("%Y/%m/%d")
            })

        return JsonResponse({"response_code": 2, 'invoices': invoices})
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def search_expense(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data['search_word']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
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
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def delete_invoice_expense(request):
    if request.method == "POST":
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data['invoice_id']
        username = rec_data['username']

        if not request.session.get('is_logged_in', None) == username:
            return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoiceExpense.objects.get(pk=invoice_id)
        invoice_type = invoice_obj.settlement_type

        if invoice_type == "CASH":
            invoice_obj.delete()

        elif invoice_type == "CREDIT":
            invoice_obj.delete()

        return JsonResponse({"response_code": 2})
    return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})


def get_all_tags(request):
    if request.method != "POST":
        return JsonResponse({"response_code": 4, "error_msg": METHOD_NOT_ALLOWED})

    rec_data = json.loads(request.read().decode('utf-8'))
    username = rec_data['username']

    if not request.session.get('is_logged_in', None) == username:
        return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})

    all_tags = ExpenseTag.objects.all().order_by("name")
    all_tags_data = []
    for tag in all_tags:
        all_tags_data.append({
            "id": tag.pk,
            "name": tag.name
        })

    return JsonResponse({"response_code": 2, 'tags': all_tags_data})
