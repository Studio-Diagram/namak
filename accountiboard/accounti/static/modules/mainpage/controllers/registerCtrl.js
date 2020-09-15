angular.module("mainpage")
    .controller("registerCtrl", function ($scope, $interval, $rootScope, $filter, $http, $state, $auth, $timeout, $window, mainpageHttpRequest) {
        var initialize = function () {
            var reCaptcha_showing = $interval(function () {
                jQuery.noConflict();
                (function ($) {
                    var badge_object = $('.grecaptcha-badge');
                    if (badge_object) {
                        badge_object.css('visibility', 'visible');
                        badge_object.css('opacity', '1');
                        $interval.cancel(reCaptcha_showing);
                    }
                })(jQuery);
            }, 500);

            $scope.new_user = {
                phone: "",
                password: "",
                re_password: "",
                company_name: "",
                company_address: "",
                start_working_time: "",
                end_working_time: "",
                sms_verify_token: ""
            };
            $scope.form_state = {
                "is_error": false,
                "error_msg": "",
                "is_loading": false
            };
            $scope.config_clock();
            $scope.minutes_counter = 120;
            $scope.resend_verification_enable = false;
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

        $scope.register_new_user = function () {
            $scope.form_state.is_loading = true;
            $scope.form_state.is_error = false;
            jQuery.noConflict();
            (function ($) {
                $scope.new_user.end_working_time = $('#end-time-clock').val();
                $scope.new_user.start_working_time = $('#start-time-clock').val();
            })(jQuery);
            mainpageHttpRequest.registerCafeOwner($scope.new_user)
                .then(function (data) {
                    $scope.form_state.is_loading = false;
                    $state.go("main.login");
                }, function (error) {
                    $scope.form_state.is_error = true;
                    $scope.form_state.is_loading = false;
                    $scope.form_state.error_msg = error.data.error_msg;
                });
        };

        $scope.verify_password = function () {
            if ($scope.new_user.password !== $scope.new_user.re_password) {
                $scope.form_state.is_error = true;
                $scope.form_state.is_loading = false;
                $scope.form_state.error_msg = "رمز عبور باید با تکرار آن برابر باشد.";
                return false;
            }
            else if ($scope.new_user.password.length < 8) {
                $scope.form_state.is_error = true;
                $scope.form_state.is_loading = false;
                $scope.form_state.error_msg = "رمز عبور باید حداقل ۸ کاراکتر باشد.";
                return false;
            }
            return true;
        };

        $scope.send_verify_code_to_phone = function () {
            if (!$scope.verify_password()){
                return false
            }
            jQuery.noConflict();
            (function ($) {
                grecaptcha.ready(function () {
                    grecaptcha.execute('6LenhbwZAAAAALB_dr4AvmJyudUMsvSA2rlJkNBm', {action: 'submit'}).then(function (token) {
                        $scope.form_state.is_loading = true;
                        $scope.form_state.is_error = false;
                        mainpageHttpRequest.phoneVerify({
                            phone: $scope.new_user.phone,
                            recaptcha_response_token: token,
                            verify_type: "REGISTER"
                        })
                            .then(function (data) {
                                $scope.form_state.is_loading = false;
                                $scope.change_registration_state('personal_registration', 'phone_verify_final_step');
                                $scope.minutes_counter = 120;
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

        $scope.change_registration_state = function (current_state, target_state) {
            jQuery.noConflict();
            (function ($) {
                if (current_state === "company_registration" && target_state === "personal_registration") {
                    $('#companyRegistrationForm').removeClass('showForm');
                    $('#personalRegistrationForm').addClass('showForm');
                    $scope.new_user.end_working_time = $('#end-time-clock').val();
                    $scope.new_user.start_working_time = $('#start-time-clock').val();
                }
                else if (current_state === "personal_registration" && target_state === "phone_verify_final_step") {
                    $('#personalRegistrationForm').removeClass('showForm');
                    $('#phoneVerifyRegistrationForm').addClass('showForm');
                }
                else if (current_state === "personal_registration" && target_state === "company_registration") {
                    $('#personalRegistrationForm').removeClass('showForm');
                    $('#companyRegistrationForm').addClass('showForm');
                }
                else if (current_state === "activation_code" && target_state === "personal_registration") {
                    $('#phoneVerifyRegistrationForm').removeClass('showForm');
                    $('#personalRegistrationForm').addClass('showForm');
                }
            })(jQuery);
        };

        $scope.config_clock = function () {
            jQuery.noConflict();
            (function ($) {
                var choices = ["00", "15", "30", "45"];
                $('#start-time-clock').clockpicker({
                    donetext: 'تایید',
                    autoclose: true,
                    afterShow: function () {
                        $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                            return !($.inArray($(element).text(), choices) != -1)
                        }).remove();
                    },
                    afterDone: function () {
                        var seleceted_min = $('#start-time-clock').val().split(":")[1];
                        if (!choices.includes(seleceted_min)) {
                            $('#start-time-clock').val("");
                        }
                        else {
                            $scope.new_user.start_working_time = $('#start-time-clock').val();
                        }
                    }
                });
                $('#end-time-clock').clockpicker({
                    donetext: 'تایید',
                    autoclose: true,
                    afterShow: function () {
                        $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                            return !($.inArray($(element).text(), choices) != -1)
                        }).remove();
                    },
                    afterHide: function () {
                        var seleceted_min = $('#end-time-clock').val().split(":")[1];
                        if (!choices.includes(seleceted_min)) {
                            $('#end-time-clock').val("");
                        }
                        else {
                            $scope.new_user.end_working_time = $('#end-time-clock').val();
                        }
                    }
                });
            })(jQuery);
        };

        initialize();
    });