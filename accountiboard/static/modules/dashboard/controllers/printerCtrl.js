angular.module("dashboard")
    .controller("printerCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.new_printer_data = {
                'printer_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.get_printers_data($rootScope.user_data);
        };

        $scope.get_printers_data = function (data) {
            dashboardHttpRequest.getPrinters(data)
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

        $scope.resetFrom = function () {
            $scope.new_printer_data = {
                'printer_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        initialize();
    });