angular.module("dashboard")
    .controller("cashDisableCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $stateParams, offlineAPIHttpRequest) {
        var initialize = function () {
            $scope.cash_state = $stateParams.state;
        };

        $scope.open_cash = function () {
            dashboardHttpRequest.openCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.open_cash_offline(data['new_cash_id']);
                        $scope.get_today_cash();
                        $state.go("cash_manager");
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_message'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.close_then_open_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.closeCash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.close_cash_offline();
                        $scope.open_cash();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_message'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.close_cash_offline = function () {
            var sending_data = {
                'night_report_inputs': $scope.night_report_inputs,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            offlineAPIHttpRequest.close_cash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                    // $scope.error_message = error;
                    // $scope.openErrorModal();
                });
        };

        $scope.open_cash_offline = function (new_cash_id) {
            var sending_data = {
                "username": $rootScope.user_data.username,
                "branch": $rootScope.user_data.branch,
                "cash_server_id": new_cash_id
            };
            offlineAPIHttpRequest.open_cash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                    // $scope.error_message = error;
                    // $scope.openErrorModal();
                });
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
            })(jQuery);
        };

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.cash_data.cash_id = data['cash_id'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.cash_data.cash_id = 0;
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        initialize();
    });