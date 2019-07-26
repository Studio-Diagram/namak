angular.module("dashboard")
    .controller("tableCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_table_data = {
                'table_id': 0,
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
                            $scope.closeAddEmployeeModal();
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

        $scope.resetFrom = function () {
            $scope.new_table_data = {
                'table_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddTableModal();
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

        initialize();
    });