angular.module("dashboard")
    .controller("bundlesCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.get_bundles();
            $rootScope.is_page_loading = false;
        };


        $scope.get_bundles = function () {
            dashboardHttpRequest.getBundles()
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.active_bundle = data.active_bundle;
                    $scope.reserved_bundles = data.reserved_bundles;
                    $scope.expired_bundles = data.expired_bundles;
                    $scope.not_successfully_paid_bundles = data.not_successfully_paid_bundles;

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };


        initialize();
    });