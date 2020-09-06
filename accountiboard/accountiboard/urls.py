from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from accounti.views import EmployeeView, MemberView, stockView, BranchView, InvoiceSaleView, \
    SupplierView, InvoicePurchaseView, InvoiceSettlementView, InvoiceExpenseView, InvoiceReturnView, \
    ReserveView, CashView, TableView, GeneralInvoiceView, MenuCategoryView, ShopProductView, LotteryView, CreditView, \
    OfflineAPIs, UserView, ReportView, BundleView, BugReportView, LatestNewsView
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
    path('api/addInvoiceSales/', InvoiceSaleView.CreateNewInvoiceSaleView.as_view()),
    path('api/getAllTodayInvoices/', InvoiceSaleView.GetAllTodayInvoiceSalesView.as_view()),
    path('api/getInvoice/', InvoiceSaleView.GetInvoiceSaleView.as_view()),
    path('api/endCurrentGame/', InvoiceSaleView.EndCurrentGameView.as_view()),
    path('api/getAllInvoiceGames/', InvoiceSaleView.GetAllInvoiceGamesView.as_view()),
    path('api/addSupplier/', SupplierView.add_supplier),
    path('api/getSuppliers/', SupplierView.get_suppliers),
    path('api/getSupplier/', SupplierView.get_supplier),
    path('api/searchSupplier/', SupplierView.search_supplier),
    path('api/getMaterials/', InvoicePurchaseView.GetMaterialsView.as_view()),
    path('api/searchMaterials/', InvoicePurchaseView.SearchMaterialsView.as_view()),
    path('api/addInvoicePurchase/', InvoicePurchaseView.CreateNewInvoicePurchaseView.as_view()),
    path('api/getAllInvoicePurchases/', InvoicePurchaseView.GetAllInvoicesPurchaseView.as_view()),
    path('api/getShopProducts/', InvoicePurchaseView.GetShopProductsView.as_view()),
    path('api/getLastBuyPrice/', InvoicePurchaseView.GetLastBuyPriceView.as_view()),
    path('api/searchShopProducts/', InvoicePurchaseView.SearchShopProductsView.as_view()),
    path('api/getInvoicePurchase/', InvoicePurchaseView.GetInvoicePurchaseView.as_view()),
    path('api/getAllPays/', InvoiceSettlementView.GetAllInvoiceSettlementsView.as_view()),
    path('api/addPay/', InvoiceSettlementView.CreateNewInvoiceSettlementView.as_view()),
    path('api/searchPay/', InvoiceSettlementView.SearchPaysView.as_view()),
    path('api/getAllExpenses/', InvoiceExpenseView.GetAllInvoicesExpenseView.as_view()),
    path('api/addExpense/', InvoiceExpenseView.CreateNewInvoiceExpenseView.as_view()),
    path('api/searchExpense/', InvoiceExpenseView.SearchExpenseView.as_view()),
    path('api/getAllReturns/', InvoiceReturnView.GetAllInvoicesReturnView.as_view()),
    path('api/addReturn/', InvoiceReturnView.CreateNewInvoiceReturnView.as_view()),
    path('api/searchReturn/', InvoiceReturnView.SearchInvoicesReturnView.as_view()),
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
    path('api/deleteItems/', InvoiceSaleView.DeleteItemsView.as_view()),
    path('api/settleInvoiceSale/', InvoiceSaleView.SettleInvoiceSaleView.as_view()),
    path('api/getTodayStatus/', InvoiceSaleView.GetTodayStatusView.as_view()),
    path('api/getKitchenDetailSales/', InvoiceSaleView.GetKitchenSaleDetailView.as_view()),
    path('api/getBarDetailSales/', InvoiceSaleView.GetBarSaleDetailView.as_view()),
    path('api/getOtherDetailSales/', InvoiceSaleView.GetOtherSaleDetailView.as_view()),
    path('api/addReserve/', ReserveView.AddReserveView.as_view()),
    path('api/getAllReserves/', ReserveView.GetReservesView.as_view()),
    path('api/arriveReserve/', ReserveView.ArriveReserveView.as_view()),
    path('api/deleteReserve/', ReserveView.DeleteReserveView.as_view()),
    path('api/getReserve/', ReserveView.GetReserveView.as_view()),
    path('api/printAfterSave/', InvoiceSaleView.PrintAfterSaveView.as_view()),
    path('api/printCash/', InvoiceSaleView.PrintCashView.as_view()),
    path('api/addMaterial/', InvoicePurchaseView.AddMaterialView.as_view()),
    path('api/addShopProduct/', InvoicePurchaseView.AddShopProductView.as_view()),
    path('api/getTodayCash/', EmployeeView.GetTodayCashView.as_view()),
    path('api/getAllCashes/', CashView.GetAllCashView.as_view()),
    path('api/closeCash/', CashView.CloseCashView.as_view()),
    path('api/openCash/', CashView.OpenCashView.as_view()),
    path('api/checkCashExist/', CashView.CheckCashExistView.as_view()),
    path('api/getWorkingTime/', BranchView.GetWorkingTimeForReserveView.as_view()),
    path('api/getTodayForReserve/', ReserveView.GetTodayForReserveView.as_view()),
    path('api/deleteInvoicePurchase/', InvoicePurchaseView.DeleteInvoicePurchaseView.as_view()),
    path('api/deleteInvoiceExpense/', InvoiceExpenseView.DeleteInvoiceExpenseView.as_view()),
    path('api/deleteInvoiceReturn/', InvoiceReturnView.DeleteInvoicesReturnView.as_view()),
    path('api/deleteInvoiceSettlement/', InvoiceSettlementView.DeleteInvoiceSettlementView.as_view()),
    path('api/getNextFactorNumber/', GeneralInvoiceView.GetInvoiceNumberView.as_view()),
    path('api/addTableCategory/', TableView.AddTableCategoryView.as_view()),
    path('api/getTableCategory/', TableView.GetTableCategoryView.as_view()),
    path('api/getTableCategories/', TableView.GetTableCategoriesView.as_view()),
    path('api/changeMenuCategoryOrder/', MenuCategoryView.ChangeListOrderView.as_view()),
    path('api/getCategoriesBaseOnKind/', MenuCategoryView.GetCategoriesBasedOnKindView.as_view()),
    path('api/readyForSettle/', InvoiceSaleView.ReadyForSettleView.as_view()),
    path('api/getAllExpenseTags/', InvoiceExpenseView.GetAllTagsView.as_view()),
    path('api/deleteInvoiceSale/', InvoiceSaleView.DeleteInvoiceSaleView.as_view()),
    path('api/getSupplierRemainder/', SupplierView.get_remainder_supplier),
    path('api/createAllSuppliersExcel/', SupplierView.create_all_supplier_excel),
    path('api/createAllMaterialsExcel/', SupplierView.create_all_materials_buy),
    path('api/getDetailProductNumber/', ShopProductView.GetDetailProductNumberView.as_view()),
    path('api/getMostUsedItemsForSupplier/', SupplierView.get_supplier_purchase_item_used),
    path('api/getWaitingList/', ReserveView.GetWaitingListReservesView.as_view()),
    path('api/addWaitingList/', ReserveView.AddWaitingListView.as_view()),
    path('api/getAllInvoicesStateBase/', InvoiceSaleView.GetDashboardQuickAccessInvoicesView.as_view()),
    path('api/changeGameState/', InvoiceSaleView.ChangeGameStateView.as_view()),
    path('api/doNotWantOrder/', InvoiceSaleView.DoNotWantOrderView.as_view()),
    path('api/startInvoiceGame/', InvoiceSaleView.StartInvoiceGameView.as_view()),
    path('api/getAllLeftReserves/', ReserveView.GetAllTodayLeftReservesWithHourView.as_view()),
    path('api/getAllNotComeReserves/', ReserveView.GetAllTodayNotCameReservesView.as_view()),
    path('api/lottery/', LotteryView.LotteryView.as_view()),
    path('api/get_lotteries/', LotteryView.LotteryListView.as_view()),
    path('api/give_lottery_prize/', LotteryView.GivePrizeView.as_view()),
    path('api/performCredit/', CreditView.PerformCreditOnInvoiceSaleView.as_view()),
    path('api/memberCredits/', CreditView.GetAllCreditsDataFromUserView.as_view()),
    path('api/createCredit/', CreditView.CreateCreditView.as_view()),
    path('api/getYourInvoices/', InvoiceSaleView.GetAllInvoiceSaleWithDateView.as_view()),
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

    path('api/editPaymentInvoiceSale/', InvoiceSaleView.EditPaymentInvoiceSaleView.as_view()),
    path('template/night-report', InvoiceSaleView.NightReportTemplateView.as_view()),
    path('template/invoice-cash', InvoiceSaleView.PrintCashWithTemlateView.as_view()),
    path('template/invoice-no-cash', InvoiceSaleView.PrintAfterSaveTemlateView.as_view()),
    path('api/do_sync/', include('accounti.offline_syncer_urls')),
    path('admin/', admin.site.urls),
    url(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^dashboard', TemplateView.as_view(template_name='dashboard.html')),
    url(r'^mobile', TemplateView.as_view(template_name='mobile.html')),
    url(r'^', TemplateView.as_view(template_name='index.html')),

]
