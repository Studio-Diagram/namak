angular.module("dashboard")
    .controller("statusCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.get_status_data();
        };

        $scope.get_status_data = function (data) {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch,
            };
            dashboardHttpRequest.getTodayStatus(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.status = data['all_today_status'];
                    }
                    else if (data['response_code'] === 3) {
                        console.log("NOT SUCCESS!");
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        initialize();
    });