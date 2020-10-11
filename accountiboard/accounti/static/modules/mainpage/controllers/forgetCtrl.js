angular.module("mainpage")
    .controller("forgetCtrl", function ($scope, $interval, $rootScope, $filter, $http, $auth, $timeout, $window, mainpageHttpRequest, $state) {
        var initialize = function () {
            $scope.minutes_counter = 120;
            $scope.resend_verification_enable = false;
            $scope.user_forget_password_data = {
                "phone": '',
                "password": '',
                "re_password": '',
                "sms_verify_token": ''
            };
            $scope.form_state = {
                "is_error": false,
                "error_msg": "",
                "is_loading": false
            };
        };

        $scope.verify_password = function () {
            if ($scope.user_forget_password_data.password !== $scope.user_forget_password_data.re_password) {
                $scope.form_state.is_error = true;
                $scope.form_state.is_loading = false;
                $scope.form_state.error_msg = "رمز عبور باید با تکرار آن برابر باشد.";
                return false;
            }
            else if ($scope.user_forget_password_data.password.length < 8) {
                $scope.form_state.is_error = true;
                $scope.form_state.is_loading = false;
                $scope.form_state.error_msg = "رمز عبور باید حداقل ۸ کاراکتر باشد.";
                return false;
            }
            return true;
        };

        $scope.start_timer = function () {
            var interval = $interval(function () {
                if ($scope.minutes_counter !== 0) {
                    $scope.minutes_counter--;
                }
                else {
                    $scope.resend_verification_enable = true;
                    $interval.cancel(interval);
                }
            }, 1000, 0);
        };

        $scope.send_forget_password = function () {
            if (!$scope.verify_password()){
                return false
            }
            $scope.form_state.is_loading = true;
            $scope.form_state.is_error = false;
            mainpageHttpRequest.forgetPassword($scope.user_forget_password_data)
                .then(function (data) {
                    $scope.form_state.is_loading = false;
                    $state.go("main.login");
                }, function (error) {
                    $scope.form_state.is_error = true;
                    $scope.form_state.is_loading = false;
                    $scope.form_state.error_msg = error.data.error_msg;
                });
        };

        $scope.send_verify_code_to_phone = function () {
            $scope.form_state.is_loading = true;
            jQuery.noConflict();
            (function ($) {
                grecaptcha.ready(function () {
                    grecaptcha.execute('6LenhbwZAAAAALB_dr4AvmJyudUMsvSA2rlJkNBm', {action: 'submit'}).then(function (token) {
                        $scope.minutes_counter = 120;
                        $scope.resend_verification_enable = false;
                        $scope.form_state.is_loading = true;
                        $scope.form_state.is_error = false;
                        mainpageHttpRequest.phoneVerify({
                            phone: $scope.user_forget_password_data.phone,
                            recaptcha_response_token: token,
                            verify_type: "FORGET"
                        })
                            .then(function (data) {
                                $scope.form_state.is_loading = false;
                                $scope.change_form_state('sendVerifyCodeForgetPassword', 'changePasswordForgetPassword');
                                $scope.start_timer();
                            }, function (error) {
                                $scope.form_state.is_error = true;
                                $scope.form_state.is_loading = false;
                                $scope.form_state.error_msg = error.data.error_msg;
                            });
                    });
                });
            })(jQuery);
        };

        $scope.change_form_state = function (current_state, target_state) {
            jQuery.noConflict();
            (function ($) {
                if (current_state === "sendVerifyCodeForgetPassword" && target_state === "changePasswordForgetPassword") {
                    $('#sendVerifyCodeForgetPassword').removeClass('showForm');
                    $('#changePasswordForgetPassword').addClass('showForm');
                }
            })(jQuery);
        };

        initialize();
    });