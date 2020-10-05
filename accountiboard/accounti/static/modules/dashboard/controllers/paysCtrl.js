angular.module("dashboard")
    .controller("paysCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.set_today_for_invoice();
            $scope.new_pay_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'payment_amount': 0,
                'backup_code': '',
                'settle_type': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': '',
                'description': ''
            };
            $scope.search_data_pay = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.headers = [
                {
                    name: "شماره پرداختی",
                    key: "factor_number"
                },
                {
                    name: "طرف حساب",
                    key: "supplier_name"
                },
                {
                    name: "میزان پرداختی",
                    key: "payment_amount"
                },
                {
                    name: "نوع پرداخت",
                    key: "settle_type"
                },
                {
                    name: "شماره ارجاع",
                    key: "backup_code"
                },
                {
                    name: "بانکداری",
                    key: "banking"
                },
                {
                    name: "تاریخ",
                    key: "created_time"
                }
            ];
            $scope.table_config = {
                price_fields: ["payment_amount"],
                has_detail_button: false,
                has_delete_button: true,
                has_row_numbers: false
            };
            $scope.get_pays();
            $scope.get_suppliers();
            $scope.get_banking_data();
            $scope.get_stocks_data();

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

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_pay_data.factor_number = data['next_factor_number'];
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

        $scope.addPay = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_pay_data.date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addPay($scope.new_pay_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_pays();
                        $scope.resetFrom();
                        $rootScope.close_modal('addModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.searchPay = function () {
            if ($scope.search_data_pay.search_word === '') {
                $scope.get_pays();
            }
            else {
                dashboardHttpRequest.searchPay($scope.search_data_pay)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.pays = data['pays'];
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {
                        $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                    });
            }
        };

        $scope.get_pays = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getAllPays(data)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.pays = data['invoices']
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.delete_invoice_pay = function (invoice_id) {
            dashboardHttpRequest.deleteInvoiceSettlement(invoice_id)
                .then(function (data) {
                    $scope.get_pays();
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
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
            $scope.addPay();
            $timeout(function () {
                $scope.set_today_for_invoice();
                $scope.open_modal('addModal');
                $scope.getNextFactorNumber('PAY');
            }, 1000);
        };

        $scope.resetFrom = function () {
            $scope.new_pay_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': '',
                'payment_amount': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': '',
                'description': ''
            };
        };
        initialize();
    });