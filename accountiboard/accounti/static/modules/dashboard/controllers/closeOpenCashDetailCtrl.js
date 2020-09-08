angular.module("dashboard")
    .controller("closeOpenCashDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
            $scope.show_initiate_edit_payment_invoice_sale = false;
            $scope.get_cash_and_related_invoices();
            $scope.get_status_data();
        };

        $scope.get_cash_and_related_invoices = function () {
            dashboardHttpRequest.getCashAndRelatedInvoices($scope.cash_id)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.current_cash = data;
                    $scope.current_cash.is_closed ? $scope.current_cash.is_closed = "بسته‌شده" : $scope.current_cash.is_closed = "باز";
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error.data.error_msg;
                    $scope.openErrorModal();
                });

        };

        $scope.get_status_data = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $scope.cash_id
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

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
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