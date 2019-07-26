angular.module("dashboard")
    .controller("managerCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location) {
        var initialize = function () {
            if ($location.path() === '/manager' || $location.path() === '/manager/'){
                $state.go('manager.addEmployee');
            }
            if ($location.path() === '/cash_manager' || $location.path() === '/cash_manager/'){
                $state.go("cash_manager.salon");
            }
            if ($location.path() === '/account_manager'){
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

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };
        initialize();
    });