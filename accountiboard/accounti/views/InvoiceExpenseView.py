from django.http import JsonResponse
from django.views import View
from accountiboard.custom_permissions import *
from accounti.models import *
from datetime import datetime
import jdatetime, json
from accountiboard.constants import *


class CreateNewInvoiceExpenseView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
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
            branch_id = rec_data['branch_id']
            factor_number = rec_data['factor_number']
            banking_id = rec_data.get('banking_id')
            stock_id = rec_data.get('stock_id')

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
                factor_number=new_factor_number,
                banking=banking_obj,
                stock=stock_obj,
            )
            new_invoice.save()

            for tag in expense_tags:
                if "id" in tag:
                    tag_obj = ExpenseTag.objects.filter(id=tag['id']).first()
                else:
                    tag_obj = ExpenseTag(
                        name=tag['name'],
                        organization=branch_obj.organization
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


class GetAllInvoicesExpenseView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch_id')

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


class SearchExpenseView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        search_word = rec_data.get('search_word')

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


class DeleteInvoiceExpenseView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS,
        branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_id = rec_data.get('invoice_id')

        if not invoice_id:
            return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

        invoice_obj = InvoiceExpense.objects.get(pk=invoice_id)
        invoice_type = invoice_obj.settlement_type

        if invoice_type == "CASH":
            invoice_obj.delete()

        elif invoice_type == "CREDIT":
            invoice_obj.delete()

        return JsonResponse({"response_code": 2})


class GetAllTagsView(View):
    @permission_decorator_class_based(token_authenticate,
        {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['CASHIER'], USER_ROLES['ACCOUNTANT']},
        ALLOW_ALL_PLANS)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        branch_id = rec_data.get('branch')

        organization_object = Branch.objects.get(id=branch_id).organization
        all_tags = ExpenseTag.objects.filter(organization=organization_object).order_by("name")
        all_tags_data = []
        for tag in all_tags:
            all_tags_data.append({
                "id": tag.pk,
                "name": tag.name
            })

        return JsonResponse({"response_code": 2, 'tags': all_tags_data})
