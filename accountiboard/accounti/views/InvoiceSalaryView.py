from django.http import JsonResponse
from accounti.models import *
from datetime import datetime
import jdatetime, json
from accountiboard.constants import *

def create_new_invoice_salary(request):
    if request.method == "POST":
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
            bounses_description = rec_data['bounses_description']
            reduction = rec_data['reduction']
            reduction_description = rec_data['reduction_description']
            insurance = rec_data['reduction_description']
            tax = rec_data['tax']
            total_price = rec_data['total_price']
            username = rec_data['username']
            settle_type = rec_data['settle_type']
            backup_code = rec_data['backup_code']

            invoice_date = rec_data['date']
            factor_number = rec_data['factor_number']
            banking_id = rec_data.get('banking_id')

            if not username:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not request.session.get('is_logged_in', None) == username:
                return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
            if not branch_id or not employee_id or not factor_number or not invoice_date or not backup_code or not settle_type :
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
            if not total_price or not tax or not insurance or not reduction or not reduction_description or not bonuses or not bounses_description or not base_salary or not over_time_pay or not benefits:
                return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

            branch_obj = Branch.objects.get(pk=branch_id)
            employee_obj = Employee.objects.get(pk=employee_id)
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
                bounses_description=bounses_description,
                reduction=reduction,
                reduction_description=reduction_description,
                insurance=insurance,
                tax=tax,
                total_price=total_price,
                invoice_time=invoice_date_g,
                factor_number=new_factor_number,
                backup_code=backup_code,
                settle_type=settle_type,
                banking=banking_obj,
            )
            new_invoice.save()

            return JsonResponse({"response_code": 2})

        return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})

    return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})




# def create_new_invoice_settlement(request):
#     if request.method == "POST":
#         rec_data = json.loads(request.read().decode('utf-8'))
#         invoice_settlement_id = rec_data['id']

#         if invoice_settlement_id == 0:
#             supplier_id = rec_data['supplier_id']
#             payment_amount = rec_data['payment_amount']
#             username = rec_data['username']
#             settle_type = rec_data['settle_type']
#             backup_code = rec_data['backup_code']
#             branch_id = rec_data['branch_id']
#             invoice_date = rec_data['date']
#             factor_number = rec_data['factor_number']
#             banking_id = rec_data.get('banking_id')

#             if not username:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#             if not request.session.get('is_logged_in', None) == username:
#                 return JsonResponse({"response_code": 3, "error_msg": UNATHENTICATED})
#             if not branch_id:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#             if not payment_amount:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#             if supplier_id == 0:
#                 return JsonResponse({"response_code": 3, "error_msg": SUPPLIER_REQUIRE})
#             if not invoice_date:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#             if not settle_type:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#             if not factor_number:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})
#             if not banking_id:
#                 return JsonResponse({"response_code": 3, "error_msg": DATA_REQUIRE})

#             branch_obj = Branch.objects.get(pk=branch_id)
#             supplier_obj = Supplier.objects.get(pk=supplier_id)
#             now_time = datetime.now()

#             if banking_id:
#                 try:
#                     banking_obj = BankingBaseClass.objects.get(pk=banking_id)
#                 except:
#                     return JsonResponse({"error_msg": BANKING_NOT_FOUND}, status=404)
#             else:
#                 banking_obj = None

#             invoice_date_split = invoice_date.split('/')
#             invoice_date_g = jdatetime.datetime(int(invoice_date_split[2]), int(invoice_date_split[1]),
#                                                 int(invoice_date_split[0]), datetime.now().hour, datetime.now().minute,
#                                                 datetime.now().second).togregorian()

#             last_invoice_obj = InvoiceSettlement.objects.filter(branch=branch_obj).order_by('id').last()
#             if last_invoice_obj:
#                 new_factor_number = last_invoice_obj.factor_number + 1
#             else:
#                 new_factor_number = 1
#             if new_factor_number != factor_number:
#                 return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})

#             new_invoice = InvoiceSettlement(
#                 branch=branch_obj,
#                 payment_amount=payment_amount,
#                 settle_type=settle_type,
#                 backup_code=backup_code,
#                 supplier=supplier_obj,
#                 created_time=invoice_date_g,
#                 factor_number=new_factor_number,
#                 banking=banking_obj,
#             )
#             new_invoice.save()

#             return JsonResponse({"response_code": 2})

#         return JsonResponse({"response_code": 3, "error_msg": "Wrong ID!"})

#     return JsonResponse({"response_code": 4, "error_msg": "GET REQUEST!"})


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