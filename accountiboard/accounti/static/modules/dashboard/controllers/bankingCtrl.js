angular.module("dashboard")
    .controller("bankingCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.new_banking_data = {
                'branch':'',
                'type':'',
                'name': '',
                'unit': 'IR-RIAL',
                'bank_name': '',
                'bank_account': '',
                'bank_card_number': '',
                'shaba_number': '',
            };
            $scope.get_banking_data();
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBanking()
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.branches = $rootScope.user_data.branches;
                    $scope.banks = data['bank'];
                    $scope.tankhahs = data['tankhah'];
                    $scope.cash_registers = data['cash_register'];

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.addBanking = function () {
            dashboardHttpRequest.addBanking($scope.new_banking_data)
                .then(function (data) {
                    $scope.get_banking_data();
                    $scope.resetFrom();
                    $rootScope.close_modal('addBankingModal');
                    
                }, function (error) {
                    $scope.error_message = error;
                    $rootScope.open_modal('errorModal', 'addBankingModal');
                });
        };

        $scope.editBanking = function (banking_id) {
            dashboardHttpRequest.getBankingDetail(banking_id)
                .then(function (data) {
                    $scope.new_banking_data.branch = data.branches[0];
                    $scope.new_banking_data.type = data.type;
                    $scope.new_banking_data.name = data.name;
                    $scope.new_banking_data.unit = data.unit;
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

        $scope.resetFrom = function () {
            $scope.new_banking_data = {
                'branch':'',
                'type':'',
                'name': '',
                'unit': 'IR-RIAL',
                'bank_name': '',
                'bank_account': '',
                'bank_card_number': '',
                'shaba_number': '',
            };
        };

        initialize();
    });