angular.module("dashboard")
    .controller("tableCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_table_data = {
                'table_id': 0,
                'table_cat_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_table_category_data = {
                'id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_table = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.tableSearchWord = '';
            $scope.get_tables_data($rootScope.user_data);
            $scope.get_table_categories_data($rootScope.user_data);
        };

        $scope.get_tables_data = function (data) {
            dashboardHttpRequest.getTables(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.tables = data['tables'];
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

        $scope.get_table_categories_data = function (data) {
            dashboardHttpRequest.getTableCategories(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.table_categories = data['table_categories'];
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

        $scope.openAddTableModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddTableModal = function () {
            $scope.resetFrom();
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('hide');
            })(jQuery);
        };

        $scope.openAddTableCategoryModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addModalTableCategory').modal('show');
            })(jQuery);
        };

        $scope.closeAddTableCategoryModal = function () {
            $scope.resetFrom();
            jQuery.noConflict();
            (function ($) {
                $('#addModalTableCategory').modal('hide');
            })(jQuery);
        };

        $scope.addTable = function () {
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addTable($scope.new_table_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_tables_data($rootScope.user_data);
                            $scope.closeAddTableModal();
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
                dashboardHttpRequest.addTable($scope.new_table_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_tables_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddTableModal();
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

        $scope.addTableCategory = function () {
            dashboardHttpRequest.addTableCategory($scope.new_table_category_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_table_categories_data($rootScope.user_data);
                        $scope.get_tables_data($rootScope.user_data);
                        $scope.closeAddTableCategoryModal();
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

        $scope.searchTable = function () {
            if ($scope.search_data_table.search_word === '') {
                $scope.get_tables_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchTable($scope.search_data_table)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.tables = data['tables'];
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

        $scope.getTable = function (table_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'table_id': table_id
            };
            dashboardHttpRequest.getTable(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['table'];
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


        $scope.getTableCategory = function (table_category_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'table_cat_id': table_category_id
            };
            dashboardHttpRequest.getTableCategory(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['table_category'];
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


        $scope.editTable = function (table_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
                'table_id': table_id
            };
            dashboardHttpRequest.getTable(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_table_data = {
                            'table_id': data['table']['table_id'],
                            'name': data['table']['table_name'],
                            'table_cat_id': data['table']['table_cat_id']
                        };
                        $scope.openAddTableModal();
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

        $scope.editTableCategory = function (table_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'table_cat_id': table_id
            };
            dashboardHttpRequest.getTableCategory(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_table_category_data['id'] = data['table_category']['id'];
                        $scope.new_table_category_data['name'] = data['table_category']['name'];
                        $scope.openAddTableCategoryModal();
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
            $scope.new_table_data = {
                'table_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_table_category_data = {
                'id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddTableModal();
            $scope.closeAddTableCategoryModal();
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addModal').css('z-index', 1000);
                $('#addModalTableCategory').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addModal').css('z-index', "");
                $('#addModalTableCategory').css('z-index', "");
            })(jQuery);
        };

        initialize();
    });