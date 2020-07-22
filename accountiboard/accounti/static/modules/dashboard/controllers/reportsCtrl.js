angular.module("dashboard")
    .controller("reportsCtrl", function ($scope, $rootScope, $state, dashboardHttpRequest) {
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

            $scope.invoice_types = [
                {
                    id: "INVOICE_SALE",
                    name: "فاکتور فروش"
                },
                {
                    id: "INVOICE_PURCHASE",
                    name: "فاکتور خرید"
                },
                {
                    id: "INVOICE_PAY",
                    name: "فاکتور پرداخت"
                },
                {
                    id: "INVOICE_EXPENSE",
                    name: "فاکتور هزینه"
                },
                {
                    id: "INVOICE_RETURN",
                    name: "فاکتور مرجوعی"
                }
            ];
            $rootScope.is_page_loading = false;
            $scope.get_suppliers();
            $scope.check_url_parameters();
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

        $scope.get_report = function () {
            dashboardHttpRequest.getReport('?type=' + $scope.report_data.report_category +
                '&start=' + $scope.report_data.start_date +
                '&end=' + $scope.report_data.end_date +
                '&suppliers=' + $scope.report_data.suppliers +
                '&s_types=' + $scope.report_data.settlement_types)
                .then(function (data) {
                    $scope.reports_result = data['results'];
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.check_url_parameters = function () {
            $scope.report_data.report_category = $state.params.type;
            $scope.report_data.start_date = $state.params.start;
            $scope.report_data.end_date = $state.params.end;
            $scope.report_data.suppliers = $state.params.suppliers;
            $scope.report_data.settlement_types = $state.params.s_types;
            if ($scope.report_data.report_category && $scope.report_data.start_date && $scope.report_data.end_date){
                $scope.get_report();
            }
        };

        $scope.change_url_params = function () {
            $state.go('account_manager.reports', {
                type: $scope.report_data.report_category,
                start: $scope.report_data.start_date = $("#start_date_picker").val(),
                end: $scope.report_data.end_date = $("#end_date_picker").val(),
                suppliers: $scope.report_data.suppliers,
                s_types: $scope.report_data.settlement_types
            }, {
                notify: false,
                reload: false,
                location: 'replace',
                inherit: true
            });
        };

        initialize();
    });