angular.module("mainpage")
    .controller("mainpageCtrl", function ($scope, $interval, $rootScope, $filter, $http, $state, $auth, $timeout, $window, mainpageHttpRequest) {
        var initialize = function () {
            // $state.go('main.login');
        };

        initialize();
    });