angular.module("dashboard")
    .controller("stocksCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.new_stocks_data = {
                'id': 0,
                'branches':[],
                'name': ''
            };
            $scope.get_stocks_data();
            $scope.get_branches_data();
            angular.copy($rootScope.user_data.branches, $scope.new_stocks_data.branches);
            $scope.table_headers = [
                {
                    name: "نام انبار",
                    key: "name"
                },
                {
                    name: "شعبه",
                    key: "branches_names"
                }
            ];
            $scope.table_config = {has_detail_button: true, price_fields: [],has_delete_button: false,};
        };

        $scope.get_stocks_data = function () {
            dashboardHttpRequest.getStocks()
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    angular.copy($rootScope.user_data.branches, $scope.branches);
                    $scope.stocks = data['stocks'];

                    for (var i = $scope.stocks.length - 1; i >= 0; i--) {
                        $scope.stocks[i].branches_names = [];
                        for (var j = $scope.stocks[i].branches.length - 1; j >= 0; j--) {
                            for (var k = $rootScope.user_data.branches.length - 1; k >= 0; k--) {
                                if ($rootScope.user_data.branches[k].id == $scope.stocks[i].branches[j]) {
                                    $scope.stocks[i].branches_names.push($rootScope.user_data.branches[k].name);
                                }
                            }
                        }
                        $scope.stocks[i].branches_names = $scope.stocks[i].branches_names.join('، ');
                    }

                }, function (error) {
                    $rootScope.is_page_loading = false;

                });
        };

        $scope.addStock = function () {
            if ($scope.new_stocks_data.id === 0) {
                dashboardHttpRequest.addStock($scope.new_stocks_data)
                    .then(function (data) {
                        $scope.get_stocks_data();
                        $scope.resetFrom();
                        $rootScope.close_modal('addStockModal');
                        
                    }, function (error) {});
            } else {
                dashboardHttpRequest.updateStockDetail($scope.new_stocks_data.id, $scope.new_stocks_data)
                    .then(function (data) {
                        $scope.get_stocks_data();
                        $scope.resetFrom();
                        $rootScope.close_modal('addStockModal');
                        
                    }, function (error) {});
            }

        };

        $scope.editStock = function (stock_id) {
            dashboardHttpRequest.getStockDetail(stock_id)
                .then(function (data) {
                    // $scope.new_stocks_data.branches = data.branches;
                    // $scope.new_stocks_data.branches = $scope.branches;
                    $scope.new_stocks_data = {
                        'branches':$scope.branches,
                        'name': '',
                    };
                    angular.copy($rootScope.user_data.branches, $scope.new_stocks_data.branches);


                    var branches = data['branches'];
                    branches.forEach(function (branch_id) {
                        $scope.new_stocks_data.branches.forEach(function (branch) {
                            if (branch_id === branch.id) {
                                branch.is_checked = 1;
                                branch.is_checked_m = 1;
                            }
                        })
                    });
                    
                    $scope.new_stocks_data.id = data.id;
                    $scope.new_stocks_data.name = data.name;
                    $rootScope.open_modal('addStockModal');
                }, function (error) {});

        };

        $scope.changeStockBranchCheckBox = function (branch_id) {
            $scope.new_stocks_data.branches.forEach(function (branch) {
                if (branch_id === branch.id) {
                    if (branch.is_checked === 1) {
                        branch.is_checked = 0;
                        branch.is_checked_m = 0;
                    }
                    else {
                        branch.is_checked = 1;
                        branch.is_checked_m = 1;
                    }
                }
            });
        };

        $scope.clearStockBranchesCheckboxes = function () {
            $scope.branches.forEach(function (branch) {
                branch.is_checked = 0;
                branch.is_checked_m = 0;
            });
        };

        $scope.get_branches_data = function () {
            dashboardHttpRequest.getBranches($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.branches = data['branches'];
                        $scope.new_stocks_data.branches = $scope.branches;
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

                });
        };

        $scope.closeaddStockModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addStockModal').modal('hide');
                $scope.resetFrom();
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_stocks_data = {
                'id': 0,
                'branches':[],
                'name': ''
            };
            $scope.clearStockBranchesCheckboxes();
            angular.copy($rootScope.user_data.branches, $scope.new_stocks_data.branches);
        };

        initialize();
    });