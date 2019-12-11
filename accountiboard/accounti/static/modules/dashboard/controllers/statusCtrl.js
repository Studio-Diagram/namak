angular.module("dashboard")
    .controller("statusCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            if ($rootScope.cash_data.cash_id !== 0) {
                $scope.get_status_data();
            }
            else {
                $scope.get_today_cash();
            }
        };

        $scope.get_status_data = function () {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };
            dashboardHttpRequest.getTodayStatus(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.status = data['all_today_status'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_kitchen_detail_sales = function () {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };
            dashboardHttpRequest.getKitchenDetailSales(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sale_details = data['sale_details'];
                        $scope.open_modal("sale_details");
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_bar_detail_sales = function () {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };
            dashboardHttpRequest.getBarDetailSales(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sale_details = data['sale_details'];
                        $scope.open_modal("sale_details");
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_other_detail_sales = function () {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };
            dashboardHttpRequest.getOtherDetailSales(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.sale_details = data['sale_details'];
                        $scope.open_modal("sale_details");
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.cash_data.cash_id = data['cash_id'];
                        $scope.get_status_data();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.cash_data.cash_id = 0;
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.openPermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closePermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.close_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.closeCash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.log_out();
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

        $scope.log_out = function () {
            dashboardHttpRequest.logOut($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $window.location.href = '/';
                        $rootScope.user_data = {
                            "username": '',
                            "branch": ''
                        };
                    }
                    else if (data['response_code'] === 3) {
                        $window.location.href = '/';
                        $rootScope.user_data = {
                            "username": '',
                            "branch": ''
                        };
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        initialize();
    });