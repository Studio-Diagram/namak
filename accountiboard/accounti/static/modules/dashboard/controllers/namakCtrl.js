angular.module("dashboard")
    .controller("namakCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {

            // var split_url = $location.path().split('/');
            // if ($location.path() === '/cafe/namak' || $location.path() === '/cafe/namak/') {
            //     $state.go('cafe_management.namak');
            // }
            // else if ($location.path() === '/cafe/namak/bundles') {
            //     $state.go('cafe_management.namak_bundles');
            // }

            $rootScope.is_page_loading = false;

        };

        initialize();
    });