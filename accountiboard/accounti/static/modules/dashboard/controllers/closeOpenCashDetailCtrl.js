angular.module("dashboard")
    .controller("closeOpenCashDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
            $scope.get_cash_and_related_invoices();
            $scope.get_status_data();
        };

        $scope.get_cash_and_related_invoices = function () {
            dashboardHttpRequest.getCashAndRelatedInvoices($scope.cash_id)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.current_cash = data;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });

        };

        $scope.get_status_data = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $scope.cash_id
            };
            dashboardHttpRequest.getTodayStatus(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.status = data['all_today_status'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.error_message = data['error_msg'];
                        $rootScope.open_modal('mainErrorModal');

                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = 500;
                    $rootScope.open_modal('mainErrorModal');

                });
        };

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
        };


        initialize();
    });