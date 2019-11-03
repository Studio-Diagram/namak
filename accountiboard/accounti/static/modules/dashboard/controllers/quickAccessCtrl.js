angular.module("dashboard")
    .controller("quickAccessCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker_pay").datepicker();
                    $("#datepicker_expense").datepicker();
                });
            })(jQuery);
            $scope.members = [];
            $scope.tags = [];
            $scope.new_member_data = {
                'member_id': 0,
                'first_name': '',
                'last_name': '',
                'card_number': '',
                'year_of_birth': '',
                'month_of_birth': '',
                'day_of_birth': '',
                'phone': '',
                'intro': 'other',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_invoice_expense_data = {
                'id': 0,
                'factor_number': 0,
                'expense_id': 0,
                'expense_kind': '',
                'expense_tags': [],
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
            $scope.new_pay_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'payment_amount': 0,
                'backup_code': '',
                'settle_type': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.serach_data_member = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.get_all_expense_tags();
            $scope.get_suppliers();
        };

        $scope.addMember = function () {
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addMember($scope.new_member_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_members_data($rootScope.user_data);
                            $scope.close_modal('addMemberModal');
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
            else {
                dashboardHttpRequest.addMember($scope.new_member_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_members_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.close_modal('addMemberModal');
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

        $scope.addPay = function () {
            $scope.new_pay_data.date = $("#datepicker_pay").val();
            dashboardHttpRequest.addPay($scope.new_pay_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.resetFrom();
                        $scope.close_modal('addPayModal');
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

        $scope.change_total_price = function () {
            $scope.new_invoice_expense_data.total_price = 0;
            for (var i = 0; i < $scope.new_invoice_expense_data.services.length; i++) {
                $scope.new_invoice_expense_data.total_price += Number($scope.new_invoice_expense_data.services[i].price);
            }

            $scope.new_invoice_expense_data.total_price = Number($scope.new_invoice_expense_data.total_price) + Number($scope.new_invoice_expense_data.tax) - Number($scope.new_invoice_expense_data.discount);
        };

        $scope.add_new_row_to_services = function () {
            $scope.new_invoice_expense_data.services.push({
                'service_name': '',
                'price': 0,
                'description': ''
            });
        };

        $scope.deleteNewItem = function (item_index) {
            $scope.new_invoice_expense_data.services.splice(item_index, 1);
        };

        $scope.addExpense = function () {
            $scope.new_invoice_expense_data.expense_tags = $scope.tags;
            $scope.new_invoice_expense_data.date = $("#datepicker_expense").val();
            dashboardHttpRequest.addExpense($scope.new_invoice_expense_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_expense_tags();
                        $scope.resetFrom();
                        $scope.close_modal('addExpenseModal');
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

        $scope.loadTags = function ($query) {
            return $scope.expense_tags.filter(function (tag) {
                return tag.name.toLowerCase().indexOf($query.toLowerCase()) !== -1;
            });
        };

        $scope.get_all_expense_tags = function () {
            var sending_data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getAllExpenseTags(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.expense_tags = data['tags'];
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

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_pay_data.factor_number = data['next_factor_number'];
                        $scope.new_invoice_expense_data.factor_number = data['next_factor_number'];
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

        $scope.searchMember = function () {
            if ($scope.serach_data_member.search_word === '') {
                $scope.get_members_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchMember($scope.serach_data_member)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.members = data['members'];
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

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModalQ').modal('show');
                $('#addMemberModal').css('z-index', 1000);
                $('#addPayModal').css('z-index', 1000);
                $('#addExpenseModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModalQ').modal('hide');
                $('#addMemberModal').css('z-index', "");
                $('#addPayModal').css('z-index', "");
                $('#addExpenseModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_member_data = {
                'member_id': 0,
                'first_name': '',
                'last_name': '',
                'card_number': '',
                'year_of_birth': '',
                'month_of_birth': '',
                'day_of_birth': '',
                'phone': '',
                'intro': 'other',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_pay_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'payment_amount': 0,
                'backup_code': '',
                'settle_type': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_invoice_expense_data = {
                'id': 0,
                'factor_number': 0,
                'expense_id': 0,
                'expense_kind': '',
                'expense_tags': [],
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
        };

        $scope.save_and_open_modal_pay = function () {
            $scope.addPay();
            $timeout(function () {
                $scope.open_modal('addPayModal');
                $scope.getNextFactorNumber('PAY');
            }, 1000);
        };

        $scope.save_and_open_modal_expense = function () {
            $scope.addExpense();
            $timeout(function () {
                $scope.open_modal('addExpenseModal');
                $scope.getNextFactorNumber('EXPENSE');
            }, 1000);
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.close_modal('addMemberModal');
        };

        initialize();
    });