angular.module("dashboard")
    .controller("supplierDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.supplier_id = $stateParams.supplier;
            $scope.is_return = false;
            $scope.detailState = $stateParams.detailState;
            if ($rootScope.search_data_supplier === undefined) {
                $scope.search_data_supplier = {
                    'from_time': '',
                    'to_time': '',
                    'username': $rootScope.user_data.username,
                    'branch': $rootScope.user_data.branch
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
            if ($scope.detailState === "PURCHASE") {
                $scope.state_word = 'خرید';
                $scope.get_detail_invoice_purchases();
            }
            else if ($scope.detailState === "PAY") {
                $scope.state_word = 'پرداختی';
                $scope.get_detail_invoice_settlements();
            }
            else if ($scope.detailState === "EXPENSE") {
                $scope.state_word = 'هزینه';
                $scope.get_detail_invoice_expenses();
            }
            else if ($scope.detailState === "RETURN") {
                $scope.state_word = 'مرجوعی';
                $scope.is_return = true;
                $scope.get_detail_invoice_returns();
            }
            else if ($scope.detailState === "AMANI_SALE") {
                $scope.state_word = 'فروش فروشگاهی';
                $scope.get_detail_invoice_amani_sales();
            }
        };

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
        };

        $scope.showInvoicePurchase = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id
            };
            dashboardHttpRequest.getInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.invoice_purchase_data = data['invoice'];
                        $rootScope.open_modal('show_invoice_purchase');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });
        };

        $scope.show_invoice_detail = function (invoice_id) {
            if ($scope.detailState === "PURCHASE"){
                $scope.showInvoicePurchase(invoice_id);
            }
        };

        $scope.get_supplier = function () {
            dashboardHttpRequest.getSupplier($scope.supplier_id)
                .then(function (data) {
                    $scope.supplier_name = data['supplier']['name'];
                }, function (error) {});
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
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {});
            }
        };

        $scope.get_detail_invoice_purchases = function () {
            var data = {
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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                });
        };

        $scope.get_detail_invoice_settlements = function () {
            var data = {
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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

                });
        };

        $scope.get_detail_invoice_expenses = function () {
            var data = {
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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

                });
        };

        initialize();
    });