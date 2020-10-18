angular.module("dashboard")
    .controller("salaryCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.set_today_for_invoice();
            $scope.edit_mode = false;
            $scope.search_word = '';
            $scope.new_salary_data = {
                'id': 0,
                'factor_number': 0,
                'employee_id': 0,
                'base_salary': 0,
                'over_time_pay': 0,
                'benefits': 0,
                'bonuses': 0,
                'reduction': 0,
                'insurance': 0,
                'tax': 0,
                'total_price': 0,
                'backup_code': '',
                'settle_type': '',
                'bonuses_description': '',
                'benefits_description': '',
                'over_time_pay_description': '',
                'reduction_description': '',
                'description': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': ''

            };
            $scope.get_banking_data();
            $scope.get_employees_data();
            $scope.getInvoiceSalaries();
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker").datepicker();
                });
            })(jQuery);
            $scope.headers = [
                {
                    name: "شماره سند",
                    key: "factor_number",
                    is_number: true
                },
                {
                    name: "تاریخ",
                    key: "invoice_date",
                    is_number: true
                },
                {
                    name: "طرف حساب",
                    key: "employee_name"
                },
                {
                    name: "نوع پرداخت",
                    key: "settle_type"
                },
                {
                    name: "بانکداری",
                    key: "banking"
                },
                {
                    name: "مبلغ",
                    key: "total_price"
                }
            ];
            $scope.table_config = {
                price_fields: ["total_price"],
                has_detail_button: true,
                has_delete_button: true,
                has_row_numbers: false
            };
        };

        $scope.get_employee_name_from_id = function () {
            for (var index = 0; index < $scope.employees.length; index++) {
                if ($scope.employees[index].id === $scope.new_salary_data.employee_id) {
                    $scope.selected_employee_name = $scope.employees[index].full_name;
                    break;
                }
            }
        };

        $scope.compare_before_exit = function () {
            return angular.toJson($scope.first_initial_value_of_invoice_salary) === angular.toJson($scope.new_salary_data);
        };

        $scope.change_total_price = function () {
            $scope.new_salary_data.total_price = Number($scope.new_salary_data.base_salary) + Number($scope.new_salary_data.over_time_pay) + Number($scope.new_salary_data.benefits) + Number($scope.new_salary_data.bonuses) - Number($scope.new_salary_data.reduction) - Number($scope.new_salary_data.insurance) - Number($scope.new_salary_data.tax);
        };

        $scope.get_employees_data = function () {
            dashboardHttpRequest.getBranchEmployees($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    $scope.employees = data['employees'];
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
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

        $scope.save_and_open_modal = function () {
            $scope.addSalary();
            $timeout(function () {
                $scope.set_today_for_invoice();
                $scope.open_modal('addModal');
                $scope.getNextFactorNumber('SALARY');
            }, 1000);
        };

        $scope.resetFrom = function () {
            $scope.new_salary_data = {
                'id': 0,
                'factor_number': 0,
                'employee_id': 0,
                'base_salary': 0,
                'over_time_pay': 0,
                'benefits': 0,
                'bonuses': 0,
                'reduction': 0,
                'insurance': 0,
                'tax': 0,
                'total_price': 0,
                'backup_code': '',
                'settle_type': '',
                'bonuses_description': '',
                'benefits_description': '',
                'over_time_pay_description': '',
                'reduction_description': '',
                'description': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': ''
            };
            $scope.selected_employee_name = "";
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
                    $rootScope.show_toast(error.data.error_msg, 'danger');
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
                        $scope.new_salary_data.factor_number = data['next_factor_number'];
                        $scope.first_initial_value_of_invoice_salary = angular.copy($scope.new_salary_data);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };


        $scope.addSalary = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_salary_data.invoice_date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addInvoiceSalary($scope.new_salary_data, '0')
                .then(function (data) {
                    $scope.getInvoiceSalaries();
                    $scope.resetFrom();
                    $scope.close_modal('addModal');
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.getInvoiceSalaries = function () {
            dashboardHttpRequest.getSalaries($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    $scope.salaries = data['invoices'];
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.delete_invoice_salary = function (invoice_id) {
            dashboardHttpRequest.deleteInvoiceSalary(invoice_id)
                .then(function (data) {
                    $scope.getInvoiceSalaries();
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.showInvoiceSalary = function (invoice_id) {
            dashboardHttpRequest.getInvoiceSalary(invoice_id)
                .then(function (data) {
                    $scope.new_salary_data = {
                        'id': data['invoice']['id'],
                        'factor_number': data['invoice']['factor_number'],
                        'employee_id': data['invoice']['employee_id'],
                        'settle_type': data['invoice']['settle_type'],
                        'branch_id': $rootScope.user_data.branch,
                        'banking_id': data['invoice']['banking']['id'],
                        'backup_code': data['invoice']['backup_code'],
                        'invoice_date': data['invoice']['invoice_date'],

                        'base_salary': data['invoice']['base_salary'],
                        'over_time_pay': data['invoice']['over_time_pay'],
                        'benefits': data['invoice']['benefits'],
                        'bonuses': data['invoice']['bonuses'],
                        'reduction': data['invoice']['reduction'],
                        'insurance': data['invoice']['insurance'],
                        'tax': data['invoice']['tax'],
                        'total_price': data['invoice']['total_price'],

                        'bonuses_description': data['invoice']['bonuses_description'],
                        'benefits_description': data['invoice']['benefits_description'],
                        'over_time_pay_description': data['invoice']['over_time_pay_description'],
                        'reduction_description': data['invoice']['reduction_description'],
                        'description': data['invoice']['description'],
                    };
                    $scope.first_initial_value_of_invoice_salary = angular.copy($scope.new_salary_data);
                    $scope.edit_mode = true;
                    $scope.open_modal('addModal');
                    $scope.get_employee_name_from_id();
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.editSalary = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_salary_data.invoice_date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.editInvoiceSalary($scope.new_salary_data, $scope.new_salary_data.id)
                .then(function (data) {
                    $scope.getInvoiceSalaries();
                    $scope.resetFrom();
                    $scope.edit_mode = false;
                    $scope.close_modal('addModal');
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.searchSalary = function () {
            if ($scope.search_word === '') {
                $scope.getInvoiceSalaries();
            }
            else {
                dashboardHttpRequest.searchSalary($scope.search_word, $rootScope.user_data.branch)
                    .then(function (data) {
                        $rootScope.is_sub_page_loading = false;
                        $scope.salaries = data['invoices'];

                    }, function (error) {
                        $rootScope.show_toast(error.data.error_msg, 'danger');
                    });
            }
        };

        initialize();


    });