angular.module("dashboard")
    .controller("tableCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.new_table_data = {
                'table_id': 0,
                'table_cat_id': '',
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
            $scope.get_tables_data($rootScope.user_data);
            $scope.get_table_categories_data($rootScope.user_data);
        };

        $scope.get_tables_data = function (data) {
            dashboardHttpRequest.getTables(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.tables = data['tables'];
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

        $scope.addTable = function () {
            dashboardHttpRequest.addTable($scope.new_table_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_tables_data($rootScope.user_data);
                        $scope.resetFrom();
                        $rootScope.close_modal('addModal');
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

        $scope.addTableCategory = function () {
            dashboardHttpRequest.addTableCategory($scope.new_table_category_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_table_categories_data($rootScope.user_data);
                        $rootScope.close_modal('addModalTableCategory');
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
                        $scope.open_modal('addModal');
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
                        $rootScope.open_modal('addModalTableCategory');
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
                'table_cat_id': '',
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
            $rootScope.close_modal('addModal');
            $rootScope.close_modal('addModalTableCategory');
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