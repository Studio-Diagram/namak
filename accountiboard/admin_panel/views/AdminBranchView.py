from django.views import View
from django.shortcuts import render
from accounti.models import *
from django.http import HttpResponseRedirect, HttpResponse
from accountiboard.custom_permissions import *

class AdminBranchDetailView(View):

    @permission_decorator_class_based_simplified(session_authenticate_admin_panel)
    def get(self, request, branch_id, *args, **kwargs):
        context = {}

        try:
            current_branch = Branch.objects.get(pk=branch_id)
        except:
            return HttpResponse("Error 404: branch with that id was not found", status=404)


        cafe_owner = current_branch.organization.cafeowner_set.first().user
        employee_count = EmployeeToBranch.objects.filter(branch=current_branch).count()
        printer_count = Printer.objects.filter(branch=current_branch).count()
        menu_category_count = MenuCategory.objects.filter(branch=current_branch).count()
        boardgame_count = Boardgame.objects.filter(branch=current_branch).count()
        member_count = Member.objects.filter(organization=current_branch.organization).count()

        table_category_count = TableCategory.objects.filter(branch=current_branch).count()
        table_category = TableCategory.objects.filter(branch=current_branch)
        table_count = Table.objects.filter(category__in=[x.id for x in table_category]).count()

        game_count = Game.objects.filter(branch=current_branch).count()
        shop_product_count = ShopProduct.objects.filter(branch=current_branch).count()

        cash_count = Cash.objects.filter(branch=current_branch).count()
        invoice_sales_count = InvoiceSales.objects.filter(branch=current_branch).count()
        invoice_settlement_count = InvoiceSettlement.objects.filter(branch=current_branch).count()
        invoice_purchase_count = InvoicePurchase.objects.filter(branch=current_branch).count()
        invoice_expense_count = InvoiceExpense.objects.filter(branch=current_branch).count()
        invoice_return_count = InvoiceReturn.objects.filter(branch=current_branch).count()

        supplier_count = Supplier.objects.filter(organization=current_branch.organization).count()

        reservation_count = Reservation.objects.filter(branch=current_branch).count()

        lottery_count = Lottery.objects.filter(organization=current_branch.organization).count()


        context['branch'] = {
            'branch_name': current_branch.name,
            'branch_organization': current_branch.organization.name,
            'branch_cafeowner': f'{cafe_owner.first_name} {cafe_owner.last_name}',

            'branch_employee_count': employee_count,
            'branch_printer_count': printer_count,
            'branch_menu_category_count': menu_category_count,
            'branch_boardgame_count': boardgame_count,
            'branch_member_count': member_count,
            'branch_table_category_count': table_category_count,
            'branch_table_count': table_count,

            'branch_game_count': game_count,
            'branch_shop_product_count': shop_product_count,
            'branch_cash_count': cash_count,

            'branch_invoice_sales_count': invoice_sales_count,
            'branch_invoice_settlement_count': invoice_settlement_count,
            'branch_invoice_purchase_count': invoice_purchase_count,
            'branch_invoice_expense_count': invoice_expense_count,
            'branch_invoice_return_count': invoice_return_count,

            'branch_supplier_count': supplier_count,
            'branch_reservation_count': reservation_count,
            'branch_lottery_count': lottery_count,
        }  

        return render(request, 'admin_panel_branch_detail.html', context)

