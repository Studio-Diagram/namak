angular.module("mainpage")
    .controller("loginCtrl", function ($scope, $interval, $rootScope, $filter, $http, $auth, $timeout, $window, mainpageHttpRequest) {
        var initialize = function () {
            $scope.user_login_data = {
                "username": '',
                "password": '',
                "recaptcha_token": ''
            };
            $scope.form_state = {
                "is_error": false,
                "error_msg": "",
                "is_loading": false
            };
        };

        $scope.send_login_data = function () {
            jQuery.noConflict();
            (function ($) {
                grecaptcha.ready(function() {
                  grecaptcha.execute('6LenhbwZAAAAALB_dr4AvmJyudUMsvSA2rlJkNBm', {action: 'submit'}).then(function(token) {
                    console.log(token);
                  });
                });
            })(jQuery);
            
            $scope.form_state.is_loading = true;
            mainpageHttpRequest.loginUser($scope.user_login_data)
                .then(function (data) {
                    $scope.form_state.is_loading = false;
                    if (data['response_code'] === 2) {
                        localStorage.user = JSON.stringify(data['user_data']['username']);
                        localStorage.branch = JSON.stringify(data['user_data']['branch']);
                        localStorage.branches = JSON.stringify(data['user_data']['branches']);
                        localStorage.user_roles = JSON.stringify(data['user_data']['user_roles']);
                        localStorage.full_name = JSON.stringify(data['user_data']['full_name']);
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