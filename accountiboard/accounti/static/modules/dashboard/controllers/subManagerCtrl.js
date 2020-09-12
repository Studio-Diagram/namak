angular.module("dashboard")
    .controller("subManagerCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
        };

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };

        initialize();
    });