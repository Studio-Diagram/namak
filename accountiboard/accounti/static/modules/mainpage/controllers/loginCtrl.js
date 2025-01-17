angular.module("mainpage")
    .controller("loginCtrl", function ($scope, $interval, $rootScope, $filter, $http, $auth, $timeout, $window, mainpageHttpRequest, deviceDetector) {
        var initialize = function () {
            $scope.user_login_data = {
                "username": '',
                "password": '',
                "recaptcha_response_token": ''
            };
            $scope.form_state = {
                "is_error": false,
                "error_msg": "",
                "is_loading": false
            };
        };

        $scope.send_login_data = function () {
            $scope.form_state.is_loading = true;
            $scope.form_state.is_error = false;
            jQuery.noConflict();
            (function ($) {
                grecaptcha.ready(function () {
                    grecaptcha.execute('6LenhbwZAAAAALB_dr4AvmJyudUMsvSA2rlJkNBm', {action: 'submit'}).then(function (token) {
                        $scope.user_login_data.recaptcha_response_token = token;
                        mainpageHttpRequest.loginUser($scope.user_login_data)
                            .then(function (data) {
                                $scope.form_state.is_loading = false;
                                $scope.form_state.is_error = false;
                                localStorage.user = JSON.stringify(data['user_data']['username']);
                                localStorage.branch = JSON.stringify(data['user_data']['branch']);
                                localStorage.branches = JSON.stringify(data['user_data']['branches']);
                                localStorage.user_roles = JSON.stringify(data['user_data']['user_roles']);
                                localStorage.full_name = JSON.stringify(data['user_data']['full_name']);
                                localStorage.organization_name = JSON.stringify(data['user_data']['organization_name']);
                                $auth.setToken(data['token']);
                                $scope.deviceDetector = deviceDetector;
                                if ($scope.deviceDetector.isMobile() || $scope.deviceDetector.isTablet()) {
                                    $window.location.href = "/mobile";
                                }
                                else {
                                    $window.location.href = '/dashboard';
                                }
                            }, function (error) {
                                $scope.form_state.is_error = true;
                                $scope.form_state.is_loading = false;
                                $scope.form_state.error_msg = error.data.error_msg;
                            });
                    });
                });
            })(jQuery);
        };
        initialize();
    });