angular.module("dashboard")
    .controller("expenseCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker").datepicker();
                });
            })(jQuery);
            $scope.error_message = '';
            $scope.new_invoice_expense_data = {
                'id': 0,
                'expense_id': 0,
                'expense_cat_id': 0,
                'supplier_id': 0,
                'services': [
                    {
                        'service_name': '',
                        'price': 0,
                        'description': ''
                    }
                ],
                'total_price': 0,
                'settlement_type': 'CASH',
                'tax': 0,
                'discount': 0,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_expense = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.get_expenses();
            $scope.get_suppliers();
            $scope.get_expense_cats_data($rootScope.user_data);
        };

        $scope.get_expense_cats_data = function (data) {
            dashboardHttpRequest.getAllExpenseCategories(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.expense_cats = data['all_expense_categories'];
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
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getSuppliers(data)
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
            $scope.resetFrom();
        };

        $scope.addExpense = function () {
            $scope.new_invoice_expense_data.date = $("#datepicker").val();
            for(var i in $scope.new_invoice_expense_data.services) {
                $scope.new_invoice_expense_data.total_price += Number($scope.new_invoice_expense_data.services[i].price);
            }
            dashboardHttpRequest.addExpense($scope.new_invoice_expense_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_expenses();
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

        $scope.delete_invoice_expense = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.deleteInvoiceExpense(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_expenses();
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

        $scope.searchExpense = function () {
            if ($scope.search_data_expense.search_word === '') {
                $scope.get_expenses();
            }
            else {
                dashboardHttpRequest.searchExpense($scope.search_data_expense)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.expenses = data['expenses'];
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

        $scope.get_expenses = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getAllExpenses(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.expenses = data['invoices'];
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

        $scope.deleteNewItem = function (item_index) {
            $scope.new_invoice_expense_data.services.splice(item_index, 1);
        };

        $scope.resetFrom = function () {
            $scope.new_invoice_expense_data = {
                'id': 0,
                'expense_id': 0,
                'expense_cat_id': 0,
                'service_name': '',
                'description': '',
                'total_price': 0,
                'settlement_type': 'CASH',
                'tax': 0,
                'services': [
                    {
                        'service_name': '',
                        'price': 0,
                        'description': ''
                    }
                ],
                'discount': 0,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.change_total_price = function () {
            $scope.new_invoice_expense_data.total_price = 0;
            for (var i = 0; i < $scope.new_invoice_expense_data.services.length; i++){
                $scope.new_invoice_expense_data.total_price += Number($scope.new_invoice_expense_data.services[i].price);
            }
        };

        $scope.add_new_row_to_services = function () {
            $scope.new_invoice_expense_data.services.push({
                'service_name': '',
                'price': 0,
                'description': ''
            });
        };

        initialize();
    });