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
            mainpageHttpRequest.registerCafeOwner($scope.new_user)
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

        $scope.send_verify_code_to_phone = function () {
            jQuery.noConflict();
            (function ($) {
                grecaptcha.ready(function () {
                    grecaptcha.execute('6LenhbwZAAAAALB_dr4AvmJyudUMsvSA2rlJkNBm', {action: 'submit'}).then(function (token) {
                        $scope.form_state.is_loading = true;
                        mainpageHttpRequest.phoneVerify({
                            phone: $scope.new_user.phone,
                            recaptcha_response_token: token
                        })
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
                }
                else if (current_state === "personal_registration" && target_state === "phone_verify_final_step") {
                    $('#personalRegistrationForm').removeClass('showForm');
                    $('#phoneVerifyRegistrationForm').addClass('showForm');
                }
            })(jQuery);
        };

        initialize();
    });