angular.module("dashboard")
    .controller("returnCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.new_invoice_return_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'return_products': [],
                'date': '',
                'return_type': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': ''
            };
            $scope.search_data_return = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch,
            };
            $scope.search_data_shop_products = {
                'search_word': ''
            };
            $scope.headers = [
                {
                    name: "شماره فاکتور",
                    key: "factor_number"
                },
                {
                    name: "طرف حساب",
                    key: "supplier_name"
                },
                {
                    name: "نام محصول",
                    key: "shop_name"
                },
                {
                    name: "تعداد",
                    key: "numbers"
                },
                {
                    name: "قیمت کل",
                    key: "total_price"
                },
                {
                    name: "توضیحات",
                    key: "description"
                },
                {
                    name: "تاریخ",
                    key: "date"
                }
            ];
            $scope.table_config = {
                price_fields: ["total_price"],
                has_detail_button: false,
                has_delete_button: false,
                has_row_numbers: false
            };
            $scope.get_returns();
            $scope.get_suppliers();
            $scope.get_shop_products();
            $scope.get_banking_data();
            $scope.get_stocks_data();
        };

        $scope.add_item_shop = function (shop_product_id, shop_product_name) {
            var is_added = false;
            $scope.new_invoice_return_data.return_products.forEach(function (item) {
                if (item.shop_id === shop_product_id) {
                    is_added = true;
                    item.numbers += 1;
                }
            });
            if (!is_added) {
                $scope.new_invoice_return_data.return_products.push({
                    shop_id: shop_product_id,
                    shop_name: shop_product_name,
                    numbers: 1,
                    buy_price: 0,
                    description: ''
                });
            }
        };

        $scope.compare_before_exit = function () {
            return angular.toJson($scope.first_initial_value_of_invoice_return) === angular.toJson($scope.new_invoice_return_data);
        };

        $scope.delete_product_row = function (product_index) {
            $scope.new_invoice_return_data.return_products.splice(product_index, 1);
        };

        $scope.set_today_for_invoice = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    var date = new Date();
                    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                    $("#datepicker").datepicker();
                    $('#datepicker').datepicker('setDate', today);
                });
            })(jQuery);
        };

        $scope.search_shop_products = function () {
            $scope.shops = $filter('filter')($scope.shop_products_original, {'name': $scope.search_data_shop_products.search_word});
        };

        $scope.add_new_row_to_return_products = function () {
            $scope.new_invoice_return_data.return_products.push({
                'shop_id': '',
                'numbers': 0,
                'buy_price': 0,
                'description': ''
            });
        };

        $scope.get_shop_products = function () {
            dashboardHttpRequest.getShopProducts($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.shops = data['shop_products'];
                        $scope.shop_products_original = data['shop_products'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.addReturn = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_invoice_return_data.date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addReturn($scope.new_invoice_return_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_returns();
                        $scope.resetFrom();
                        $scope.close_modal('addModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.searchReturn = function () {
            if ($scope.search_data_return.search_word === '') {
                $scope.get_returns();
            }
            else {
                dashboardHttpRequest.searchReturn($scope.search_data_return)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.returns = data['returns'];
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {
                        $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                    });
            }
        };

        $scope.get_returns = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getAllReturns(data)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.returns = data['invoices'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_return_data.factor_number = data['next_factor_number'];
                        $scope.first_initial_value_of_invoice_return = angular.copy($scope.new_invoice_return_data);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBankingByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    $scope.allbanking_names = [];
                    data['bank'].forEach(function (bank) {
                        $scope.allbanking_names.push({'id': bank.id, 'name': bank.name});
                    });

                    data['tankhah'].forEach(function (tankhah) {
                        $scope.allbanking_names.push({'id': tankhah.id, 'name': tankhah.name});
                    });

                    data['cash_register'].forEach(function (cash_register) {
                        $scope.allbanking_names.push({'id': cash_register.id, 'name': cash_register.name});
                    });

                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_stocks_data = function () {
            dashboardHttpRequest.getStockByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    angular.copy($rootScope.user_data.branches, $scope.branches);
                    $scope.stocks = data['stocks'];

                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.save_and_open_modal = function () {
            $scope.addReturn();
            $timeout(function () {
                $scope.set_today_for_invoice();
                $scope.open_modal('addModal');
                $scope.getNextFactorNumber('RETURN');
            }, 1000);
        };

        $scope.set_date = function (date_picker_id, date) {
            jQuery.noConflict();
            (function ($) {
                $('#' + date_picker_id).datepicker('setDate', date);
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.set_date("datepicker", "");
            $scope.new_invoice_return_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'return_products': [
                    {
                        'shop_id': '',
                        'numbers': 0,
                        'buy_price': 0,
                        'description': ''
                    }
                ],
                'date': '',
                'return_type': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': ''
            };
            $scope.getNextFactorNumber('RETURN');
        };
        initialize();
    });