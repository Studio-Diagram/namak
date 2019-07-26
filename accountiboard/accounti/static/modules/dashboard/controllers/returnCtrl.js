angular.module("dashboard")
    .controller("returnCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.new_invoice_return_data = {
                'id': 0,
                'supplier_id': 0,
                'shop_id': '',
                'numbers': 0,
                'buy_price': 0,
                'return_type': 'CUSTOMER_TO_CAFE',
                'description': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_return = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.get_returns();
            $scope.get_suppliers();
            $scope.get_shop_products();
        };

        $scope.get_last_buy_price = function (shop_product_id) {
            var sending_data = {
                'shop_product_id': shop_product_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getLastBuyPrice(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_return_data.buy_price = data['last_buy_price'];
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


        $scope.get_shop_products = function () {
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getShopProducts(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.shops = data['shop_products'];
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

        $scope.get_suppliers = function () {
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getSuppliers(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
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

        $scope.openAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.addReturn = function () {
            dashboardHttpRequest.addReturn($scope.new_invoice_return_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_returns();
                        $scope.resetFrom();
                        $scope.closeAddModal();
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

        $scope.searchReturn = function () {
            if ($scope.search_data_return.search_word === '') {
                $scope.get_returns();
            }
            else {
                dashboardHttpRequest.searchReturn($scope.search_data_return)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.returns = data['returns'];
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
        };

        $scope.get_returns = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getAllReturns(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.returns = data['invoices'];
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

        $scope.resetFrom = function () {
            $scope.new_invoice_return_data = {
                'id': 0,
                'supplier_id': 0,
                'shop_id': '',
                'numbers': 0,
                'buy_price': 0,
                'return_type': 'CUSTOMER_TO_CAFE',
                'description': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };
        initialize();
    });