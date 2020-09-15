angular.module("dashboard")
    .controller("namakCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
        };

        initialize();
    });