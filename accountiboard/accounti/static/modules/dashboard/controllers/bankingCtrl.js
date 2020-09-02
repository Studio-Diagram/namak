angular.module("dashboard")
    .controller("bankingCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.new_banking_data = {
                'id': 0,
                'branches':[],
                'type':'',
                'name': '',
                'bank_name': '',
                'bank_account': '',
                'bank_card_number': '',
                'shaba_number': ''
            };
            $scope.get_banking_data();
            $scope.get_branches_data();
            angular.copy($rootScope.user_data.branches, $scope.new_banking_data.branches);
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBanking()
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    angular.copy($rootScope.user_data.branches, $scope.branches);
                    $scope.banks = data['bank'];
                    $scope.tankhahs = data['tankhah'];
                    $scope.cash_registers = data['cash_register'];
                    
                    for (var i = $scope.banks.length - 1; i >= 0; i--) {
                        $scope.banks[i].branches_names = [];
                        for (var j = $scope.banks[i].branches.length - 1; j >= 0; j--) {
                            for (var k = $rootScope.user_data.branches.length - 1; k >= 0; k--) {
                                if ($rootScope.user_data.branches[k].id == $scope.banks[i].branches[j]) {
                                    $scope.banks[i].branches_names.push($rootScope.user_data.branches[k].name);
                                }
                            }
                        }
                    }

                    for (var i = $scope.tankhahs.length - 1; i >= 0; i--) {
                        $scope.tankhahs[i].branches_names = [];
                        for (var j = $scope.tankhahs[i].branches.length - 1; j >= 0; j--) {
                            for (var k = $rootScope.user_data.branches.length - 1; k >= 0; k--) {
                                if ($rootScope.user_data.branches[k].id == $scope.tankhahs[i].branches[j]) {
                                    $scope.tankhahs[i].branches_names.push($rootScope.user_data.branches[k].name);
                                }
                            }
                        }
                    }

                    for (var i = $scope.cash_registers.length - 1; i >= 0; i--) {
                        $scope.cash_registers[i].branches_names = [];
                        for (var j = $scope.cash_registers[i].branches.length - 1; j >= 0; j--) {
                            for (var k = $rootScope.user_data.branches.length - 1; k >= 0; k--) {
                                if ($rootScope.user_data.branches[k].id == $scope.cash_registers[i].branches[j]) {
                                    $scope.cash_registers[i].branches_names.push($rootScope.user_data.branches[k].name);
                                }
                            }
                        }
                    }

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.addBanking = function () {
            if ($scope.new_banking_data.id === 0) {
                dashboardHttpRequest.addBanking($scope.new_banking_data)
                    .then(function (data) {
                        $scope.get_banking_data();
                        $scope.resetFrom();
                        $rootScope.close_modal('addBankingModal');
                        
                    }, function (error) {
                        $scope.error_message = error.data.error_msg;
                        $rootScope.open_modal('errorModal', 'addBankingModal');
                    });
            } else {
                dashboardHttpRequest.updateBankingDetail($scope.new_banking_data.id, $scope.new_banking_data)
                    .then(function (data) {
                        $scope.get_banking_data();
                        $scope.resetFrom();
                        $rootScope.close_modal('addBankingModal');
                        
                    }, function (error) {
                        $scope.error_message = error.data.error_msg;
                        $rootScope.open_modal('errorModal', 'addBankingModal');
                    });
            }
        };

        $scope.editBanking = function (banking_id) {
            dashboardHttpRequest.getBankingDetail(banking_id)
                .then(function (data) {
                    $scope.new_banking_data = {
                        'branches':$scope.branches,
                        // 'branches':[],
                        'type':'',
                        'name': '',
                        'bank_name': '',
                        'bank_account': '',
                        'bank_card_number': '',
                        'shaba_number': '',
                    };
                    angular.copy($rootScope.user_data.branches, $scope.new_banking_data.branches)


                    var branches = data['branches'];
                    branches.forEach(function (branch_id) {
                        $scope.new_banking_data.branches.forEach(function (branch) {
                            if (branch_id === branch.id) {
                                branch.is_checked = 1;
                                branch.is_checked_m = 1;
                            }
                        })
                    });

                    $scope.new_banking_data.id = data.id;
                    $scope.new_banking_data.type = data.type;
                    $scope.new_banking_data.name = data.name;
                    $scope.new_banking_data.bank_name = data.bank_name;
                    $scope.new_banking_data.bank_account = data.bank_account;
                    $scope.new_banking_data.bank_card_number = data.bank_card_number;
                    $scope.new_banking_data.shaba_number = data.shaba_number;

                    $rootScope.open_modal('addBankingModal');
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });

        };

        $scope.changeBankingBranchCheckBox = function (branch_id) {
            $scope.new_banking_data.branches.forEach(function (branch) {
                if (branch_id === branch.id) {
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

        $scope.clearBankingBranchesCheckboxes = function () {
            $scope.branches.forEach(function (branch) {
                branch.is_checked = 0;
                branch.is_checked_m = 0;
            });
        };

        $scope.get_branches_data = function () {
            dashboardHttpRequest.getBranches($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.branches = data['branches'];
                        $scope.new_banking_data.branches = $scope.branches;
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

        $scope.closeAddBankingModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addBankingModal').modal('hide');
                $scope.resetFrom();
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_banking_data = {
                'id': 0,
                'branches':[],
                'type':'',
                'name': '',
                'bank_name': '',
                'bank_account': '',
                'bank_card_number': '',
                'shaba_number': ''
            };
            $scope.clearBankingBranchesCheckboxes();
            angular.copy($rootScope.user_data.branches, $scope.new_banking_data.branches);
        };

        initialize();
    });