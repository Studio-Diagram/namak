"""accountiboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from accounti.views import EmployeeView, boardgameView, MemberView, stockView, BranchView, InvoiceSaleView, \
    SupplierView, InvoicePurchaseView, InvoiceSettlementView, InvoiceExpenseView, InvoiceReturnView, \
    ExpenseCategoryView, ReserveView, CashView, TableView

urlpatterns = [
    path('api/login/', EmployeeView.login),
    path('api/checkLogin/', EmployeeView.check_login),
    path('api/getEmployees/', EmployeeView.get_employees),
    path('api/registerEmployee/', EmployeeView.register_employee),
    path('api/searchEmployee/', EmployeeView.search_employee),
    path('api/getEmployee/', EmployeeView.get_employee),
    path('api/getMenuCategory/', EmployeeView.get_menu_category),
    path('api/getMenuCategories/', EmployeeView.get_menu_categories),
    path('api/addMenuCategory/', EmployeeView.add_menu_category),
    path('api/searchMenuCategory/', EmployeeView.search_menu_category),
    path('api/getMenuItem/', EmployeeView.get_menu_item),
    path('api/getMenuItems/', EmployeeView.get_menu_items),
    path('api/addMenuItem/', EmployeeView.add_menu_item),
    path('api/searchMenuItem/', EmployeeView.search_menu_item),
    path('api/addBoardgame/', boardgameView.add_boardgame),
    path('api/getBoardgames/', boardgameView.get_boardgames),
    path('api/searchBoardgame/', boardgameView.search_boardgame),
    path('api/getBoardgame/', boardgameView.get_boardgame),
    path('api/addMember/', MemberView.add_member),
    path('api/getMembers/', MemberView.get_members),
    path('api/searchMember/', MemberView.search_member),
    path('api/getMember/', MemberView.get_member),
    path('api/addStock/', stockView.add_stock),
    path('api/getStocks/', stockView.get_stocks),
    path('api/searchStock/', stockView.search_stock),
    path('api/getStock/', stockView.get_stock),
    path('api/addBranch/', BranchView.add_branch),
    path('api/getBranches/', BranchView.get_branches),
    path('api/searchBranch/', BranchView.search_branch),
    path('api/getBranch/', BranchView.get_branch),
    path('api/getMenuItemsWithCategories/', EmployeeView.get_menu_items_with_categories),
    path('api/getTables/', EmployeeView.get_tables),
    path('api/addTable/', TableView.add_table),
    path('api/searchTable/', TableView.search_table),
    path('api/getTable/', TableView.get_table),
    path('api/getPrinters/', EmployeeView.get_printers),
    path('api/addInvoiceSales/', InvoiceSaleView.create_new_invoice_sales),
    path('api/getAllTodayInvoices/', InvoiceSaleView.get_all_today_invoices),
    path('api/getInvoice/', InvoiceSaleView.get_invoice),
    path('api/endCurrentGame/', InvoiceSaleView.end_current_game),
    path('api/getAllInvoiceGames/', InvoiceSaleView.get_all_invoice_games),
    path('api/addSupplier/', SupplierView.add_supplier),
    path('api/getSuppliers/', SupplierView.get_suppliers),
    path('api/getSupplier/', SupplierView.get_supplier),
    path('api/searchSupplier/', SupplierView.search_supplier),
    path('api/getMaterials/', InvoicePurchaseView.get_materials),
    path('api/searchMaterials/', InvoicePurchaseView.search_materials),
    path('api/addInvoicePurchase/', InvoicePurchaseView.create_new_invoice_purchase),
    path('api/getAllInvoicePurchases/', InvoicePurchaseView.get_all_invoices),
    path('api/getShopProducts/', InvoicePurchaseView.get_shop_products),
    path('api/getLastBuyPrice/', InvoicePurchaseView.get_last_buy_price),
    path('api/searchShopProducts/', InvoicePurchaseView.search_shop_products),
    path('api/getInvoicePurchase/', InvoicePurchaseView.get_invoice),
    path('api/getAllPays/', InvoiceSettlementView.get_all_invoices),
    path('api/addPay/', InvoiceSettlementView.create_new_invoice_settlement),
    path('api/searchPay/', InvoiceSettlementView.search_pays),
    path('api/getAllExpenses/', InvoiceExpenseView.get_all_invoices),
    path('api/addExpense/', InvoiceExpenseView.create_new_invoice_expense),
    path('api/searchExpense/', InvoiceExpenseView.search_expense),
    path('api/getAllReturns/', InvoiceReturnView.get_all_invoices),
    path('api/addReturn/', InvoiceReturnView.create_new_invoice_return),
    path('api/searchReturn/', InvoiceReturnView.search_return),
    path('api/getSumInPurchase/', SupplierView.get_sum_invoice_purchases_from_supplier),
    path('api/getSumInSettlement/', SupplierView.get_sum_invoice_settlements_from_supplier),
    path('api/getSumInExpense/', SupplierView.get_sum_invoice_expenses_from_supplier),
    path('api/getSumInReturn/', SupplierView.get_sum_invoice_return_from_supplier),
    path('api/getDetailInPurchase/', SupplierView.get_detail_invoice_purchases_from_supplier),
    path('api/getDetailInSettlement/', SupplierView.get_detail_invoice_settlements_from_supplier),
    path('api/getDetailInExpense/', SupplierView.get_detail_invoice_expenses_from_supplier),
    path('api/getDetailInReturn/', SupplierView.get_detail_invoice_returns_from_supplier),
    path('api/deleteItems/', InvoiceSaleView.delete_items),
    path('api/settleInvoiceSale/', InvoiceSaleView.settle_invoice_sale),
    path('api/getTodayStatus/', InvoiceSaleView.get_today_status),
    path('api/timeCalc/', InvoiceSaleView.calec_time),
    path('api/addExpenseCategory/', ExpenseCategoryView.add_expense_category),
    path('api/getAllExpenseCategories/', ExpenseCategoryView.get_all_expense_categories),
    path('api/searchExpenseCategory/', ExpenseCategoryView.search_expense_category),
    path('api/getExpenseCategory/', ExpenseCategoryView.get_expense_category),
    path('api/addReserve/', ReserveView.add_reserve),
    path('api/getAllReserves/', ReserveView.get_reserves),
    path('api/arriveReserve/', ReserveView.arrive_reserve),
    path('api/deleteReserve/', ReserveView.delete_reserve),
    path('api/getReserve/', ReserveView.get_reserve),
    path('api/printAfterSave/', InvoiceSaleView.print_after_save),
    path('api/printCash/', InvoiceSaleView.print_cash),
    path('api/addMaterial/', InvoicePurchaseView.add_material),
    path('api/addShopProduct/', InvoicePurchaseView.add_shop_product),
    path('api/getTodayCash/', EmployeeView.get_today_cash),
    path('api/getAllCashes/', CashView.get_all_cash),
    path('api/closeCash/', CashView.close_cash),
    path('api/openCash/', CashView.open_cash),
    path('api/checkCashExist/', CashView.check_cash_exist),
    path('api/logOut/', EmployeeView.log_out),
    path('api/getWorkingTime/', BranchView.get_working_time_for_reserve),
    path('api/getTodayForReserve/', ReserveView.get_today_for_reserve),
    path('api/deleteInvoicePurchase/', InvoicePurchaseView.delete_invoice_purchase),
    path('api/deleteInvoiceExpense/', InvoiceExpenseView.delete_invoice_expense),
    path('api/deleteInvoiceReturn/', InvoiceReturnView.delete_invoice_return),
    path('api/deleteInvoiceSettlement/', InvoiceSettlementView.delete_invoice_settlement),
    path('template/invoice-cash', InvoiceSaleView.print_cash_with_template),
    path('template/invoice-no-cash', InvoiceSaleView.print_after_save_template),
    path('admin/', admin.site.urls),
    url(r'^dashboard', TemplateView.as_view(template_name='dashboard.html')),
    url(r'^', TemplateView.as_view(template_name='index.html')),
]
