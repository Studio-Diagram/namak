from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View
import jdatetime
from django.db.models import Sum


class ReportView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
									  {USER_PLANS_CHOICES['STANDARDNORMAL']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):
        invoice_type = request.GET.get('type')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        branches = request.GET.get('branches')
        suppliers = request.GET.get('suppliers')
        settlement_types = request.GET.get('s_types')
        reports_data = []

        if not branches or not invoice_type or not start_date or not end_date:
            return JsonResponse({"error_msg": DATA_REQUIRE}, status=400)

        if branches:
            branches = list(map(int, branches.split(',')))

        try:
            start_date_split = start_date.split('/')
            start_date_gregorian = jdatetime.date(int(start_date_split[2]), int(start_date_split[1]),
                                                  int(start_date_split[0])).togregorian()
            end_date_split = end_date.split('/')
            end_date_gregorian = jdatetime.date(int(end_date_split[2]), int(end_date_split[1]),
                                                int(end_date_split[0])).togregorian() + jdatetime.timedelta(days=1)
        except Exception as e:
            return JsonResponse({
                'error_msg': TIME_NOT_IN_CORRECT_FORMAT
            }, status=400)

        if invoice_type == "INVOICE_SALE":
            invoice_objects = InvoiceSales.objects.filter(created_time__gte=start_date_gregorian,
                                                          created_time__lte=end_date_gregorian, is_deleted=False,
                                                          is_settled=True, branch_id__in=branches)
            total_price_sum = invoice_objects.aggregate(Sum('total_price'))
            total_invoices = invoice_objects.count()
            reports_data = [{
                "id": invoice.pk,
                "price": invoice.total_price,
                "created_time": jdatetime.date.fromgregorian(day=invoice.created_time.day,
                                                             month=invoice.created_time.month,
                                                             year=invoice.created_time.year).strftime('%Y/%m/%d'),
                "branch_name": invoice.branch.name
            } for invoice in invoice_objects]

            return JsonResponse({"results": reports_data, "total_invoices": total_invoices,
                                 "total_price": total_price_sum.get('total_price__sum') if total_price_sum.get(
                                     'total_price__sum') else 0})

        elif invoice_type == "INVOICE_PURCHASE":
            invoice_objects = InvoicePurchase.objects.filter(created_time__gte=start_date_gregorian,
                                                             created_time__lte=end_date_gregorian,
                                                             branch_id__in=branches)
            if suppliers:
                suppliers = list(map(int, suppliers.split(',')))
                invoice_objects = invoice_objects.filter(supplier_id__in=suppliers)
            if settlement_types:
                settlement_types = settlement_types.split(',')
                invoice_objects = invoice_objects.filter(settlement_type__in=settlement_types)

            total_price_sum = invoice_objects.aggregate(Sum('total_price'))
            total_invoices = invoice_objects.count()
            reports_data = [{
                "id": invoice.pk,
                "price": invoice.total_price,
                "created_time": jdatetime.date.fromgregorian(day=invoice.created_time.day,
                                                             month=invoice.created_time.month,
                                                             year=invoice.created_time.year).strftime('%Y/%m/%d'),
                "branch_name": invoice.branch.name,
                "supplier": invoice.supplier.name,
                "settlement_type": invoice.get_settlement_type_display()
            } for invoice in invoice_objects]

            return JsonResponse({"results": reports_data, "total_invoices": total_invoices,
                                 "total_price": total_price_sum.get('total_price__sum') if total_price_sum.get(
                                     'total_price__sum') else 0})

        elif invoice_type == "INVOICE_PAY":
            invoice_objects = InvoiceSettlement.objects.filter(created_time__gte=start_date_gregorian,
                                                               created_time__lte=end_date_gregorian,
                                                               branch_id__in=branches)
            if suppliers:
                suppliers = list(map(int, suppliers.split(',')))
                invoice_objects = invoice_objects.filter(supplier_id__in=suppliers)

            total_price_sum = invoice_objects.aggregate(Sum('payment_amount'))
            total_invoices = invoice_objects.count()
            reports_data = [{
                "id": invoice.pk,
                "price": invoice.payment_amount,
                "created_time": jdatetime.date.fromgregorian(day=invoice.created_time.day,
                                                             month=invoice.created_time.month,
                                                             year=invoice.created_time.year).strftime('%Y/%m/%d'),
                "branch_name": invoice.branch.name,
                "supplier": invoice.supplier.name,
                "settle_type": invoice.get_settle_type_display(),
                "backup_code": invoice.backup_code
            } for invoice in invoice_objects]

            return JsonResponse({"results": reports_data, "total_invoices": total_invoices,
                                 "total_price": total_price_sum.get('payment_amount__sum') if total_price_sum.get(
                                     'payment_amount__sum') else 0})

        elif invoice_type == "INVOICE_EXPENSE":
            invoice_objects = InvoiceExpense.objects.filter(created_time__gte=start_date_gregorian,
                                                            created_time__lte=end_date_gregorian,
                                                            branch_id__in=branches)
            if suppliers:
                suppliers = list(map(int, suppliers.split(',')))
                invoice_objects = invoice_objects.filter(supplier_id__in=suppliers)
            if settlement_types:
                settlement_types = settlement_types.split(',')
                invoice_objects = invoice_objects.filter(settlement_type__in=settlement_types)

            total_price_sum = invoice_objects.aggregate(Sum('price'))
            total_invoices = invoice_objects.count()
            reports_data = [{
                "id": invoice.pk,
                "price": invoice.price,
                "created_time": jdatetime.date.fromgregorian(day=invoice.created_time.day,
                                                             month=invoice.created_time.month,
                                                             year=invoice.created_time.year).strftime('%Y/%m/%d'),
                "branch_name": invoice.branch.name,
                "supplier": invoice.supplier.name,
                "expense_category": invoice.get_expense_kind_display(),
                "settlement_type": invoice.get_settlement_type_display()
            } for invoice in invoice_objects]

            return JsonResponse({"results": reports_data, "total_invoices": total_invoices,
                                 "total_price": total_price_sum.get('price__sum') if total_price_sum.get(
                                     'price__sum') else 0})

        elif invoice_type == "INVOICE_RETURN":
            invoice_objects = InvoiceReturn.objects.filter(created_time__gte=start_date_gregorian,
                                                           created_time__lte=end_date_gregorian,
                                                           branch_id__in=branches)
            if suppliers:
                suppliers = list(map(int, suppliers.split(',')))
                invoice_objects = invoice_objects.filter(supplier_id__in=suppliers)

            total_price_sum = invoice_objects.aggregate(Sum('total_price'))
            total_invoices = invoice_objects.count()
            reports_data = [{
                "id": invoice.pk,
                "price": invoice.total_price,
                "created_time": jdatetime.date.fromgregorian(day=invoice.created_time.day,
                                                             month=invoice.created_time.month,
                                                             year=invoice.created_time.year).strftime('%Y/%m/%d'),
                "branch_name": invoice.branch.name,
                "supplier": invoice.supplier.name if invoice.supplier else '',
                "shop_name": invoice.shop_product.name,
                "numbers": invoice.numbers,
                "return_type": invoice.get_return_type_display(),
                "description": invoice.description
            } for invoice in invoice_objects]

            return JsonResponse({"results": reports_data, "total_invoices": total_invoices,
                                 "total_price": total_price_sum.get('total_price__sum') if total_price_sum.get(
                                     'total_price__sum') else 0})

        return JsonResponse({"results": reports_data})
