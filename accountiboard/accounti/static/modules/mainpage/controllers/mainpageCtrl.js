angular.module("mainpage")
    .controller("mainpageCtrl", function ($scope, $interval, $rootScope, $filter, $http, $state) {
        var initialize = function () {
            $state.go('main.login');
        };

        initialize();
    });