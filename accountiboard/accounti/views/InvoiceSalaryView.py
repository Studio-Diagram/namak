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
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def post(self, request, invoice_id, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_salary_id = rec_data['id']

        if invoice_salary_id == 0:

            branch_id = rec_data['branch_id']
            employee_id = rec_data['employee_id']
            base_salary = rec_data['base_salary']
            description = rec_data['description']
            over_time_pay = rec_data['over_time_pay']
            over_time_pay_description = rec_data['over_time_pay_description']
            benefits = rec_data['benefits']
            benefits_description = rec_data['benefits_description']
            bonuses = rec_data['bonuses']
            bonuses_description = rec_data['bonuses_description']
            reduction = rec_data['reduction']
            reduction_description = rec_data['reduction_description']
            insurance = rec_data['insurance']
            tax = rec_data['tax']
            
            settle_type = rec_data['settle_type']
            backup_code = rec_data['backup_code']
            invoice_date = rec_data['invoice_date']
            factor_number = rec_data['factor_number']
            banking_id = rec_data.get('banking_id')


            if not branch_id or not employee_id or not factor_number or not invoice_date  or not settle_type :
                return JsonResponse({ "error_msg": DATA_REQUIRE},status=400)
            # if not total_price or not tax or not insurance or not reduction or not reduction_description or not bonuses or not bonuses_description or not base_salary or not over_time_pay or not benefits:
            #     return JsonResponse({ "error_msg": DATA_REQUIRE},status=400)

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
            total_price = int(base_salary) + int(over_time_pay) + int(benefits) + int(bonuses) - int(reduction) - int(insurance) - int(tax)
            new_invoice = InvoiceSalary(
                branch=branch_obj,
                employee= employee_obj,
                description=description,
                base_salary=base_salary,
                over_time_pay= over_time_pay,
                over_time_pay_description=over_time_pay_description,
                benefits=benefits,
                benefits_description=benefits_description,
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




    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def put(self, request, invoice_id, *args, **kwargs):
        rec_data = json.loads(request.read().decode('utf-8'))
        invoice_salary_id = rec_data['id'] 

        branch_id = rec_data['branch_id']
        employee_id = rec_data['employee_id']
        base_salary = rec_data['base_salary']
        description = rec_data['description']
        over_time_pay = rec_data['over_time_pay']
        over_time_pay_description = rec_data['over_time_pay_description']
        benefits = rec_data['benefits']
        benefits_description = rec_data['benefits_description']
        bonuses = rec_data['bonuses']
        bonuses_description = rec_data['bonuses_description']
        reduction = rec_data['reduction']
        reduction_description = rec_data['reduction_description']
        insurance = rec_data['insurance']
        tax = rec_data['tax']
        
        settle_type = rec_data['settle_type']
        backup_code = rec_data['backup_code']
        invoice_date = rec_data['invoice_date']
        factor_number = rec_data['factor_number']
        banking_id = rec_data.get('banking_id')


        if not branch_id or not employee_id or not factor_number or not invoice_date  or not settle_type :
            return JsonResponse({ "error_msg": DATA_REQUIRE},status=400)

        
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

        invoice_obj = InvoiceSalary.objects.get(pk=invoice_id)
        invoice_obj.employee = employee_obj
        invoice_obj.base_salary = base_salary
        invoice_obj.description = description
        invoice_obj.over_time_pay = over_time_pay
        invoice_obj.over_time_pay_description = over_time_pay_description
        invoice_obj.benefits = benefits
        invoice_obj.benefits_description = benefits_description
        invoice_obj.bonuses = bonuses 
        invoice_obj.bonuses_description = bonuses_description
        invoice_obj.reduction = reduction
        invoice_obj.reduction_description = reduction_description
        invoice_obj.insurance = insurance
        invoice_obj.tax = tax
        invoice_obj.total_price = int(base_salary) + int(over_time_pay) + int(benefits) + int(bonuses) - int(reduction) - int(insurance) - int(tax)
        invoice_obj.settle_type = settle_type
        invoice_obj.backup_code = backup_code
        invoice_obj.invoice_date = invoice_date_g
        invoice_obj.banking = banking_obj
        # if new_factor_number != factor_number:
        #     return JsonResponse({"response_code": 3, "error_msg": FACTOR_NUMBER_INVALID})
        invoice_obj.save()
        return JsonResponse({"msg":INVOICE_DELETED},status =200)




    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def get(self, request, invoice_id, *args, **kwargs):
        if not invoice_id:
            return JsonResponse({"error_msg": DATA_REQUIRE},status=400)

        invoice_obj = InvoiceSalary.objects.get(pk=invoice_id)
        try:
            banking_obj = BankingBaseClass.objects.get(pk=invoice_obj.banking.id)
        except:
            banking_obj = None
     
        invoice_date = invoice_obj.invoice_date.date()
        jalali_date = jdatetime.date.fromgregorian(day=invoice_date.day, month=invoice_date.month,
                                                    year=invoice_date.year)

        invoice_data = {
                'id': invoice_obj.pk,
                'factor_number': invoice_obj.factor_number,
                'employee_name': invoice_obj.employee.user.get_full_name(),
                'employee_id': invoice_obj.employee.id,
                'total_price': invoice_obj.total_price,
                'settle_type': invoice_obj.settle_type,
                'backup_code': invoice_obj.backup_code,
                'invoice_date': jalali_date.strftime("%d/%m/%Y"),
                'banking': {'id':banking_obj.id, 'name': banking_obj.name} if banking_obj else {'id': None},
                'base_salary': invoice_obj.base_salary,
                'over_time_pay':invoice_obj.over_time_pay,
                'benefits':invoice_obj.benefits,
                'bonuses':invoice_obj.bonuses,
                'reduction':invoice_obj.reduction,
                'insurance':invoice_obj.insurance,
                'tax':invoice_obj.tax,
                'over_time_pay_description':invoice_obj.over_time_pay_description,
                'benefits_description': invoice_obj.benefits_description,
                'bonuses_description':invoice_obj.bonuses_description,
                'reduction_description':invoice_obj.reduction_description,
                'description':invoice_obj.description,
                'branch_id': invoice_obj.branch.id,                
                
            }


        return JsonResponse({"invoice":invoice_data},status =200)




    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def delete(self, request, invoice_id, *args, **kwargs):
        if not invoice_id:
            return JsonResponse({"error_msg": DATA_REQUIRE},status=400)

        invoice_obj = InvoiceSalary.objects.get(pk=invoice_id)
        invoice_obj.delete()

        return JsonResponse({"msg":INVOICE_DELETED},status =200)






class InvoiceSalariesView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
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
    





class InvoiceSalarySearchView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
                                      ALLOW_ALL_PLANS,
                                      branch_disable=True)
    def get(self, request,branch_id,search_word, *args, **kwargs):

        if not search_word:
            return JsonResponse({"error_msg": DATA_REQUIRE},status=400)

        if not branch_id:
                return JsonResponse({"error_msg": DATA_REQUIRE},status=400)

        branch_obj = Branch.objects.get(pk=branch_id)
        invoice_objects = InvoiceSalary.objects.filter(branch=branch_obj)
        invoices = []
        for invoice in invoice_objects:
            if search_word in invoice.employee.user.get_full_name():
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
    




