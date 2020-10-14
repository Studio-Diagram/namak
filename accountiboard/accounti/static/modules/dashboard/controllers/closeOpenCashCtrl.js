angular.module("dashboard")
    .controller("closeOpenCashCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, offlineAPIHttpRequest) {
        var initialize = function () {
            $scope.get_all_cashes();
        };

        $scope.get_all_cashes = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getAllCashes(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.all_cashes = data['all_cashes'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

                });
        };

        initialize();
    });