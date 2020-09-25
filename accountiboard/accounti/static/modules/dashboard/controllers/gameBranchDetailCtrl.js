angular.module("dashboard")
    .controller("gameBranchDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.game_branch_data = {
                guest_pricing: false,
                min_paid_price: 5000,
                game_data: [
                    {
                        "which_hour": 1,
                        "price_per_hour": 0
                    },
                    {
                        "which_hour": 2,
                        "price_per_hour": 0
                    }
                ]
            };
            $scope.get_branch_data();
        };

        $scope.get_branch_data = function () {
            dashboardHttpRequest.getBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.setDefaultData(data.branch);
                    $scope.show_game_branch_data = data.branch;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                });
        };

        $scope.updateBranch = function () {
            dashboardHttpRequest.updateBranch($rootScope.user_data.branch, $scope.game_branch_data)
                .then(function (data) {
                    $scope.setDefaultData(data.branch);
                    $scope.show_game_branch_data = data.branch;
                    $scope.close_modal('editGameDetailsModal');
                }, function (error) {});
        };

        $scope.setDefaultData = function (data) {
            $scope.game_branch_data.guest_pricing = data.guest_pricing;
            $scope.game_branch_data.min_paid_price = data.min_paid_price;
            $scope.game_branch_data.game_data = angular.copy(data.game_data);
        };

        initialize();
    });