angular.module("dashboard")
    .controller("statusCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.night_report_inputs = {
                "income_report": 0,
                "outcome_report": 0,
                "event_tickets": 0,
                "current_money_in_cash": 0
            };
            $scope.bar_sale_detail_category_filter = "";
            if ($rootScope.cash_data.cash_id !== 0) {
                $scope.get_status_data();
            }
            else {
                $scope.get_today_cash();
            }
            $scope.get_menu_categories_base_on_kind("BAR");
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

        $scope.get_menu_categories_base_on_kind = function (kind) {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'kind': kind
            };
            dashboardHttpRequest.getCategoriesBaseOnKind(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        if (kind === "BAR")
                            $scope.bar_categories = data['categories'];
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
                'cash_id': $rootScope.cash_data.cash_id,
                "menu_category_id": $scope.bar_sale_detail_category_filter
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
            $rootScope.open_modal('closeInvoicePermissionModal', 'submit_cash_today_modal');
        };

        $scope.closePermissionModal = function () {
            $rootScope.close_modal('closeInvoicePermissionModal', 'submit_cash_today_modal');
        };

        $scope.close_cash = function () {
            var sending_data = {
                'night_report_inputs': $scope.night_report_inputs,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.closeCash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.print_night_report();
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

        $scope.print_night_report = function () {
            var sending_data = {
                'cash_id': $rootScope.cash_data.cash_id
            };
            $http({
                method: 'POST',
                url: 'http://127.0.0.1:8000/printNightReport',
                data: sending_data,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {

            }, function errorCallback(response) {
                $scope.error_message = "Printer Server not connected.";
                $scope.openErrorModal();
            });
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        initialize();
    });