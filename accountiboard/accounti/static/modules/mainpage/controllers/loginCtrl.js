angular.module("mainpage")
    .controller("loginCtrl", function ($scope, $interval, $rootScope, $filter, $http, $auth, $timeout, $window, mainpageHttpRequest) {
        var initialize = function () {
            $scope.user_login_data = {
                "username": '',
                "password": ''
            };
            $scope.form_state = {
                "is_error": false,
                "error_msg": "",
                "is_loading": false
            };
        };

        $scope.send_login_data = function () {
            $scope.form_state.is_loading = true;
            mainpageHttpRequest.loginUser($scope.user_login_data)
                .then(function (data) {
                    $scope.form_state.is_loading = false;
                    if (data['response_code'] === 2) {
                        var logged_in_user = data['user_data']['username'];
                        var branch = data['user_data']['branch'];
                        localStorage.user = JSON.stringify(logged_in_user);
                        localStorage.branch = JSON.stringify(branch);
                        $auth.setToken(data['token']);
                        $window.location.href = '/dashboard';
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