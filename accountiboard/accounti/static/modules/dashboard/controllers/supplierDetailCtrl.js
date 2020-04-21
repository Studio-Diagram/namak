angular.module("dashboard")
    .controller("supplierDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.supplier_id = $stateParams.supplier;
            $scope.is_return = false;
            $scope.detailState = $stateParams.detailState;
            if ($rootScope.search_data_supplier === undefined) {
                $scope.search_data_supplier = {
                    'from_time': '',
                    'to_time': '',
                    'username': $rootScope.user_data.username
                };
            }
            else {
                $scope.search_data_supplier = {
                    'from_time': $rootScope.search_data_supplier.from_time,
                    'to_time': $rootScope.search_data_supplier.to_time,
                    'username': $rootScope.user_data.username
                };
            }
            $scope.get_supplier();
            if ($scope.detailState === "buy") {
                $scope.state_word = 'خرید';
                $scope.get_detail_invoice_purchases();
            }
            else if ($scope.detailState === "pay") {
                $scope.state_word = 'پرداختی';
                $scope.get_detail_invoice_settlements();
            }
            else if ($scope.detailState === "expense") {
                $scope.state_word = 'هزینه';
                $scope.get_detail_invoice_expenses();
            }
            else if ($scope.detailState === "return") {
                $scope.state_word = 'مرجوعی';
                $scope.is_return = true;
                $scope.get_detail_invoice_returns();
            }
            else if ($scope.detailState === "amani_sales") {
                $scope.state_word = 'فروش امانی';
                $scope.get_detail_invoice_amani_sales();
            }
        };

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
        };

        $scope.showInvoicePurchase = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.invoice_purchase_data = data['invoice'];
                        $rootScope.open_modal('show_invoice_purchase');
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

        $scope.show_invoice_detail = function (invoice_id) {
            if ($scope.detailState === "buy"){
                $scope.showInvoicePurchase(invoice_id);
            }
        };

        $scope.get_supplier = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSupplier(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.supplier_name = data['supplier']['name']
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
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

        $scope.searchSupplier = function () {
            if ($scope.search_data_supplier.search_word === '') {
                $scope.get_suppliers();
            }
            else {
                dashboardHttpRequest.searchSupplier($scope.search_data_supplier)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.suppliers = data['suppliers'];
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.error_message = 500;
                        $scope.openErrorModal();
                    });
            }
        };

        $scope.get_detail_invoice_purchases = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $scope.search_data_supplier.from_time,
                'to_time': $scope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getDetailInPurchase(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sum_invoices = data['all_invoice_purchases_sum'];
                        $scope.invoices_data = data['invoices_data'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_detail_invoice_settlements = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $scope.search_data_supplier.from_time,
                'to_time': $scope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getDetailInSettlement(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sum_invoices = data['all_invoice_settlements_sum'];
                        $scope.invoices_data = data['invoices_data'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_detail_invoice_expenses = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $scope.search_data_supplier.from_time,
                'to_time': $scope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getDetailInExpense(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sum_invoices = data['all_invoice_expenses_sum'];
                        $scope.invoices_data = data['invoices_data'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_detail_invoice_returns = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $scope.search_data_supplier.from_time,
                'to_time': $scope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getDetailInReturn(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sum_invoices = data['all_invoice_returns_sum'];
                        $scope.invoices_data = data['invoices_data'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_detail_invoice_amani_sales = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch,
                'from_time': $scope.search_data_supplier.from_time,
                'to_time': $scope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getDetailInAmaniSales(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sum_invoices = data['all_invoice_amani_sales_sum'];
                        $scope.invoices_data = data['invoices_data'];
                        $scope.amani_sale_products = data['amani_sale_base_on_product'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        initialize();
    });