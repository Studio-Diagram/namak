angular.module("dashboard")
    .controller("cashDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, $auth, dashboardHttpRequest, offlineAPIHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.selected_detail_category = "";
            $scope.night_report_inputs = {
                "income_report": 0,
                "outcome_report": 0,
                "event_tickets": 0,
                "current_money_in_cash": 0
            };
            $scope.sale_detail_category_filter = "";
            if ($stateParams.cash_id !== 0) {
                $scope.get_status_data();
            }
            else {
                $scope.get_today_cash();
            }
            $scope.display_cash_number = $stateParams.display_cash_number;
            $scope.cash_id = $stateParams.cash_id;
            $scope.show_submit_today_cash_button = $stateParams.show_submit_today_cash_button;
            $scope.show_print_today_cash_button = $stateParams.show_print_today_cash_button;
        };

        $scope.get_status_data = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $stateParams.cash_id
            };
            dashboardHttpRequest.getTodayStatus(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.status = data['all_today_status'];
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };

        $scope.change_detail_sale_category = function () {
            if ($scope.selected_detail_category === "BAR")
                $scope.get_bar_detail_sales();
            else if ($scope.selected_detail_category === "KITCHEN")
                $scope.get_kitchen_detail_sales();
            else if ($scope.selected_detail_category === "OTHER")
                $scope.get_other_detail_sales();
        };

        $scope.get_menu_categories_base_on_kind = function (kind) {
            $scope.selected_detail_category = kind;
            var sending_data = {
                'username': $rootScope.user_data.username,
                'kind': kind,
                'current_branch': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getCategoriesBaseOnKind(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.detail_categories = data['categories'];
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
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $stateParams.cash_id,
                "menu_category_id": $scope.sale_detail_category_filter
            };
            dashboardHttpRequest.getKitchenDetailSales(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.sale_details = data['sale_details'];
                    $scope.open_modal("sale_details");
                }, function (error) {
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };

        $scope.get_bar_detail_sales = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $stateParams.cash_id,
                "menu_category_id": $scope.sale_detail_category_filter
            };
            dashboardHttpRequest.getBarDetailSales(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.sale_details = data['sale_details'];
                    $scope.open_modal("sale_details");
                }, function (error) {
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };

        $scope.get_other_detail_sales = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $stateParams.cash_id,
                "menu_category_id": $scope.sale_detail_category_filter
            };
            dashboardHttpRequest.getOtherDetailSales(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.sale_details = data['sale_details'];
                    $scope.open_modal("sale_details");
                }, function (error) {
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $stateParams.cash_id = data['cash_id'];
                        $scope.get_status_data();
                    }
                    else if (data['response_code'] === 3) {
                        $stateParams.cash_id = 0;
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
                        $scope.close_cash_offline();
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

        $scope.close_cash_offline = function () {
            var sending_data = {
                'night_report_inputs': $scope.night_report_inputs,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            offlineAPIHttpRequest.close_cash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                    // $scope.error_message = error;
                    // $scope.openErrorModal();
                });
        };

        $scope.log_out = function () {
            $auth.logout();
            $window.location.href = '/';
        };

        $scope.print_night_report = function () {
            var sending_data = {
                'cash_id': $stateParams.cash_id,
                'location_url': "https://namak.works/"
            };
            $http({
                method: 'POST',
                url: 'http://127.0.0.1:8000/printNightReport',
                data: sending_data,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {

            }, function errorCallback(response) {
                $scope.error_message = "اتصال سرور پرینتر نمک برقرار نیست، مجددا برنامه پرینتر نمک را اجرا کنید";
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