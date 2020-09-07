from django.http import JsonResponse
from accounti.models import *
# from datetime import datetime
import datetime
import jdatetime, json
from accountiboard.constants import *
from django.views import View
from accountiboard.custom_permissions import *


class InvoiceSalaryView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def post(self, request, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_salary_id = rec_data['id']

        if invoice_salary_id == 0:

            branch_id = rec_data['branch_id']
            employee_id = rec_data['employee_id']
            base_salary = rec_data['base_salary']
            description = rec_data['description']
            over_time_pay = rec_data['over_time_pay']
            benefits = rec_data['benefits']
            bonuses = rec_data['bonuses']
            bonuses_description = rec_data['bonuses_description']
            reduction = rec_data['reduction']
            reduction_description = rec_data['reduction_description']
            insurance = rec_data['insurance']
            tax = rec_data['tax']
            total_price = rec_data['total_price']
            settle_type = rec_data['settle_type']
            backup_code = rec_data['backup_code']
            invoice_date = rec_data['invoice_date']
            factor_number = rec_data['factor_number']
            banking_id = rec_data.get('banking_id')


            if not branch_id or not employee_id or not factor_number or not invoice_date or not backup_code or not settle_type :
                return JsonResponse({ "error_msg": DATA_REQUIRE},status=400)
            if not total_price or not tax or not insurance or not reduction or not reduction_description or not bonuses or not bonuses_description or not base_salary or not over_time_pay or not benefits:
                return JsonResponse({ "error_msg": DATA_REQUIRE},status=400)

            branch_obj = Branch.objects.get(pk=branch_id)
            employee_obj = Employee.objects.get(pk=employee_id)
            now_time = datetime.datetime.now()

            if banking_id:
                try:
                    banking_obj = BankingBaseClass.objects.get(pk=banking_id)
                except:
                    return JsonResponse({"error_msg": BANKING_NOT_FOUND}, status=404)
            else:
                banking_obj = None

            invoice_date_split = invoice_date.split('/')
            invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
                                                int(invoice_date_split[0]), now_time.hour, now_time.now().minute,
                                                now_time.now().second).togregorian()

            last_invoice_obj = InvoiceSalary.objects.filter(branch=branch_obj).order_by('id').last()
            if last_invoice_obj:
                new_factor_number = last_invoice_obj.factor_number + 1
            else:
                new_factor_number = 1
            # if new_factor_number != factor_number:
            #     return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

            new_invoice = InvoiceSalary(
                branch=branch_obj,
                employee= employee_obj,
                description=description,
                base_salary=base_salary,
                over_time_pay= over_time_pay,
                benefits=benefits,
                bonuses=bonuses,
                bonuses_description=bonuses_description,
                reduction=reduction,
                reduction_description=reduction_description,
                insurance=insurance,
                tax=tax,
                total_price=total_price,
                invoice_date=invoice_date_g,
                factor_number=new_factor_number,
                backup_code=backup_code,
                settle_type=settle_type,
                banking=banking_obj,
            )
            new_invoice.save()

            return JsonResponse({"msg": "invoice salary created"}, status=200)



class InvoiceSalariesView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      {USER_PLANS_CHOICES['FREE']},
                                      branch_disable=True)
    def get(self, request,branch_id, *args, **kwargs):

        if not branch_id:
            return JsonResponse({"error_msg": DATA_REQUIRE},status=400)

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoiceSalary.objects.filter(branch=branch_obj).order_by('-id')[:100]
        invoices = []
        for invoice in invoice_objects:
            invoice_date = invoice.invoice_date.date()
            jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                       year=invoice_date.year)

            invoices.append({
                'id': invoice.pk,
                'factor_number': invoice.factor_number,
                'employee_name': invoice.employee.user.get_full_name(),
                'total_price': invoice.total_price,
                'settle_type': invoice.get_settle_type_display(),
                'backup_code': invoice.backup_code,
                'invoice_date': jalali_date.strftime("%Y/%m/%d"),
                'banking': invoice.banking.name if invoice.banking else "",
            })

        return JsonResponse({'invoices': invoices},status=200)
    


# def get_all_invoices(request):
#     if request.method == "POST":
#         rec_data = json.loads(request.read().decode('utf-8'))
#         username = rec_data['username']
#         branch_id = rec_data['branch_id']

#         if not request.session.get('is_logged_in', None) == username:
#             return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
#         if not branch_id:
#             return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

#         branch_obj = Branch.objects.get(pk=branch_id)
#         invoice_objects = InvoiceSettlement.objects.filter(branch=branch_obj).order_by('-id')[:100]
#         invoices = []
#         for invoice in invoice_objects:
#             invoice_date = invoice.created_time.date()
#             jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
#                                                        year=invoice_date.year)

#             invoices.append({
#                 'id': invoice.pk,
#                 'factor_number': invoice.factor_number,
#                 'supplier_name': invoice.supplier.name,
#                 'payment_amount': invoice.payment_amount,
#                 'settle_type': invoice.get_settle_type_display(),
#                 'backup_code': invoice.backup_code,
#                 'created_time': jalali_date.strftime("%Y/%m/%d"),
#                 'banking': invoice.banking.name if invoice.banking else "",
#             })

#         return JsonResponse({"response_code": 2, 'invoices': invoices})
#     return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


# def search_pays(request):
#     if request.method == "POST":
#         rec_data = json.loads(request.read().decode('utf-8'))
#         search_word = rec_data['search_word']
#         username = rec_data['username']

#         if not request.session.get('is_logged_in', None) == username:
#             return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
#         if not search_word:
#             return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#         items_searched = InvoiceSettlement.objects.filter(supplier__name__contains=search_word)
#         pays = []
#         for pay in items_searched:
#             invoice_date = pay.created_time.date()
#             jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
#                                                        year=invoice_date.year)
#             pays.append({
#                 'id': pay.pk,
#                 'factor_number': pay.factor_number,
#                 'supplier_name': pay.supplier.name,
#                 'payment_amount': pay.payment_amount,
#                 'settle_type': pay.get_settle_type_display(),
#                 'backup_code': pay.backup_code,
#                 'created_time': jalali_date.strftime("%Y/%m/%d")
#             })
#         return JsonResponse({"response_code": 2, 'pays': pays})
#     return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


# def delete_invoice_settlement(request):
#     if request.method == "POST":
#         rec_data = json.loads(request.read().decode('utf-8'))
#         invoice_id = rec_data['invoice_id']
#         username = rec_data['username']

#         if not request.session.get('is_logged_in', None) == username:
#             return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
#         if not invoice_id:
#             return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

#         invoice_obj = InvoiceSettlement.objects.get(pk=invoice_id)

#         invoice_obj.delete()

#         return JsonResponse({"response_code": 2})
#     return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})