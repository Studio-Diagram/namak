angular.module("dashboard")
    .controller("menuItemCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode_menu_item = false;
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
            $scope.get_menu_item_data($rootScope.user_data);
            $scope.get_menu_category_data($rootScope.user_data);
        };

        $scope.get_menu_category_data = function (data) {
            dashboardHttpRequest.getMenuCategories(data)
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

        $scope.openAddMenuItemModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addMenuItemModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddMenuItemModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addMenuItemModal').modal('hide');
            })(jQuery);
            $scope.resetFrom();
        };

        $scope.addMenuItemF = function () {
            if ($scope.is_in_edit_mode_menu_item) {
                $scope.is_in_edit_mode_menu_item = false;
                dashboardHttpRequest.addMenuItem($scope.new_menu_item_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_menu_item_data($rootScope.user_data);
                            $scope.closeAddMenuItemModal();
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
                dashboardHttpRequest.addMenuItem($scope.new_menu_item_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_menu_item_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddMenuItemModal();
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
            $scope.is_in_edit_mode_menu_item = true;
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
                        $scope.openAddMenuItemModal();
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

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addMenuItemModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addMenuItemModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
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