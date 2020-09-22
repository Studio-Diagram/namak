angular.module("dashboard")
    .controller("settledInvoiceModalCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
            $scope.first_time_edit_payment_init = 2;
            $scope.show_invoice_data = {
                invoice_sales_id: 0,
                cash_amount: 10000000000000000000,
                pos_amount: 0
            };
        };

        $scope.showInvoice = function (invoice_id, showEditPaymentButton, showPrintButton) {
            $scope.settledInvoiceEditPaymentButton = showEditPaymentButton;
            $scope.settledInvoicePrintButton = showPrintButton;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getInvoice(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.show_invoice_data = {
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
                        $scope.open_modal('viewSettledInvoiceModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.edit_settled_invoice_payment = function () {
            var sending_data = {
                "invoice_data": {
                    invoice_id: $scope.show_invoice_data.invoice_sales_id,
                    cash: $scope.show_invoice_data.cash_amount,
                    pos: $scope.show_invoice_data.pos_amount,
                    total: $scope.show_invoice_data.cash + $scope.show_invoice_data.pos
                }
            };
            dashboardHttpRequest.editPaymentInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.close_modal('editSettledInvoicePayment', 'viewSettledInvoiceModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                });
        };

        $scope.edit_payment_modal_changer = function () {
            if ($scope.first_time_edit_payment_init) {
                $timeout(function () {
                    $scope.first_time_edit_payment_init -= 1;
                });
            }
            else {
                $scope.show_invoice_data.pos = $scope.show_invoice_data.total - $scope.show_invoice_data.cash;
            }
        };


        initialize();
    });