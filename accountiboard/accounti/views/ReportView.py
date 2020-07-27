from accounti.models import *
from accountiboard.constants import *
from accountiboard.custom_permissions import *
from django.views import View
from django.shortcuts import get_object_or_404
import jdatetime
from django.db.models import Sum


class ReportView(View):
    @permission_decorator_class_based(token_authenticate,
                                      {USER_ROLES['CAFE_OWNER'], USER_ROLES['MANAGER'], USER_ROLES['ACCOUNTANT']},
									  {USER_PLANS_CHOICES['STANDARD_NORMAL']},
                                      branch_disable=True)
    def get(self, request, *args, **kwargs):
        invoice_type = request.GET.get('type')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        reports_data = []

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
                                                          is_settled=True)
            total_price_sum = invoice_objects.aggregate(Sum('total_price'))
            total_invoices = invoice_objects.count()
            reports_data = [{
                "id": invoice.pk,
                "price": invoice.total_price,
                "created_time": jdatetime.date.fromgregorian(day=invoice.created_time.day,
                                                             month=invoice.created_time.month,
                                                             year=invoice.created_time.year).strftime('%Y/%m/%d')
            } for invoice in invoice_objects]

            return JsonResponse({"results": reports_data, "total_invoices": total_invoices,
                                 "total_price": total_price_sum.get('total_price__sum')})

        return JsonResponse({"results": reports_data})
