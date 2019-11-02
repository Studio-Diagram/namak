angular.module("dashboard")
    .controller("menuCategoryCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode_menu_category = false;
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
            $scope.printers = [];
            $scope.error_message = "";
            $scope.get_printers_data($rootScope.user_data);
            $scope.get_menu_category_data($rootScope.user_data);
        };

        $scope.changePrinterCheckBox = function (is_checked, printer_id) {
            if (is_checked) {
                $scope.new_menu_category_data.printers_id.push(printer_id);
            }
            else {
                for (var i = 0; i < $scope.new_menu_category_data.printers_id.length; i++) {
                    if ($scope.new_menu_category_data.printers_id[i] === printer_id) {
                        $scope.new_menu_category_data.printers_id.splice(i, 1);
                    }
                }
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

        $scope.get_printers_data = function (data) {
            dashboardHttpRequest.getPrinters(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.printers = data['printers'];
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
                $('#addMenuCategoryModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addMenuCategoryModal').css('z-index', "");
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
                $scope.get_printers_data($rootScope.user_data);
            })(jQuery);
        };

        $scope.addMenuCategory = function () {
            if ($scope.is_in_edit_mode_menu_category) {
                $scope.is_in_edit_mode_menu_category = false;
                dashboardHttpRequest.addMenuCategory($scope.new_menu_category_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_menu_category_data($rootScope.user_data);
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
            }
            else {
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
            }
        };

        $scope.searchMenuCategory = function () {
            if ($scope.searach_data_menu_category.search_word === '') {
                $scope.get_menu_category_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchMenuCategory($scope.searach_data_menu_category)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.menu_categories = data['menu_categories'];
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


        $scope.editMenuCategory = function (menu_category_id) {
            $scope.is_in_edit_mode_menu_category = true;
            var data = {
                'username': $rootScope.user_data.username,
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

        $scope.resetFrom = function () {
            $scope.new_menu_category_data = {
                'menu_category_id': 0,
                'name': '',
                'kind': '',
                'printers_id': [],
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };
        initialize();
    });