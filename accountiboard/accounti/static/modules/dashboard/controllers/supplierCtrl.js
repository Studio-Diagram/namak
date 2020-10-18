angular.module("dashboard")
    .controller("supplierCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, $state, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.all_sum_invoices_supplier = [
                {
                    id: "PURCHASE",
                    name: "خرید",
                    numbers: 0,
                    total_price: 0
                },
                {
                    id: "PAY",
                    name: "پرداخت",
                    numbers: 0,
                    total_price: 0
                },
                {
                    id: "EXPENSE",
                    name: "هزینه",
                    numbers: 0,
                    total_price: 0
                },
                {
                    id: "RETURN",
                    name: "مرجوعی",
                    numbers: 0,
                    total_price: 0
                },
                {
                    id: "AMANI_SALE",
                    name: "فروش فروشگاهی",
                    numbers: 0,
                    total_price: 0
                }
            ];
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker").datepicker();
                    $("#datepicker1").datepicker();
                    $("#datepicker_remainder").datepicker();
                });

            })(jQuery);
            $scope.headers = [
                {
                    name: "عنوان",
                    key: "name"
                },
                {
                    name: "تعداد",
                    key: "numbers",
                    is_number: true
                },
                {
                    name: "ملبغ",
                    key: "total_price"
                }
            ];
            $scope.table_configs = {
                price_fields: ["total_price"],
                has_detail_button: true,
                has_row_numbers: false,
                price_with_tags: true
            };
            $scope.supplier_id = $stateParams.supplier;
            $rootScope.search_data_supplier = {
                'from_time': '',
                'to_time': ''
            };
            $scope.search_data_supplier_remainder = {
                'supplier_id': $stateParams.supplier,
                'to_time': ''
            };
            $scope.get_supplier();
            $scope.get_sum_all_invoices();
        };

        $scope.get_sum_all_invoices = function () {
            $scope.get_sum_invoice_purchases();
            $scope.get_sum_invoice_settlements();
            $scope.get_sum_invoice_expenses();
            $scope.get_sum_invoice_returns();
            $scope.get_sum_invoice_amani_sales();
        };

        $scope.go_to_detail_of_invoice = function (invoice_type) {
            $state.go('dashboard.accounting.detail', {supplier: $scope.supplier_id, detailState: invoice_type});
        };

        $scope.get_remainder = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.search_data_supplier_remainder.to_time = $("#datepicker_remainder").val();
            })(jQuery);
            dashboardHttpRequest.getSupplierRemainder($scope.search_data_supplier_remainder)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.remainder = data['supplier_remainder'];
                    }
                    else if (data['response_code'] === 3) $rootScope.show_toast(data.error_msg, 'danger');
                }, function (error) {
                });
        };

        $scope.filter_data = function () {
            jQuery.noConflict();
            (function ($) {
                $rootScope.search_data_supplier.to_time = $("#datepicker").val();
                $rootScope.search_data_supplier.from_time = $("#datepicker1").val();
            })(jQuery);
            $scope.get_sum_all_invoices();
        };

        $scope.get_supplier = function () {
            dashboardHttpRequest.getSupplier($scope.supplier_id)
                .then(function (data) {
                    $scope.supplier_name = data['supplier']['name'];
                    $scope.remainder = data['supplier']['remainder'];
                }, function (error) {
                });
        };

        $scope.get_sum_invoice_purchases = function () {
            var data = {
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInPurchase(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.all_sum_invoices_supplier[0].numbers = data['purchase_count'];
                        $scope.all_sum_invoices_supplier[0].total_price = data['all_invoice_purchases_sum']['total_price__sum'];
                    }
                    else if (data['response_code'] === 3) $rootScope.show_toast(data.error_msg, 'danger');
                }, function (error) {
                });
        };

        $scope.get_sum_invoice_settlements = function () {
            var data = {
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInSettlement(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.all_sum_invoices_supplier[1].numbers = data['pay_count'];
                        $scope.all_sum_invoices_supplier[1].total_price = data['all_invoice_settlements_sum']['payment_amount__sum'];
                    }
                    else if (data['response_code'] === 3) $rootScope.show_toast(data.error_msg, 'danger');
                }, function (error) {
                });
        };

        $scope.get_sum_invoice_expenses = function () {
            var data = {
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInExpense(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.all_sum_invoices_supplier[2].numbers = data['expense_count'];
                        $scope.all_sum_invoices_supplier[2].total_price = data['all_invoice_expenses_sum']['price__sum'];
                    }
                    else if (data['response_code'] === 3) $rootScope.show_toast(data.error_msg, 'danger');
                }, function (error) {
                });
        };

        $scope.get_sum_invoice_returns = function () {
            var data = {
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInReturn(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.all_sum_invoices_supplier[3].numbers = data['return_count'];
                        $scope.all_sum_invoices_supplier[3].total_price = data['all_invoice_returns_sum']['total_price__sum'];
                    }
                    else if (data['response_code'] === 3) $rootScope.show_toast(data.error_msg, 'danger');
                }, function (error) {
                });
        };

        $scope.get_sum_invoice_amani_sales = function () {
            var data = {
                'branch': $rootScope.user_data.branch,
                'from_time': $rootScope.search_data_supplier.from_time,
                'to_time': $rootScope.search_data_supplier.to_time,
                'supplier_id': $scope.supplier_id
            };
            dashboardHttpRequest.getSumInAmaniSales(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.all_sum_invoices_supplier[4].numbers = data['all_amani_sales_buy'];
                        $scope.all_sum_invoices_supplier[4].total_price = data['all_amani_sales_sum'];
                    }
                    else if (data['response_code'] === 3) $rootScope.show_toast(data.error_msg, 'danger');
                }, function (error) {
                    $rootScope.is_page_loading = false;
                });
        };

        initialize();
    });