angular.module("dashboard")
    .controller("stockCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_stock_data = {
                'stock_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_stock = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.employeeSearchWord = '';
            $scope.get_stocks_data($rootScope.user_data);
        };

        $scope.get_stocks_data = function (data) {
            dashboardHttpRequest.getStocks(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.stocks = data['stocks'];
                    }
                    else if (data['response_code'] === 3) {
                        console.log("NOT SUCCESS!");
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        $scope.openAddStockModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addStockModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddStockModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addStockModal').modal('hide');
            })(jQuery);
        };

        $scope.addStock = function () {
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addStock($scope.new_stock_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_stocks_data($rootScope.user_data);
                            $scope.closeAddStockModal();
                        }
                        else if (data['response_code'] === 3) {
                            console.log("NOT SUCCESS!");
                        }
                    }, function (error) {
                        console.log(error);
                    });
            }
            else {
                dashboardHttpRequest.addStock($scope.new_stock_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_employees_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddEmployeeModal();
                        }
                        else if (data['response_code'] === 3) {
                            console.log("NOT SUCCESS!");
                        }
                    }, function (error) {
                        console.log(error);
                    });
            }
        };

        $scope.searchStock = function () {
            if ($scope.search_data_stock.search_word === '') {
                $scope.get_stocks_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchStock($scope.search_data_stock)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.stocks = data['stocks'];
                        }
                        else if (data['response_code'] === 3) {
                            console.log("NOT SUCCESS!");
                        }
                    }, function (error) {
                        console.log(error);
                    });
            }
        };

        $scope.getStock = function (stock_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'stock_id': stock_id
            };
            dashboardHttpRequest.getStock(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['employee'];
                    }
                    else if (data['response_code'] === 3) {
                        console.log("NOT SUCCESS!");
                    }
                }, function (error) {
                    console.log(error);
                });
        };


        $scope.editStock = function (stock_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
                'stock_id': stock_id
            };
            dashboardHttpRequest.getStock(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_stock_data = {
                            'stock_id': data['stock']['id'],
                            'name': data['stock']['name'],
                            'category': data['stock']['category'],
                            'min_players': data['stock']['min_players'],
                            'max_players': data['stock']['max_players'],
                            'best_players': data['stock']['best_players'],
                            'rate': data['stock']['rate'],
                            'learning_time': data['stock']['learning_time'],
                            'duration': data['stock']['duration'],
                            'image_name': data['stock']['image_name'],
                            'image_path': data['stock']['image_path'],
                            'description': data['stock']['description'],
                            'bgg_code': data['stock']['bgg_code'],
                        };
                        $('#customFile').next('.custom-file-label').html($scope.new_stock_data.image_name);
                        $scope.openAddStockModal();
                    }
                    else if (data['response_code'] === 3) {
                        console.log("NOT SUCCESS!");
                    }
                }, function (error) {
                    console.log(error);
                });

        };

        $scope.resetFrom = function () {
            $scope.new_stock_data = {
                'stock_id': 0,
                'name': '',
                'category': '',
                'min_players': '',
                'max_players': '',
                'best_players': '',
                'rate': 1,
                'learning_time': '',
                'duration': '',
                'image_name': '',
                'image_path': '',
                'description': '',
                'bgg_code': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $('#customFile').next('.custom-file-label').html("Choose File");

        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddStockModal();
        };
        initialize();
    });