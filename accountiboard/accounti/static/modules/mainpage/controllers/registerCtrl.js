angular.module("mainpage")
    .controller("registerCtrl", function ($scope, $interval, $rootScope, $filter, $http, $state, $auth, $timeout, $window, mainpageHttpRequest) {
        var initialize = function () {
            $scope.new_user = {
                "company_name": '',
                "email": '',
                "phone": '',
                "password": '',
                "re_password": ''
            };
            $scope.form_state = {
                "is_error": false,
                "error_msg": "",
                "is_loading": false
            };
        };

        $scope.register_new_user = function () {
            $scope.form_state.is_loading = true;
            mainpageHttpRequest.registerUser($scope.new_user)
                .then(function (data) {
                    $scope.form_state.is_loading = false;
                    if (data['response_code'] === 2) {
                        $state.go("login");
                    }
                    else if (data['response_code'] === 3) {
                        $scope.form_state.is_error = true;
                        $scope.form_state.error_msg = data['error_msg'];
                    }
                }, function (error) {
                    $scope.form_state.is_error = true;
                    $scope.form_state.is_loading = false;
                    $scope.form_state.error_msg = error;
                });
        };
        initialize();
    });