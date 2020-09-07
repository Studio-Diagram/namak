angular.module("dashboard")
    .controller("settledInvoiceModalCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
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
                            'menu_items_old': data['invoice']['menu_items_old'],
                            'shop_items_old': data['invoice']['shop_items_old'],
                            'games': data['invoice']['games'],
                            'total_price': data['invoice']['total_price'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            "cash_amount": Number(data['invoice']['cash_amount']),
                            "pos_amount": Number(data['invoice']['pos_amount']),
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit']
                        };
                        $scope.openViewSettledInvoiceModal();
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



        $scope.openViewSettledInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#viewSettledInvoiceModal').modal('show');
            })(jQuery);
        };



        initialize();
    });