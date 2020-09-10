angular.module("dashboard")
    .controller("managerCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location) {
        var initialize = function () {
            var split_url = $location.path().split('/');
            if ($location.path() === '/manager' || $location.path() === '/manager/') {
                $state.go('manager.tables');
            }
            if ($location.path() === '/account_manager') {
                $state.go('account_manager.buy');
            }
            $scope.get_today_cash();
        };

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };


        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.cash_id = data['cash_id'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.cash_id = 0;
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        initialize();
    });