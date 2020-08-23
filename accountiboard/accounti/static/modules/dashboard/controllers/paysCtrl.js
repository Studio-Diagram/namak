angular.module("dashboard")
    .controller("paysCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $scope.set_today_for_invoice();
            $scope.error_message = '';
            $scope.new_pay_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'payment_amount': 0,
                'backup_code': '',
                'settle_type': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username,
                'banking_id':''
            };
            $scope.search_data_pay = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.get_pays();
            $scope.get_suppliers();
            $scope.get_banking_data();

        };

        $scope.set_today_for_invoice = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    var date = new Date();
                    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                    $("#datepicker").datepicker();
                    $('#datepicker').datepicker('setDate', today);
                });
            })(jQuery);
        };

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_pay_data.factor_number = data['next_factor_number'];
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
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
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
            $scope.set_today_for_invoice();
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

        $scope.addPay = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_pay_data.date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addPay($scope.new_pay_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_pays();
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

        $scope.searchPay = function () {
            if ($scope.search_data_pay.search_word === '') {
                $scope.get_pays();
            }
            else {
                dashboardHttpRequest.searchPay($scope.search_data_pay)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.pays = data['pays'];
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

        $scope.get_pays = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getAllPays(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.pays = data['invoices']
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

        $scope.delete_invoice_pay = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.deleteInvoiceSettlement(sending_data)
                .then(function (data) {
                    $scope.closeDeletePermissionModal();
                    if (data['response_code'] === 2) {
                        $scope.get_pays();
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

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBankingByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.allbanking_names = [];
                    data['bank'].forEach(function (bank) {
                        $scope.allbanking_names.push({'id':bank.id, 'name':bank.name});
                    });

                    data['tankhah'].forEach(function (tankhah) {
                        $scope.allbanking_names.push({'id':tankhah.id, 'name':tankhah.name});
                    });

                    data['cash_register'].forEach(function (cash_register) {
                        $scope.allbanking_names.push({'id':cash_register.id, 'name':cash_register.name});
                    });

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.openDeletePermissionModal = function (invoice_id) {
            $scope.deleteing_invoice_id = invoice_id;
            jQuery.noConflict();
            (function ($) {
                $('#deleteInvoicePermissionModal').modal('show');
            })(jQuery);
        };

        $scope.closeDeletePermissionModal = function () {
            $scope.deleteing_invoice_id = 0;
            jQuery.noConflict();
            (function ($) {
                $('#deleteInvoicePermissionModal').modal('hide');
            })(jQuery);
        };

        $scope.save_and_open_modal = function () {
            $scope.addPay();
            $timeout(function () {
                $scope.openAddModal();
                $scope.getNextFactorNumber('PAY');
            }, 1000);
        };

        $scope.resetFrom = function () {
            $scope.new_pay_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': '',
                'payment_amount': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };
        initialize();
    });