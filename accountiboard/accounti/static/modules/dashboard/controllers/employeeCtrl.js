angular.module("dashboard")
    .controller("employeeCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_employee_data = {
                'employee_id': 0,
                'first_name': '',
                'last_name': '',
                'father_name': '',
                'national_code': '',
                'phone': '',
                'password': '',
                're_password': '',
                'home_address': '',
                'bank_name': '',
                'bank_card_number': '',
                'shaba': '',
                'position': '',
                'membership_card_number': '',
                'base_worksheet_salary': '',
                'base_worksheet_count': '',
                'auth_level': '4',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.serach_data_employee = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.employeeSearchWord = '';
            $scope.get_employees_data($rootScope.user_data);
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

        $scope.openAddEmployeeModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addUserModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddEmployeeModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addUserModal').modal('hide');
            })(jQuery);
        };

        $scope.registerEmployee = function () {
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.registerEmployee($scope.new_employee_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_employees_data($rootScope.user_data);
                            $scope.closeAddEmployeeModal();
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
                dashboardHttpRequest.registerEmployee($scope.new_employee_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_employees_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddEmployeeModal();
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

        $scope.searchEmployee = function () {
            if ($scope.serach_data_employee.search_word === '') {
                $scope.get_employees_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchEmployee($scope.serach_data_employee)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.employees = data['employees'];
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

        $scope.getEmployee = function (employee_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'employee_id': employee_id
            };
            dashboardHttpRequest.getEmployee(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['employee'];
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


        $scope.editEmployee = function (employee_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
                'employee_id': employee_id
            };
            dashboardHttpRequest.getEmployee(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_employee_data = {
                            'employee_id': employee_id,
                            'first_name': data['employee']['first_name'],
                            'last_name': data['employee']['last_name'],
                            'father_name': data['employee']['father_name'],
                            'national_code': data['employee']['national_code'],
                            'phone': data['employee']['phone'],
                            'password': '',
                            're_password': '',
                            'home_address': data['employee']['home_address'],
                            'bank_name': data['employee']['bank_name'],
                            'bank_card_number': data['employee']['bank_card_number'],
                            'shaba': data['employee']['shaba'],
                            'position': data['employee']['position'],
                            'membership_card_number': data['employee']['membership_card_number'],
                            'base_worksheet_salary': data['employee']['base_worksheet_salary'],
                            'base_worksheet_count': data['employee']['base_worksheet_count'],
                            'auth_level': data['employee']['auth_level'],
                            'branch_id': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openAddEmployeeModal();
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
                $('#addUserModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addUserModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_employee_data = {
                'employee_id': 0,
                'first_name': '',
                'last_name': '',
                'father_name': '',
                'national_code': '',
                'phone': '',
                'password': '',
                're_password': '',
                'home_address': '',
                'bank_name': '',
                'bank_card_number': '',
                'shaba': '',
                'position': '',
                'membership_card_number': '',
                'base_worksheet_salary': '',
                'base_worksheet_count': '',
                'auth_level': '4',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddEmployeeModal();
        };
        initialize();
    });