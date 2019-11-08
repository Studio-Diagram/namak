angular.module("dashboard")
    .controller("supplierCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker").datepicker();
                    $("#datepicker1").datepicker();
                    $("#datepicker_remainder").datepicker();
                });

            })(jQuery);
            $scope.error_message = '';
            $scope.supplier_id = $stateParams.supplier;
            $rootScope.search_data_supplier = {
                'from_time': '',
                'to_time': '',
                'username': $rootScope.user_data.username
            };
            $scope.search_data_supplier_remainder = {
                'supplier_id': $stateParams.supplier,
                'to_time': '',
                'username': $rootScope.user_data.username
            };
            $scope.get_supplier();
            $scope.get_sum_invoice_purchases();
            $scope.get_sum_invoice_settlements();
            $scope.get_sum_invoice_expenses();
            $scope.get_sum_invoice_returns();
            $scope.get_sum_invoice_amani_sales();
        };

        $scope.get_remainder = function () {
            $scope.search_data_supplier_remainder.to_time = $("#datepicker_remainder").val();
            dashboardHttpRequest.getSupplierRemainder($scope.search_data_supplier_remainder)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.remainder = data['supplier_remainder'];
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

        $scope.filter_data = function () {
            $rootScope.search_data_supplier.to_time = $("#datepicker").val();
            $rootScope.search_data_supplier.from_time = $("#datepicker1").val();
            $scope.get_sum_invoice_purchases();
            $scope.get_sum_invoice_settlements();
            $scope.get_sum_invoice_expenses();
            $scope.get_sum_invoice_returns();
            $scope.get_sum_invoice_amani_sales();
        };
        $scope.get_supplier = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSupplier(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.supplier_name = data['supplier']['name'];
                        $scope.remainder = data['supplier']['remainder'];
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

        $scope.get_sum_invoice_purchases = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInPurchase(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.sum_purchase = data['all_invoice_purchases_sum']['total_price__sum'];
                        $scope.last_buy = data['last_buy'];
                        $scope.purchase_count = data['purchase_count'];
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

        $scope.get_sum_invoice_settlements = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInSettlement(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.sum_settlement = data['all_invoice_settlements_sum']['payment_amount__sum'];
                        $scope.last_pay = data['last_pay'];
                        $scope.pay_count = data['pay_count'];
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

        $scope.get_sum_invoice_expenses = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInExpense(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.sum_expense = data['all_invoice_expenses_sum']['price__sum'];
                        $scope.last_expense = data['last_expense'];
                        $scope.expense_count = data['expense_count'];
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

        $scope.get_sum_invoice_returns = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInReturn(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.sum_return = data['all_invoice_returns_sum']['total_price__sum'];
                        $scope.last_return = data['last_return'];
                        $scope.return_count = data['return_count'];
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

        $scope.get_sum_invoice_amani_sales = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInAmaniSales(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sum_amani_sales = data['all_amani_sales_sum'];
                        $scope.last_amani_sales = '-';
                        $scope.amani_sales_count = data['all_amani_sales_buy'];
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