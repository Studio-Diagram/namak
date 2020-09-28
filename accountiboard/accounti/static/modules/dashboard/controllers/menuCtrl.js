angular.module("dashboard")
    .controller("menuCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.new_menu_category_data = {
                'menu_category_id': 0,
                'name': '',
                'kind': '',
                'printers_id': [],
                'branch_id': $rootScope.user_data.branch
            };
            $scope.searach_data_menu_category = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.new_menu_item_data = {
                'menu_item_id': 0,
                'name': '',
                'price': '',
                'menu_category_id': 0
            };
            $scope.searach_data_menu_item = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.printers = [];
            $scope.get_menu_item_data($rootScope.user_data);
            $scope.get_menu_category_data();
            $scope.get_printers_data();
        };

        $scope.get_printers_data = function () {
            dashboardHttpRequest.getPrinters($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.printers = data['printers'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;

                });
        };

        $scope.changePrinterCheckBox = function (is_checked, printer_id) {
            console.log("clicked");
            var index_of_printer_id = $scope.new_menu_category_data.printers_id.indexOf(printer_id);
            if (index_of_printer_id === -1) {
                $scope.new_menu_category_data.printers_id.push(printer_id);
            }
            else {
                $scope.new_menu_category_data.printers_id.splice(index_of_printer_id, 1);
            }
        };

        $scope.get_menu_category_data = function () {
            dashboardHttpRequest.getMenuCategories($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.menu_categories = data['menu_categories'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;

                });
        };

        $scope.get_menu_item_data = function (data) {
            dashboardHttpRequest.getMenuItems(data)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.menu_items = data['menu_items'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;

                });
        };

        $scope.closeAddMenuCategoryModal = function () {
            $rootScope.close_modal('addMenuCategoryModal');
            $scope.resetFrom();
        };

        $scope.addMenuCategory = function () {
            dashboardHttpRequest.addMenuCategory($scope.new_menu_category_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_menu_category_data();
                        $scope.resetFrom();
                        $scope.closeAddMenuCategoryModal();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });
        };

        $scope.editMenuCategory = function (menu_category_id) {
            var data = {
                branch: $rootScope.user_data.branch,
                menu_category_id: menu_category_id
            };
            dashboardHttpRequest.getMenuCategory(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.printers = data['menu_category']['printers'];
                        $scope.new_menu_category_data = {
                            'menu_category_id': data['menu_category']['id'],
                            'name': data['menu_category']['name'],
                            'kind': data['menu_category']['kind'],
                            'printers_id': data['menu_category']['printers_id'],
                            'branch_id': $rootScope.user_data.branch
                        };
                        $rootScope.open_modal('addMenuCategoryModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });

        };

        $scope.change_order = function (menu_cat_id, type) {
            var sending_data = {
                "menu_cat_id": menu_cat_id,
                "change_type": type,
                "branch_id": $rootScope.user_data.branch
            };
            dashboardHttpRequest.changeMenuCategoryOrder(sending_data)
                .then(function (data) {
                    $scope.get_menu_category_data();
                }, function (error) {

                });
        };

        $scope.addMenuItem = function () {
            dashboardHttpRequest.addMenuItem($scope.new_menu_item_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_menu_item_data($rootScope.user_data);
                        $scope.resetFrom();
                        $rootScope.close_modal('addMenuItemModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });
        };

        $scope.searchMenuItem = function () {
            if ($scope.searach_data_menu_item.search_word === '') {
                $scope.get_menu_item_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchMenuItem($scope.searach_data_menu_item)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.menu_items = data['menu_items'];
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {});
            }
        };


        $scope.editMenuItem = function (menu_item_id) {
            var data = {
                'menu_item_id': menu_item_id
            };
            dashboardHttpRequest.getMenuItem(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_menu_item_data = {
                            'menu_item_id': data['menu_item']['id'],
                            'name': data['menu_item']['name'],
                            'price': data['menu_item']['price'],
                            'menu_category_id': data['menu_item']['menu_category_id'],
                            'branch_id': $rootScope.user_data.branch
                        };
                        $rootScope.open_modal('addMenuItemModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });

        };

        $scope.deleteMenuItem = function (item_id) {
            dashboardHttpRequest.deleteMenuItem(item_id)
                .then(function (data) {
                    $scope.get_menu_item_data($rootScope.user_data);
                }, function (error) {

                });
        };

        $scope.resetFrom = function () {
            $scope.new_menu_category_data = {
                'menu_category_id': 0,
                'name': '',
                'kind': '',
                'printers_id': [],
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_menu_item_data = {
                'menu_item_id': 0,
                'name': '',
                'price': '',
                'menu_category_id': 0,
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch
            };
        };
        initialize();
    });