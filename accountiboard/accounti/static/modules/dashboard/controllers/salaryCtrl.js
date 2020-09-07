angular.module("dashboard")
    .controller("salaryCtrl", function( $scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state){
        var initialize = function () {
            $scope.set_today_for_invoice();
            $scope.error_message = '';
            $scope.new_salary_data = {
                'id': 0,
                'factor_number': 0,
                'employee_id': 0,
                'base_salary': 0,
                'over_time_pay':0,
                'benefits':0,
                'bonuses':0,
                'reduction':0,
                'insurance':0,
                'tax':0,
                'total_price':0,
                'backup_code': '',
                'settle_type': '',
                'bonuses_description':'',
                'reduction_description':'',
                'description':'',
                'branch_id': $rootScope.user_data.branch,                
                'banking_id':'',
                
            };


            $scope.get_banking_data();
            $scope.get_employees_data($rootScope.user_data);

        };
        $scope.change_total_price = function () {
            $scope.new_salary_data.total_price = 0;
            $scope.new_salary_data.total_price = Number($scope.new_salary_data.base_salary) + Number($scope.new_salary_data.over_time_pay) + Number($scope.new_salary_data.benefits) + Number($scope.new_salary_data.bonuses) - Number($scope.new_salary_data.reduction) - Number($scope.new_salary_data.insurance) - Number($scope.new_salary_data.tax);
        };
        $scope.get_employees_data = function (data) {
            dashboardHttpRequest.getEmployees(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.employees = data['employees'];
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
                $scope.openAddModal();
                $scope.getNextFactorNumber('SALARY');
            }, 1000);
        };

        $scope.resetFrom = function () {
            $scope.new_salary_data = {
                'id': 0,
                'factor_number': 0,
                'employee_id': 0,
                'base_salary': 0,
                'over_time_pay':0,
                'benefits':0,
                'bonuses':0,
                'reduction':0,
                'insurance':0,
                'tax':0,
                'total_price':0,
                'backup_code': '',
                'settle_type': '',
                'bonuses_description':'',
                'reduction_description':'',
                'description':'',
                'branch_id': $rootScope.user_data.branch,                
                'banking_id':'',
            };
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

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_salary_data.factor_number = data['next_factor_number'];
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


        $scope.addSalary = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_salary_data.invoice_date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addSalary($scope.new_salary_data)
                .then(function (data) {
                    if (status === 200) {

                        $scope.resetFrom();
                        $scope.close_modal(addModal);
                    }
                    else if (status === 400) {
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


        initialize();



    });