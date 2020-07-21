angular.module("dashboard")
    .controller("reportsCtrl", function ($scope, $rootScope, dashboardHttpRequest) {
        var initialize = function () {
            $scope.config_date_pickers();
            $scope.report_data = {
                report_category: "",
                start_date: "",
                end_date: "",
                suppliers: [],
                settlement_types: []
            };
            $scope.settlement_types = [
                {
                    id: "CASH",
                    name: "نقدی"
                },
                {
                    id: "CREDIT",
                    name: "اعتباری"
                },
                {
                    id: "AMANI",
                    name: "امانی"
                }
            ];
            $rootScope.is_page_loading = false;
            $scope.get_suppliers();
        };

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
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

        $scope.resetFrom = function () {
            $scope.report_data = {
                report_category: null
            };
        };

        $scope.config_date_pickers = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#start_date_picker").datepicker();
                    $("#end_date_picker").datepicker();
                });
            })(jQuery);
        };

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
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

        initialize();
    });