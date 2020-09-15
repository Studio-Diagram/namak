angular.module("dashboard")
    .controller("transactionsCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.get_all_transactions();
            $rootScope.is_page_loading = false;
        };


        $scope.get_all_transactions = function () {
            dashboardHttpRequest.getAllTransactions()
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.all_transactions = data.all_transactions;

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };


        initialize();
    });