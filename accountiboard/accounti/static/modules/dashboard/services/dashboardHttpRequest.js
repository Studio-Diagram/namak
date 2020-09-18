angular.module('dashboard')
    .service('dashboardHttpRequest', function dashboardHttpRequest($q, $http, $auth, $cookies, $window, $rootScope) {
        var service = {
            'API_URL': window.location.origin,
            'use_session': false,
            'authenticated': null,
            'authPromise': null,
            'request': function (args) {
                if ($auth.getToken()) {
                    $http.defaults.headers.common.Authorization = 'Bearer ' + $auth.getToken();
                }
                // Continue
                params = args.params || {};
                args = args || {};
                var deferred = $q.defer(),
                    url = this.API_URL + args.url,
                    method = args.method || "GET",
                    params = params,
                    data = args.data || {};
                // Fire the request, as configured.
                $http({
                    url: url,
                    withCredentials: this.use_session,
                    method: method.toUpperCase(),
                    headers: {'X-CSRFToken': $cookies.get("csrftoken")},
                    params: params,
                    data: data
                }).then(angular.bind(this, function (data, status, headers, config) {
                        deferred.resolve(data['data'], status);
                    }), angular.bind(this, function (data, status, headers, config) {
                        // There is a timeout or connection error in server
                        if (data.status === -1){
                            $window.location.href = "http://127.0.0.1:8001/dashboard#!/?user=" + $rootScope.user_data.username ;
                        }
                        deferred.reject(data, status, headers, config);
                    }));
                return deferred.promise;
            },
            'getEmployees': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getEmployees/",
                    'data': data
                });
            },
            'checkLogin': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/checkLogin/",
                    'data': data
                });
            },
            'registerEmployee': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/registerEmployee/",
                    'data': data
                });
            },
            'searchEmployee': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchEmployee/",
                    'data': data
                });
            },
            'getEmployee': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getEmployee/",
                    'data': data
                });
            },
            'addMenuCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addMenuCategory/",
                    'data': data
                });
            },
            'searchMenuCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchMenuCategory/",
                    'data': data
                });
            },
            'getMenuCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMenuCategory/",
                    'data': data
                });
            },
            'getMenuCategories': function (branch_id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/getMenuCategories/" + branch_id + "/"
                });
            },
            'getPrinters': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getPrinters/",
                    'data': data
                });
            },
            'addPrinter': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addPrinter/",
                    'data': data
                });
            },
            'getPrinter': function (printer_id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/getPrinter/" + printer_id + "/"
                });
            },
            'addMenuItem': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addMenuItem/",
                    'data': data
                });
            },
            'deleteMenuItem': function (item_id) {
                return this.request({
                    'method': "DELETE",
                    'url': "/api/deleteMenuItem/" + item_id + "/"
                });
            },
            'searchMenuItem': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchMenuItem/",
                    'data': data
                });
            },
            'getMenuItem': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMenuItem/",
                    'data': data
                });
            },
            'getMenuItems': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMenuItems/",
                    'data': data
                });
            },
            'addMember': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addMember/",
                    'data': data
                });
            },
            'getMembers': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMembers/",
                    'data': data
                });
            },
            'searchMember': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchMember/",
                    'data': data
                });
            },
            'getMember': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMember/",
                    'data': data
                });
            },
            'addBranch': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addBranch/",
                    'data': data
                });
            },
            'getBranches': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getBranches/",
                    'data': data
                });
            },
            'searchBranch': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchBranch/",
                    'data': data
                });
            },
            'getBranch': function (branch_id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/branch/" + branch_id + "/"
                });
            },
            'updateBranch': function (branch_id, data) {
                return this.request({
                    'method': "PUT",
                    'url': "/api/branch/" + branch_id + "/",
                    'data': data
                });
            },
            'getMenuItemsWithCategories': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMenuItemsWithCategories/",
                    'data': data
                });
            },
            'getTables': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getTables/",
                    'data': data
                });
            },
            'addInvoiceSales': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addInvoiceSales/",
                    'data': data
                });
            },
            'getAllTodayInvoices': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllTodayInvoices/",
                    'data': data
                });
            },
            'getInvoice': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getInvoice/",
                    'data': data
                });
            },
            'endCurrentGame': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/endCurrentGame/",
                    'data': data
                });
            },
            'getAllInvoiceGames': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllInvoiceGames/",
                    'data': data
                });
            },
            'addSupplier': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addSupplier/",
                    'data': data
                });
            },
            'getSuppliers': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSuppliers/",
                    'data': data
                });
            },
            'getSupplier': function (supplier_id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/supplier/" + supplier_id + "/",
                });
            },
            'deleteSupplier': function (supplier_id) {
                return this.request({
                    'method': "DELETE",
                    'url': "/api/supplier/" + supplier_id + "/",
                });
            },
            'searchSupplier': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchSupplier/",
                    'data': data
                });
            },
            'getMaterials': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMaterials/",
                    'data': data
                });
            },
            'searchMaterials': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchMaterials/",
                    'data': data
                });
            },
            'addInvoicePurchase': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addInvoicePurchase/",
                    'data': data
                });
            },
            'getAllInvoicePurchases': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllInvoicePurchases/",
                    'data': data
                });
            },
            'getInvoicePurchase': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getInvoicePurchase/",
                    'data': data
                });
            },
            'getShopProducts': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getShopProducts/",
                    'data': data
                });
            },
            'searchShopProducts': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchShopProducts/",
                    'data': data
                });
            },
            'getAllPays': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllPays/",
                    'data': data
                });
            },
            'addPay': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addPay/",
                    'data': data
                });
            },
            'searchPay': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchPay/",
                    'data': data
                });
            },
            'getAllExpenses': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllExpenses/",
                    'data': data
                });
            },
            'addExpense': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addExpense/",
                    'data': data
                });
            },
            'searchExpense': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchExpense/",
                    'data': data
                });
            },
            'getSumInPurchase': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSumInPurchase/",
                    'data': data
                });
            },
            'getSumInSettlement': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSumInSettlement/",
                    'data': data
                });
            },
            'getSumInExpense': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSumInExpense/",
                    'data': data
                });
            },
            'getSumInReturn': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSumInReturn/",
                    'data': data
                });
            },
            'getSumInAmaniSales': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSumInAmaniSales/",
                    'data': data
                });
            },
            'getDetailInPurchase': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getDetailInPurchase/",
                    'data': data
                });
            },
            'getDetailInSettlement': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getDetailInSettlement/",
                    'data': data
                });
            },
            'getDetailInExpense': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getDetailInExpense/",
                    'data': data
                });
            },
            'getDetailInReturn': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getDetailInReturn/",
                    'data': data
                });
            },
            'getDetailInAmaniSales': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getDetailInAmaniSales/",
                    'data': data
                });
            },
            'getAllReturns': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllReturns/",
                    'data': data
                });
            },
            'addReturn': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addReturn/",
                    'data': data
                });
            },
            'searchReturn': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchReturn/",
                    'data': data
                });
            },
            'getLastBuyPrice': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getLastBuyPrice/",
                    'data': data
                });
            },
            'deleteItems': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteItems/",
                    'data': data
                });
            },
            'settleInvoiceSale': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/settleInvoiceSale/",
                    'data': data
                });
            },
            'getTodayStatus': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/getTodayStatus/?branch_id=" + data.branch_id + "&cash_id=" + data.cash_id,
                });
            },
            'getKitchenDetailSales': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/getSaleDetailsByCategory/?branch_id=" + data.branch_id +
                    "&cash_id=" + data.cash_id + "&category=KITCHEN&menu_category_id=" + data.menu_category_id
                });
            },
            'getBarDetailSales': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/getSaleDetailsByCategory/?branch_id=" + data.branch_id +
                    "&cash_id=" + data.cash_id + "&category=BAR&menu_category_id=" + data.menu_category_id
                });
            },
            'getOtherDetailSales': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/getSaleDetailsByCategory/?branch_id=" + data.branch_id +
                    "&cash_id=" + data.cash_id + "&category=OTHER&menu_category_id=" + data.menu_category_id
                });
            },
            'addReserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addReserve/",
                    'data': data
                });
            },
            'getAllReserves': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllReserves/",
                    'data': data
                });
            },
            'arriveReserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/arriveReserve/",
                    'data': data
                });
            },
            'deleteReserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteReserve/",
                    'data': data
                });
            },
            'getReserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getReserve/",
                    'data': data
                });
            },
            'printAfterSave': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/printAfterSave/",
                    'data': data
                });
            },
            'printCash': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/printCash/",
                    'data': data
                });
            },
            'addMaterial': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addMaterial/",
                    'data': data
                });
            },
            'addShopProduct': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addShopProduct/",
                    'data': data
                });
            },
            'getTodayCash': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getTodayCash/",
                    'data': data
                });
            },
            'getAllCashes': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllCashes/",
                    'data': data
                });
            },
            'closeCash': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/closeCash/",
                    'data': data
                });
            },
            'openCash': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/openCash/",
                    'data': data
                });
            },
            'checkCashExist': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/checkCashExist/",
                    'data': data
                });
            },
            'getCashAndRelatedInvoices': function (cash_id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/invoiceSalesByCash/" + cash_id + "/"
                });
            },
            'logOut': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/logOut/",
                    'data': data
                });
            },
            'addTable': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addTable/",
                    'data': data
                });
            },
            'searchTable': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchTable/",
                    'data': data
                });
            },
            'getTable': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getTable/",
                    'data': data
                });
            },
            'getWorkingTime': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getWorkingTime/",
                    'data': data
                });
            },
            'getTodayForReserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getTodayForReserve/",
                    'data': data
                });
            },
            'deleteInvoicePurchase': function (item_id) {
                return this.request({
                    'method': "DELETE",
                    'url': "/api/deleteInvoicePurchase/" + item_id + "/"
                });
            },
            'deleteInvoiceExpense': function (item_id) {
                return this.request({
                    'method': "DELETE",
                    'url': "/api/deleteInvoiceExpense/" + item_id + "/"
                });
            },
            'deleteInvoiceReturn': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteInvoiceReturn/",
                    'data': data
                });
            },
            'deleteInvoiceSettlement': function (item_id) {
                return this.request({
                    'method': "DELETE",
                    'url': "/api/deleteInvoiceSettlement/" + item_id + "/"
                });
            },
            'getNextFactorNumber': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getNextFactorNumber/",
                    'data': data
                });
            },
            'addTableCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addTableCategory/",
                    'data': data
                });
            },
            'getTableCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getTableCategory/",
                    'data': data
                });
            },
            'getTableCategories': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getTableCategories/",
                    'data': data
                });
            },
            'changeMenuCategoryOrder': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/changeMenuCategoryOrder/",
                    'data': data
                });
            },
            'readyForSettle': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/readyForSettle/",
                    'data': data
                });
            },
            'getAllExpenseTags': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllExpenseTags/",
                    'data': data
                });
            },
            'deleteInvoiceSale': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteInvoiceSale/",
                    'data': data
                });
            },
            'getSupplierRemainder': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSupplierRemainder/",
                    'data': data
                });
            },
            'getMostUsedItemsForSupplier': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMostUsedItemsForSupplier/",
                    'data': data
                });
            },
            'getLotteries': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/get_lotteries/",
                    'data': data
                });
            },
            'addLottery': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/lottery/",
                    'data': data
                });
            },
            'givePrize': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/give_lottery_prize/",
                    'data': data
                });
            },
            'getWaitingList': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getWaitingList/",
                    'data': data
                });
            },
            'addWaitingList': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addWaitingList/",
                    'data': data
                });
            },
            'getAllInvoicesStateBase': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllInvoicesStateBase/",
                    'data': data
                });
            },
            'changeGameState': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/changeGameState/",
                    'data': data
                });
            },
            'doNotWantOrder': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/doNotWantOrder/",
                    'data': data
                });
            },
            'getAllLeftReserves': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllLeftReserves/",
                    'data': data
                });
            },
            'getAllNotComeReserves': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllNotComeReserves/",
                    'data': data
                });
            },
            'startInvoiceGame': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/startInvoiceGame/",
                    'data': data
                });
            },
            'performCredit': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/performCredit/",
                    'data': data
                });
            },
            'memberCredits': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/memberCredits/",
                    'data': data
                });
            },
            'createCredit': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/createCredit/",
                    'data': data
                });
            },
            'getCategoriesBaseOnKind': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getCategoriesBaseOnKind/",
                    'data': data
                });
            },
            'checkGiftCode': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/checkGiftCode/",
                    'data': data
                });
            },
            'editPaymentInvoiceSale': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/editPaymentInvoiceSale/",
                    'data': data
                });
            },
            'getUserProfile': function () {
                return this.request({
                    'method': "GET",
                    'url': "/api/profile/"
                });
            },
            'updateProfile': function (data) {
                return this.request({
                    'method': "PUT",
                    'url': "/api/profile/",
                    'data': data
                });
            },
            'changePassword': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/changePassword/",
                    'data': data
                });
            },
            'getReport': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/report/" + data
                });
            },
            'get_news': function () {
                return this.request({
                    'method': "GET",
                    'url': "/api/latestnews/"
                });
            },
            'bug_report': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/bugreport/",
                    'data': data
                });
            },

            'getBanking': function () {
                return this.request({
                    'method': "GET",
                    'url': "/api/banking/"
                });
            },
            'getBankingDetail': function (id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/banking/" + id + "/"
                });
            },
            'updateBankingDetail': function (id, data) {
                return this.request({
                    'method': "PUT",
                    'url': "/api/banking/" + id + "/",
                    'data': data
                });
            },
            'getBankingByBranch': function (id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/bankingByBranch/" + id + "/"
                });
            },
            'addBanking': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/banking/",
                    'data': data
                });
            },
            'getStocks': function () {
                return this.request({
                    'method': "GET",
                    'url': "/api/stocks/"
                });
            },
            'getStockDetail': function (id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/stocks/" + id + "/"
                });
            },
            'updateStockDetail': function (id, data) {
                return this.request({
                    'method': "PUT",
                    'url': "/api/stocks/" + id + "/",
                    'data': data
                });
            },
            'getStockByBranch': function (id) {
                return this.request({
                    'method': "GET",
                    'url': "/api/stocksByBranch/" + id + "/"
                });
            },
            'addStock': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/stocks/",
                    'data': data
                });
            },
            'getBundles': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/bundles/"
                });
            },
            'buyBundle': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/bundles/",
                    'data': data
                });
            },
            'getAllTransactions': function (data) {
                return this.request({
                    'method': "GET",
                    'url': "/api/transactions/"
                });
            },
            'payirVerifyGenToken': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/payirverify-gentoken/",
                    'data': data
                });
            },
            'checkBundleDiscount': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/check-subscription-discount/",
                    'data': data
                });
            },
            'addInvoiceSalary':function(data,id){
                return this.request({
                    'method':"POST",
                    'url': "/api/salary/"+ id +"/",
                    'data':data
                })
            },
            'deleteInvoiceSalary':function(item_id){
                return this.request({
                    'method':"DELETE",
                    'url': "/api/salary/"+ item_id +"/"

                })
            },
            'getInvoiceSalary':function(id){
                return this.request({
                    'method':"GET",
                    'url': "/api/salary/"+ id +"/"

                })
            },
            'editInvoiceSalary':function(data,id){
                return this.request({
                    'method':"PUT",
                    'url': "/api/salary/"+ id +"/",
                    'data':data

                })
            },
            'getSalaries':function(data){
                return this.request({
                    'method':"GET",
                    'url': "/api/salaries/"+ data +"/",


                })
            },
            'searchSalary':function(data,id){
                return this.request({
                    'method':"GET",
                    'url': "/api/searchSalary/"+ id +"/" + data +"/",


                })
            },
            'getBranchEmployees':function(id){
                return this.request({
                    'method':"GET",
                    'url': "/api/branchEmployees/"+ id +"/" ,


                })
            }
        };
        return service;

    });