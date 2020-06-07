angular.module("dashboard")
    .controller("employeeCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.serach_data_employee = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.employeeSearchWord = '';
            $scope.branches = [];
            $scope.get_branches_data();
            $scope.get_employees_data($rootScope.user_data);
            $scope.InitializeAndResetForm();
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

        $scope.get_branches_data = function () {
            dashboardHttpRequest.getBranches($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.branches = data['branches'];
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
                $scope.InitializeAndResetForm();
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
                            $scope.InitializeAndResetForm();
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
                            'membership_card_number': data['employee']['membership_card_number'],
                            'base_worksheet_salary': data['employee']['base_worksheet_salary'],
                            'base_worksheet_count': data['employee']['base_worksheet_count'],
                            'employee_branches': $scope.branches,
                            'auth_levels': $scope.auth_levels,
                            'branch_id': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        var employee_auth_levels = data['employee']['auth_levels'];
                        employee_auth_levels.forEach(function (employee_auth_level) {
                            $scope.new_employee_data.auth_levels.forEach(function (auth_level) {
                                if (employee_auth_level === auth_level.id) {
                                    auth_level.is_checked = 1;
                                    auth_level.is_checked_m = 1;
                                }
                            })
                        });
                        var employee_branches = data['employee']['branches'];
                        employee_branches.forEach(function (employee_branch_id) {
                            $scope.new_employee_data.employee_branches.forEach(function (branch) {
                                if (employee_branch_id === branch.id) {
                                    branch.is_checked = 1;
                                    branch.is_checked_m = 1;
                                }
                            })
                        });
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

        $scope.changeAuthCheckBox = function (auth_level_name) {
            $scope.new_employee_data.auth_levels.forEach(function (auth_level) {
                if (auth_level_name === auth_level.id) {
                    if (auth_level.is_checked === 1) {
                        auth_level.is_checked = 0;
                        auth_level.is_checked_m = 0;
                    }
                    else {
                        auth_level.is_checked = 1;
                        auth_level.is_checked_m = 1;
                    }
                }
            });
        };

        $scope.changeEmployeeBranchCheckBox = function (branch_name) {
            $scope.new_employee_data.employee_branches.forEach(function (branch) {
                if (branch_name === branch.id) {
                    if (branch.is_checked === 1) {
                        branch.is_checked = 0;
                        branch.is_checked_m = 0;
                    }
                    else {
                        branch.is_checked = 1;
                        branch.is_checked_m = 1;
                    }
                }
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

        $scope.clearEmployeeBranchesCheckboxes = function () {
            $scope.branches.forEach(function (branch) {
                branch.is_checked = 0;
                branch.is_checked_m = 0;
            });
        };

        $scope.showAuthName = function (employee_auth_level) {
            var auth_display;
            angular.forEach($scope.auth_levels, function (item, index) {
                if (employee_auth_level === item.id) {
                    auth_display = item.name;
                }
            }, $scope);
            return auth_display;
        };

        $scope.InitializeAndResetForm = function () {
            $scope.auth_levels = [
                {
                    id: "MANAGER",
                    name: "مدیر",
                    is_checked: 0,
                    is_checked_m: 0
                },
                {
                    id: "CASHIER",
                    name: "صندوق‌دار",
                    is_checked: 0,
                    is_checked_m: 0
                },
                {
                    id: "ACCOUNTANT",
                    name: "حساب‌دار",
                    is_checked: 0,
                    is_checked_m: 0
                },
                {
                    id: "STAFF",
                    name: "کارمند",
                    is_checked: 0,
                    is_checked_m: 0
                }
            ];
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
                'auth_levels': $scope.auth_levels,
                'employee_branches': $scope.branches,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.clearEmployeeBranchesCheckboxes();
        };
        initialize();
    });