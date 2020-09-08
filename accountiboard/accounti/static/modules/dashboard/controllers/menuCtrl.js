angular.module("dashboard")
    .controller("menuCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.new_menu_category_data = {
                'menu_category_id': 0,
                'name': '',
                'kind': '',
                'printers_id': [],
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.searach_data_menu_category = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_menu_item_data = {
                'menu_item_id': 0,
                'name': '',
                'price': '',
                'menu_category_id': 0,
                'username': $rootScope.user_data.username
            };
            $scope.searach_data_menu_item = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_printer_data = {
                'printer_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch
            };
            $scope.printers = [];
            $scope.error_message = "";

            $scope.get_menu_item_data($rootScope.user_data);
            $scope.get_menu_category_data($rootScope.user_data);
            $scope.get_printers_data();
        };

        $scope.get_printers_data = function () {
            dashboardHttpRequest.getPrinters($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.printers = data['printers'];
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

        $scope.addPrinter = function () {
            dashboardHttpRequest.addPrinter($scope.new_printer_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_printers_data($rootScope.user_data);
                        $scope.resetFrom();
                        $rootScope.close_modal('addPrinterModal');
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $rootScope.open_modal('errorModal', 'addPrinterModal');
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $rootScope.open_modal('errorModal', 'addPrinterModal');
                });
        };

        $scope.editPrinter = function (printer_id) {
            dashboardHttpRequest.getPrinter(printer_id)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_printer_data = data['printer'];
                        $rootScope.open_modal('addPrinterModal');
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

        $scope.changePrinterCheckBox = function (is_checked, printer_id) {
            var index_of_printer_id = $scope.new_menu_category_data.printers_id.indexOf(printer_id);
            if (index_of_printer_id === -1) {
                $scope.new_menu_category_data.printers_id.push(printer_id);
            }
            else {
                $scope.new_menu_category_data.printers_id.splice(index_of_printer_id, 1);
            }
        };

        $scope.get_menu_category_data = function (data) {
            dashboardHttpRequest.getMenuCategories(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.menu_categories = data['menu_categories'];
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

        $scope.get_menu_item_data = function (data) {
            dashboardHttpRequest.getMenuItems(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.menu_items = data['menu_items'];
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

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addMenuCategoryModal').css('z-index', 1000);
                $('#addMenuItemModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addMenuCategoryModal').css('z-index', "");
                $('#addMenuItemModal').css('z-index', "");
            })(jQuery);
        };

        $scope.openAddMenuCategoryModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addMenuCategoryModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddMenuCategoryModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addMenuCategoryModal').modal('hide');
                $scope.resetFrom();
            })(jQuery);
        };

        $scope.addMenuCategory = function () {
            dashboardHttpRequest.addMenuCategory($scope.new_menu_category_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_menu_category_data($rootScope.user_data);
                        $scope.resetFrom();
                        $scope.closeAddMenuCategoryModal();
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

        $scope.editMenuCategory = function (menu_category_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch,
                'menu_category_id': menu_category_id
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
                            'branch_id': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openAddMenuCategoryModal();
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

        $scope.change_order = function (menu_cat_id, type) {
            var sending_data = {
                "menu_cat_id": menu_cat_id,
                "change_type": type,
                "username": $rootScope.user_data.username
            };
            dashboardHttpRequest.changeMenuCategoryOrder(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_menu_category_data($rootScope.user_data);
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

        $scope.addMenuItem = function () {
            dashboardHttpRequest.addMenuItem($scope.new_menu_item_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_menu_item_data($rootScope.user_data);
                        $scope.resetFrom();
                        $rootScope.close_modal('addMenuItemModal');
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
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
        };


        $scope.editMenuItem = function (menu_item_id) {
            var data = {
                'username': $rootScope.user_data.username,
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
                            'branch_id': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        $rootScope.open_modal('addMenuItemModal');
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

        $scope.deleteMenuItem = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'menu_item_id': $scope.menu_item_wants_deleted
            };
            dashboardHttpRequest.deleteMenuItem(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_menu_item_data($rootScope.user_data);
                        $scope.closeDeleteConfirmModal();
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

        $scope.openDeleteConfirmModal = function (menu_item_id) {
            $scope.menu_item_wants_deleted = menu_item_id;
            jQuery.noConflict();
            (function ($) {
                $('#deleteConfirm').modal('show');
            })(jQuery);
        };

        $scope.closeDeleteConfirmModal = function () {
            $scope.menu_item_wants_deleted = 0;
            jQuery.noConflict();
            (function ($) {
                $('#deleteConfirm').modal('hide');
            })(jQuery);
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
            $scope.new_printer_data = {
                'printer_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch
            };
        };
        initialize();
    });