angular.module("dashboard")
    .controller("accountManagerCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $scope.is_in_edit_mode_supplier = false;
            $scope.error_message = '';
            $scope.new_supplier_data = {
                'id': 0,
                'name': '',
                'phone': '',
                'salesman_name': '',
                'salesman_phone': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_supplier = {
                'search_word': '',
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch
            };
            $scope.is_in_edit_mode_supplier = false;
            $scope.get_suppliers();
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
            $scope.closePermissionModal();
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('hide');
                $scope.resetFrom();
            })(jQuery);
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

        $scope.addSupplier = function () {
            if ($scope.is_in_edit_mode_supplier) {
                $scope.is_in_edit_mode_supplier = false;
                dashboardHttpRequest.addSupplier($scope.new_supplier_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_suppliers();
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
            }
            else {
                dashboardHttpRequest.addSupplier($scope.new_supplier_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_suppliers();
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
            }
        };

        $scope.searchSupplier = function () {
            if ($scope.search_data_supplier.search_word === '') {
                $scope.get_suppliers();
            }
            else {
                dashboardHttpRequest.searchSupplier($scope.search_data_supplier)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.suppliers = data['suppliers'];
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

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
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

        $scope.editSupplier = function (supplier_id) {
            $scope.is_in_edit_mode_supplier = true;            
            dashboardHttpRequest.getSupplier(supplier_id)
                .then(function (data) {
                    $scope.new_supplier_data = {
                            'id': data['supplier']['id'],
                            'name': data['supplier']['name'],
                            'phone': data['supplier']['phone'],
                            'salesman_name': data['supplier']['salesman_name'],
                            'salesman_phone': data['supplier']['salesman_phone'],
                            'branch_id': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openAddModal();
                }, function (error) {
                    $scope.error_message = data['error_msg'];
                    $scope.openErrorModal();
                });

        };

        $scope.deleteSupplier = function (supplier_id) {
            dashboardHttpRequest.deleteSupplier(supplier_id)
                .then(function (data) {
                    $scope.get_suppliers();
                }, function (error) {
                    $scope.error_message = error.data.error_msg;
                    $scope.openErrorModal();
                });
        };

        $scope.resetFrom = function () {
            $scope.new_supplier_data = {
                'id': 0,
                'name': '',
                'phone': '',
                'salesman_name': '',
                'salesman_phone': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };
        initialize();
    });