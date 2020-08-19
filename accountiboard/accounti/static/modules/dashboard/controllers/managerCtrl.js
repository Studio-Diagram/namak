angular.module("dashboard")
    .controller("managerCtrl", function ($scope, $state, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location) {
        var initialize = function () {
            var split_url = $location.path().split('/');
            if ($location.path() === '/manager' || $location.path() === '/manager/') {
                $state.go('manager.addEmployee');
            }
            if ($location.path() === '/account_manager') {
                $state.go('account_manager.buy');
            }
        };

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };
        initialize();
    });