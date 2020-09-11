angular.module("dashboard")
    .controller("returnCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $scope.error_message = '';
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
                'username': $rootScope.user_data.username,
                'banking_id':'',
                'stock_id':''
            };
            $scope.search_data_return = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.get_returns();
            $scope.get_suppliers();
            $scope.get_shop_products();
            $scope.get_banking_data();
            $scope.get_stocks_data();
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
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.openAddModal = function () {
            $scope.set_today_for_invoice();
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
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
                        $scope.closeAddModal();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
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
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
        };

        $scope.get_returns = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getAllReturns(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.returns = data['invoices'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.openPermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closePermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_return_data.factor_number = data['next_factor_number'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBankingByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.allbanking_names = [];
                    data['bank'].forEach(function (bank) {
                        $scope.allbanking_names.push({'id':bank.id, 'name':bank.name});
                    });

                    data['tankhah'].forEach(function (tankhah) {
                        $scope.allbanking_names.push({'id':tankhah.id, 'name':tankhah.name});
                    });

                    data['cash_register'].forEach(function (cash_register) {
                        $scope.allbanking_names.push({'id':cash_register.id, 'name':cash_register.name});
                    });

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.get_stocks_data = function () {
            dashboardHttpRequest.getStockByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    angular.copy($rootScope.user_data.branches, $scope.branches);
                    $scope.stocks = data['stocks'];

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.save_and_open_modal = function () {
            $scope.addReturn();
            $timeout(function () {
                $scope.openAddModal();
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
                'username': $rootScope.user_data.username,
                'banking_id':'',
                'stock_id':''
            };
            $scope.getNextFactorNumber('RETURN');
        };
        initialize();
    });