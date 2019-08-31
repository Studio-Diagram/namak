angular.module("dashboard")
    .controller("managerCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location) {
        var initialize = function () {
            if ($location.path() === '/manager' || $location.path() === '/manager/') {
                $state.go('manager.addEmployee');
            }
            if ($location.path() === '/cash_manager' || $location.path() === '/cash_manager/') {
                $scope.check_cash($rootScope.user_data);
            }
            if ($location.path() === '/account_manager') {
                $state.go('account_manager.buy');
            }

            $scope.get_employees_data($rootScope.user_data);
        };

        $scope.get_employees_data = function (data) {
            dashboardHttpRequest.getEmployees(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.employees = data['employees'];
                    }
                    else if (data['response_code'] === 3) {
                        console.log("NOT SUCCESS!");
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        $scope.check_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.checkCashExist(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $state.go("cash_manager.salon");
                    }
                    else if (data['response_code'] === 3) {
                        if (data['error_mode'] === "NO_CASH") {
                            $state.go("cash_disable", {state: "NO_CASH"});
                        }
                        if (data['error_mode'] === "OLD_CASH") {
                            $state.go("cash_disable", {state: "OLD_CASH"});
                        }
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };
        initialize();
    });