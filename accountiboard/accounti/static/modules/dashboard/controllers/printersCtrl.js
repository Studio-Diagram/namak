angular.module("dashboard")
    .controller("printersCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.new_printer_data = {
                'printer_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch
            };
            $scope.printers = [];
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

        $scope.addPrinter = function () {
            dashboardHttpRequest.addPrinter($scope.new_printer_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_printers_data($rootScope.user_data);
                        $scope.resetFrom();
                        $rootScope.close_modal('addPrinterModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {});
        };

        $scope.editPrinter = function (printer_id) {
            dashboardHttpRequest.getPrinter(printer_id)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_printer_data = data['printer'];
                        $rootScope.open_modal('addPrinterModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {});

        };

        $scope.resetFrom = function () {
            $scope.new_printer_data = {
                'printer_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch
            };
        };
        initialize();
    });