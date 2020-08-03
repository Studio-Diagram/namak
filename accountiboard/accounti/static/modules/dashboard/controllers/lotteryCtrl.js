angular.module("dashboard")
    .controller("lotteryCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker_start_lottery").datepicker();
                    $("#datepicker_end_lottery").datepicker();
                });

            })(jQuery);
            $scope.is_in_edit_mode = false;
            $scope.new_lottery_data = {
                'start_date': '',
                'end_date': '',
                'prize': '',
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch
            };

            $scope.get_lotteries_data($rootScope.user_data);
        };

        $scope.get_lotteries_data = function (data) {
            dashboardHttpRequest.getLotteries(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.lotteries = data['lotteries'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.give_prize = function (lottery_id) {
            var sending_data = {
                "lottery_id": lottery_id,
                "username": $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch
            };
            dashboardHttpRequest.givePrize(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_lotteries_data($rootScope.user_data);
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.openAddLotteryModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addLotteryModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddLotteryModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addLotteryModal').modal('hide');
            })(jQuery);
            $scope.resetFrom();
        };

        $scope.addLottery = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_lottery_data.start_date = $("#datepicker_start_lottery").val();
                $scope.new_lottery_data.end_date = $("#datepicker_end_lottery").val();
            })(jQuery);
            dashboardHttpRequest.addLottery($scope.new_lottery_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_lotteries_data($rootScope.user_data);
                        $scope.closeAddLotteryModal();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addMemberModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addMemberModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_lottery_data = {
                'start_date': '',
                'end_date': '',
                'prize': '',
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddMemberModal();
        };
        initialize();
    });