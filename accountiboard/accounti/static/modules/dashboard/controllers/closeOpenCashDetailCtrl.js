angular.module("dashboard")
    .controller("closeOpenCashDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
            $scope.get_cash_and_related_invoices();
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

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
        };


        initialize();
    });