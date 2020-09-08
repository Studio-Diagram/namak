from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from accounti.views import EmployeeView, boardgameView, MemberView, stockView, BranchView, InvoiceSaleView, \
    SupplierView, InvoicePurchaseView, InvoiceSettlementView, InvoiceExpenseView, InvoiceReturnView, \
    ReserveView, CashView, TableView, GeneralInvoiceView, MenuCategoryView, ShopProductView, LotteryView, CreditView, \
    OfflineAPIs, UserView, ReportView, BundleView, BugReportView, LatestNewsView, InvoiceSalaryView
from accountiboard import settings
from django.views.static import serve
from accounti.views import BankingView
from accounti.views import StocksView

from admin_panel.views import AdminGeneralView, AdminNewsView, AdminBugReportView, AdminBranchView, AdminLoginView
from django.conf.urls.static import static

urlpatterns = [
    path('api/login/', EmployeeView.LoginView.as_view()),
    path('api/getEmployees/', EmployeeView.GetEmployeesView.as_view()),
    path('api/registerEmployee/', EmployeeView.RegisterEmployeeView.as_view()),
    path('api/user/', UserView.register_user),
    path('api/searchEmployee/', EmployeeView.SearchEmployeeView.as_view()),
    path('api/getEmployee/', EmployeeView.GetEmployeeView.as_view()),
    path('api/getMenuCategory/', EmployeeView.GetMenuCategoryView.as_view()),
    path('api/getMenuCategories/', EmployeeView.GetMenuCategoriesView.as_view()),
    path('api/addMenuCategory/', EmployeeView.AddMenuCategoryView.as_view()),
    path('api/searchMenuCategory/', EmployeeView.SearchMenuCategoryView.as_view()),
    path('api/getMenuItem/', EmployeeView.GetMenuItemView.as_view()),
    path('api/getMenuItems/', EmployeeView.GetMenuItemsView.as_view()),
    path('api/addMenuItem/', EmployeeView.AddMenuItemView.as_view()),
    path('api/deleteMenuItem/', EmployeeView.DeleteMenuItemView.as_view()),
    path('api/searchMenuItem/', EmployeeView.SearchMenuItemView.as_view()),
    path('api/addBoardgame/', boardgameView.add_boardgame),
    path('api/getBoardgames/', boardgameView.get_boardgames),
    path('api/searchBoardgame/', boardgameView.search_boardgame),
    path('api/getBoardgame/', boardgameView.get_boardgame),
    path('api/addMember/', MemberView.AddMemberView.as_view()),
    path('api/getMembers/', MemberView.GetMembersView.as_view()),
    path('api/searchMember/', MemberView.SearchMemberView.as_view()),
    path('api/getMember/', MemberView.GetMemberView.as_view()),
    path('api/addStock/', stockView.add_stock),
    path('api/getStocks/', stockView.get_stocks),
    path('api/searchStock/', stockView.search_stock),
    path('api/getStock/', stockView.get_stock),
    path('api/addBranch/', BranchView.AddBranchView.as_view()),
    path('api/getBranches/', BranchView.GetBranchesView.as_view()),
    path('api/searchBranch/', BranchView.SearchBranchView.as_view()),
    path('api/getBranch/', BranchView.GetBranchView.as_view()),
    path('api/getMenuItemsWithCategories/', EmployeeView.GetMenuItemsWithCategoriesView.as_view()),
    path('api/getTables/', TableView.GetTablesView.as_view()),
    path('api/addTable/', TableView.AddTableView.as_view()),
    path('api/searchTable/', TableView.SearchTableView.as_view()),
    path('api/getTable/', TableView.GetTableView.as_view()),
    path('api/getPrinters/', EmployeeView.GetPrintersView.as_view()),
    path('api/getPrinter/<int:printer_id>/', EmployeeView.GetPrinterView.as_view()),
    path('api/addPrinter/', EmployeeView.AddPrinterView.as_view()),
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
    path('api/getSumInAmaniSales/', SupplierView.get_sum_amani_sales_from_supplier),
    path('api/getDetailInPurchase/', SupplierView.get_detail_invoice_purchases_from_supplier),
    path('api/getDetailInSettlement/', SupplierView.get_detail_invoice_settlements_from_supplier),
    path('api/getDetailInExpense/', SupplierView.get_detail_invoice_expenses_from_supplier),
    path('api/getDetailInReturn/', SupplierView.get_detail_invoice_returns_from_supplier),
    path('api/getDetailInAmaniSales/', SupplierView.get_detail_amani_sales_from_supplier),
    path('api/deleteItems/', InvoiceSaleView.delete_items),
    path('api/settleInvoiceSale/', InvoiceSaleView.settle_invoice_sale),
    path('api/getTodayStatus/', InvoiceSaleView.get_today_status),
    path('api/getKitchenDetailSales/', InvoiceSaleView.get_kitchen_sail_detail),
    path('api/getBarDetailSales/', InvoiceSaleView.get_bar_sail_detail),
    path('api/getOtherDetailSales/', InvoiceSaleView.get_other_sail_detail),
    path('api/timeCalc/', InvoiceSaleView.calec_time),
    path('api/addReserve/', ReserveView.add_reserve),
    path('api/getAllReserves/', ReserveView.get_reserves),
    path('api/arriveReserve/', ReserveView.arrive_reserve),
    path('api/deleteReserve/', ReserveView.delete_reserve),
    path('api/getReserve/', ReserveView.get_reserve),
    path('api/printAfterSave/', InvoiceSaleView.print_after_save),
    path('api/printCash/', InvoiceSaleView.print_cash),
    path('api/addMaterial/', InvoicePurchaseView.add_material),
    path('api/addShopProduct/', InvoicePurchaseView.add_shop_product),
    path('api/getTodayCash/', EmployeeView.GetTodayCashView.as_view()),
    path('api/getAllCashes/', CashView.get_all_cash),
    path('api/closeCash/', CashView.close_cash),
    path('api/openCash/', CashView.open_cash),
    path('api/checkCashExist/', CashView.check_cash_exist),
    path('api/getWorkingTime/', BranchView.GetWorkingTimeForReserveView.as_view()),
    path('api/getTodayForReserve/', ReserveView.get_today_for_reserve),
    path('api/deleteInvoicePurchase/', InvoicePurchaseView.delete_invoice_purchase),
    path('api/deleteInvoiceExpense/', InvoiceExpenseView.delete_invoice_expense),
    path('api/deleteInvoiceReturn/', InvoiceReturnView.delete_invoice_return),
    path('api/deleteInvoiceSettlement/', InvoiceSettlementView.delete_invoice_settlement),
    path('api/getNextFactorNumber/', GeneralInvoiceView.get_invoice_number),
    path('api/addTableCategory/', TableView.AddTableCategoryView.as_view()),
    path('api/getTableCategory/', TableView.GetTableCategoryView.as_view()),
    path('api/getTableCategories/', TableView.GetTableCategoriesView.as_view()),
    path('api/changeMenuCategoryOrder/', MenuCategoryView.ChangeListOrderView.as_view()),
    path('api/getCategoriesBaseOnKind/', MenuCategoryView.GetCategoriesBasedOnKindView.as_view()),
    path('api/readyForSettle/', InvoiceSaleView.ready_for_settle),
    path('api/getAllExpenseTags/', InvoiceExpenseView.get_all_tags),
    path('api/deleteInvoiceSale/', InvoiceSaleView.delete_invoice),
    path('api/getSupplierRemainder/', SupplierView.get_remainder_supplier),
    path('api/createAllSuppliersExcel/', SupplierView.create_all_supplier_excel),
    path('api/createAllMaterialsExcel/', SupplierView.create_all_materials_buy),
    path('api/getDetailProductNumber/', ShopProductView.GetDetailProductNumberView.as_view()),
    path('api/getMostUsedItemsForSupplier/', SupplierView.get_supplier_purchase_item_used),
    path('api/getWaitingList/', ReserveView.get_waiting_list_reserves),
    path('api/addWaitingList/', ReserveView.add_waiting_list),
    path('api/getAllInvoicesStateBase/', InvoiceSaleView.get_dashboard_quick_access_invoices),
    path('api/changeGameState/', InvoiceSaleView.change_game_state),
    path('api/doNotWantOrder/', InvoiceSaleView.do_not_want_order),
    path('api/startInvoiceGame/', InvoiceSaleView.start_invoice_game),
    path('api/getAllLeftReserves/', ReserveView.get_all_today_left_reserves_with_hour),
    path('api/getAllNotComeReserves/', ReserveView.get_all_today_not_come_reserves),
    path('api/lottery/', LotteryView.lottery),
    path('api/get_lotteries/', LotteryView.lottery_list),
    path('api/give_lottery_prize/', LotteryView.give_prize),
    path('api/performCredit/', CreditView.PerformCreditOnInvoiceSaleView.as_view()),
    path('api/memberCredits/', CreditView.GetAllCreditsDataFromUserView.as_view()),
    path('api/createCredit/', CreditView.CreateCreditView.as_view()),
    path('api/getYourInvoices/', InvoiceSaleView.get_all_invoices_with_date),
    path('api/createManualGiftCode/', CreditView.CreateGiftCodeManualView.as_view()),
    path('api/checkGiftCode/', CreditView.CheckGiftCodeView.as_view()),
    path('api/profile/', UserView.ProfileView.as_view()),
    path('api/changePassword/', UserView.ChangePasswordView.as_view()),
    path('api/report/', ReportView.ReportView.as_view()),

    path('api/bundles/', BundleView.BundleView.as_view()),
    path('api/payir/callback/', BundleView.PayirCallbackView.as_view()),
    path('api/check-subscription-discount/', BundleView.CheckSubscriptionDiscountView.as_view()),

    path('api/kick_unkick_employee/', EmployeeView.KickUnkickEmployeeView.as_view()),

    path('api/phone-verify/', UserView.PhoneVerifyView.as_view()),
    path('api/register-cafeowner/', UserView.RegisterCafeOwnerView.as_view()),
    path('api/forgotpassword/', UserView.ForgotPasswordView.as_view()),

    path('api/bugreport/', BugReportView.BugReportView.as_view()),
    path('api/latestnews/', LatestNewsView.LatestNewsView.as_view()),

    path('api/banking/<int:id>/', BankingView.BankingDetailView.as_view()),
    path('api/banking/', BankingView.BankingView.as_view()),
    path('api/bankingByBranch/<str:branch_id>/', BankingView.BankingByBranchView.as_view()),

    path('api/stocks/<int:id>/', StocksView.StockDetailView.as_view()),
    path('api/stocks/', StocksView.StocksView.as_view()),
    path('api/stocksByBranch/<str:branch_id>/', StocksView.StockByBranchView.as_view()),
    path('api/salary/<int:invoice_id>/', InvoiceSalaryView.InvoiceSalaryView.as_view()),
    path('api/salaries/<str:branch_id>/', InvoiceSalaryView.InvoiceSalariesView.as_view()),

    # Offline APIs URLs
    path('api/offline/status/', OfflineAPIs.status_of_server),
    path('api/offline/list/member/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_member_list),
    path('api/offline/list/menu_category/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_menu_category_list),
    path('api/offline/list/menu_item/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_menu_item_list),
    path('api/offline/list/printer/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_printer_list),
    path('api/offline/list/printer_to_category/<int:last_uuid>/<str:branch>/',
         OfflineAPIs.sync_printer_to_category_list),
    path('api/offline/list/table_category/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_table_category_list),
    path('api/offline/list/table/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_table_list),
    path('api/offline/list/branch/<str:branch>/', OfflineAPIs.sync_branch_list),
    path('api/offline/list/cash/<int:last_uuid>/<str:branch>/', OfflineAPIs.sync_cash_list),
    path('api/offline/list/employee/<str:branch>/', OfflineAPIs.sync_employee_list),
    path('api/offline/list/invoice_sale/', OfflineAPIs.sync_invoice_sales_list),
    path('api/offline/list/reserve/<int:branch_id>/', OfflineAPIs.sync_reserve_list),
    path('api/offline/syncReservesFromOffline/', OfflineAPIs.sync_reserves_from_offline),
    path('api/offline/syncInvoiceSalesFromOffline/', OfflineAPIs.sync_invoice_sales_from_offline),
    # End of offline APIs URLs

    # Admin panel
    path('onward/', AdminGeneralView.AdminView.as_view()),
    path('onward/login/', AdminLoginView.AdminLoginView.as_view()),
    path('onward/logout/', AdminLoginView.AdminLogoutView.as_view()),
    path('onward/news/', AdminNewsView.AdminNewsView.as_view()),
    path('onward/news/create/', AdminNewsView.AdminNewsCreateView.as_view()),
    path('onward/news/delete/<int:latestnews_id>/', AdminNewsView.AdminNewsDeleteView.as_view()),
    path('onward/bugreports/', AdminBugReportView.AdminBugReportsView.as_view()),
    path('onward/bugreports/<int:bugreport_id>/', AdminBugReportView.AdminBugReportsDetailView.as_view()),
    path('onward/branches/<int:branch_id>/', AdminBranchView.AdminBranchDetailView.as_view()),

    path('api/editPaymentInvoiceSale/', InvoiceSaleView.edit_payment_invoice_sale),
    path('template/night-report', InvoiceSaleView.night_report_template),
    path('template/invoice-cash', InvoiceSaleView.print_cash_with_template),
    path('template/invoice-no-cash', InvoiceSaleView.print_after_save_template),
    path('api/do_sync/', include('accounti.offline_syncer_urls')),
    path('admin/', admin.site.urls),
    url(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^dashboard', TemplateView.as_view(template_name='dashboard.html')),
    url(r'^mobile', TemplateView.as_view(template_name='mobile.html')),
    url(r'^', TemplateView.as_view(template_name='index.html')),
    # salaryInvoices


]
