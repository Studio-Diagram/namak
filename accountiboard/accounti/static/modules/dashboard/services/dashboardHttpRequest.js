angular.module('dashboard')
    .service('dashboardHttpRequest', function dashboardHttpRequest($q, $http, $auth, $cookies) {
        var service = {
            'API_URL': window.location.origin,
            'use_session': false,
            'authenticated': null,
            'authPromise': null,
            'request': function (args) {
                if ($auth.getToken()) {
                    $http.defaults.headers.common.Authorization = 'Token ' + $auth.getToken();
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
                })
                    .success(angular.bind(this, function (data, status, headers, config) {
                        deferred.resolve(data, status);
                    }))
                    .error(angular.bind(this, function (data, status, headers, config) {
                        console.log("error syncing with: " + url);

                        // Set request status
                        if (data) {
                            data.status = status;
                        }

                        if (status == 0) {
                            if (data == "") {
                                data = {};
                                data['status'] = 0;
                                data['non_field_errors'] = ["Could not connect. Please try again."];
                            }
                            // or if the data is null, then there was a timeout.
                            if (data == null) {
                                // Inject a non field error alerting the user
                                // that there's been a timeout error.
                                data = {};
                                data['status'] = 0;
                                data['non_field_errors'] = ["Server timed out. Please try again."];
                            }
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
            'getMenuCategories': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getMenuCategories/",
                    'data': data
                });
            },
            'getPrinters': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getPrinters/",
                    'data': data
                });
            },
            'addMenuItem': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addMenuItem/",
                    'data': data
                });
            },
            'deleteMenuItem': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteMenuItem/",
                    'data': data
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
            'addBoardgame': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addBoardgame/",
                    'data': data
                });
            },
            'getBoardgames': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getBoardgames/",
                    'data': data
                });
            },
            'searchBoardgame': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchBoardgame/",
                    'data': data
                });
            },
            'getBoardgame': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getBoardgame/",
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
            'addStock': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addStock/",
                    'data': data
                });
            },
            'getStocks': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getStocks/",
                    'data': data
                });
            },
            'searchStock': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchStock/",
                    'data': data
                });
            },
            'getStock': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getStock/",
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
            'getBranch': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getBranch/",
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
            'getSupplier': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getSupplier/",
                    'data': data
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
                    'method': "POST",
                    'url': "/api/getTodayStatus/",
                    'data': data
                });
            },
            'timeCalc': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/timeCalc/",
                    'data': data
                });
            },
            'addExpenseCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/addExpenseCategory/",
                    'data': data
                });
            },
            'getAllExpenseCategories': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getAllExpenseCategories/",
                    'data': data
                });
            },
            'searchExpenseCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/searchExpenseCategory/",
                    'data': data
                });
            },
            'getExpenseCategory': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/getExpenseCategory/",
                    'data': data
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
            'deleteInvoicePurchase': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteInvoicePurchase/",
                    'data': data
                });
            },
            'deleteInvoiceExpense': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteInvoiceExpense/",
                    'data': data
                });
            },
            'deleteInvoiceReturn': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteInvoiceReturn/",
                    'data': data
                });
            },
            'deleteInvoiceSettlement': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "/api/deleteInvoiceSettlement/",
                    'data': data
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
            }



        };
        return service;

    });