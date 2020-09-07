angular.module("dashboard")
    .controller("closeOpenCashDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
            $scope.get_cash();
        };


        $scope.get_cash = function () {
            dashboardHttpRequest.getCash($scope.cash_id)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.current_cash = data;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });

        };



        $scope.showInvoice = function (invoice_id) {
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch,
            };
            dashboardHttpRequest.getInvoice(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data = {
                            'invoice_sales_id': data['invoice']['invoice_sales_id'],
                            'table_id': data['invoice']['table_id'],
                            'table_name': data['invoice']['table_name'],
                            'member_id': data['invoice']['member_id'],
                            'guest_numbers': data['invoice']['guest_numbers'],
                            'member_name': data['invoice']['member_name'],
                            'member_data': data['invoice']['member_data'],
                            'current_game': {
                                'id': data['invoice']['current_game']['id'],
                                'numbers': data['invoice']['current_game']['numbers'],
                                'start_time': data['invoice']['current_game']['start_time']
                            },
                            'menu_items_old': data['invoice']['menu_items_old'],
                            'shop_items_old': data['invoice']['shop_items_old'],
                            'menu_items_new': [],
                            'shop_items_new': [],
                            'games': data['invoice']['games'],
                            'total_price': data['invoice']['total_price'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            "cash_amount": Number(data['invoice']['cash_amount']),
                            "pos_amount": Number(data['invoice']['pos_amount']),
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openViewInvoiceModal();
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



        $scope.openViewInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#viewInvoiceModal2').modal('show');
            })(jQuery);
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