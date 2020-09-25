angular.module("dashboard")
    .controller("accountManagerCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $scope.is_in_edit_mode_supplier = false;
            $scope.new_supplier_data = {
                'id': 0,
                'name': '',
                'phone': '',
                'salesman_name': '',
                'salesman_phone': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.search_data_supplier = {
                'search_word': '',
                'branch': $rootScope.user_data.branch
            };
            $scope.headers = [
                {
                    name: "عنوان",
                    key: "name"
                },
                {
                    name: "مسول فروش",
                    key: "salesman_name"
                },
                {
                    name: "شماره تماس",
                    key: "salesman_phone"
                },
                {
                    name: "مانده حساب",
                    key: "remainder"
                }
            ];
            $scope.table_config = {
                price_fields: ["remainder"],
                has_detail_button: true,
                has_second_button_on_right_side: true,
                has_delete_button: true,
                has_row_numbers: false,
                right_side_button_text: "ویرایش",
                price_with_tags: true
            };
            $scope.is_in_edit_mode_supplier = false;
            $scope.get_suppliers();
        };

        $scope.go_to_supplier_detail = function (supplier_id) {
            $state.go('dashboard.accounting.supplier', {supplier: supplier_id})
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
                $('#addModal').modal('hide');
                $scope.resetFrom();
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
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
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
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
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
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
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
                        'branch_id': $rootScope.user_data.branch
                    };
                    $scope.openAddModal();
                });

        };

        $scope.deleteSupplier = function (item_id) {
            dashboardHttpRequest.deleteSupplier(item_id)
                .then(function (data) {
                    $scope.get_suppliers();
                }, function (error) {});
        };

        $scope.resetFrom = function () {
            $scope.new_supplier_data = {
                'id': 0,
                'name': '',
                'phone': '',
                'salesman_name': '',
                'salesman_phone': '',
                'branch_id': $rootScope.user_data.branch
            };
        };

        initialize();
    });