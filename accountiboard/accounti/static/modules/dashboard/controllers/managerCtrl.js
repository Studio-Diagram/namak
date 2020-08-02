angular.module("dashboard")
    .controller("managerCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location) {
        var initialize = function () {
            var split_url = $location.path().split('/');
            if ($location.path() === '/manager' || $location.path() === '/manager/') {
                $state.go('manager.addEmployee');
            }
            if (split_url.indexOf('cash_manager')) {
                $scope.check_cash($rootScope.user_data);
            }
            if ($location.path() === '/account_manager') {
                $state.go('account_manager.buy');
            }
        };

        $scope.check_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.checkCashExist(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.cash_state = "";
                        $state.go("cash_manager.salon");
                    }
                    else if (data['response_code'] === 3) {
                        if (data['error_mode'] === "NO_CASH") {
                            $rootScope.cash_state = "NO_CASH";
                            $state.go("cash_disable", {state: "NO_CASH"});
                        }
                        if (data['error_mode'] === "OLD_CASH") {
                            $rootScope.cash_state = "OLD_CASH";
                            $rootScope.error_message = "شما در حال استفاده از صندوق قدیمی ( روز گذشته ) هستید، تمام فاکتورها را تسویه کنید سپس صندوق را ببندید و یک صندوق جدید باز کنید.";
                            $scope.open_modal('errorModal');
                            // $state.go("cash_disable", {state: "OLD_CASH"});
                        }
                    }
                    $rootScope.is_page_loading = false;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };
        initialize();
    });