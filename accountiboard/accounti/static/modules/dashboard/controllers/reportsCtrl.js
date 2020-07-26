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
            $scope.headers = {
                INVOICE_SALE: [
                    {
                        name: "شماره فاکتور",
                        key: "id"
                    },
                    {
                        name: "قیمت کل",
                        key: "price"
                    },
                    {
                        name: "تاریخ ساخت",
                        key: "created_time"
                    }
                ],
                INVOICE_EXPENSE: [
                    {
                        name: "شماره فاکتور",
                        key: "id"
                    },
                    {
                        name: "قیمت کل",
                        key: "price"
                    },
                    {
                        name: "تاریخ ساخت",
                        key: "created_time"
                    },
                    {
                        name: "تامین‌کننده",
                        key: "supplier"
                    },
                    {
                        name: "دسته‌بندی",
                        key: "expense_category"
                    },
                    {
                        name: "نوع پرداخت",
                        key: "settlement_type"
                    }
                ],
                INVOICE_PAY: [
                    {
                        name: "شماره فاکتور",
                        key: "id"
                    },
                    {
                        name: "قیمت کل",
                        key: "price"
                    },
                    {
                        name: "تاریخ ساخت",
                        key: "created_time"
                    },
                    {
                        name: "تامین‌کننده",
                        key: "supplier"
                    },
                    {
                        name: "نوع پرداخت",
                        key: "settle_type"
                    },
                    {
                        name: "شماره ارجاع",
                        key: "backup_code"
                    }
                ],
                INVOICE_PURCHASE: [
                    {
                        name: "شماره فاکتور",
                        key: "id"
                    },
                    {
                        name: "قیمت کل",
                        key: "price"
                    },
                    {
                        name: "تاریخ ساخت",
                        key: "created_time"
                    },
                    {
                        name: "تامین‌کننده",
                        key: "supplier"
                    },
                    {
                        name: "نوع فاکتور",
                        key: "settlement_type"
                    }
                ],
                INVOICE_RETURN: [
                    {
                        name: "شماره فاکتور",
                        key: "id"
                    },
                    {
                        name: "قیمت کل",
                        key: "price"
                    },
                    {
                        name: "تاریخ ساخت",
                        key: "created_time"
                    },
                    {
                        name: "تامین‌کننده",
                        key: "supplier"
                    },
                    {
                        name: "نام محصول",
                        key: "shop_name"
                    },
                    {
                        name: "تعداد",
                        key: "numbers"
                    },
                    {
                        name: "توضیحات",
                        key: "description"
                    },
                    {
                        name: "نوع مرجوعی",
                        key: "return_type"
                    }
                ]
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
                    id: "AMANi",
                    name: "امانی"
                }
            ];

            $scope.invoice_types = [
                {
                    id: "INVOICE_SALE",
                    name: "فاکتور فروش",
                    price_fields: ["price"]
                },
                {
                    id: "INVOICE_PURCHASE",
                    name: "فاکتور خرید",
                    price_fields: ["price"]
                },
                {
                    id: "INVOICE_PAY",
                    name: "فاکتور پرداخت",
                    price_fields: ["price"]
                },
                {
                    id: "INVOICE_EXPENSE",
                    name: "فاکتور هزینه",
                    price_fields: ["price"]
                },
                {
                    id: "INVOICE_RETURN",
                    name: "فاکتور مرجوعی",
                    price_fields: ["price"]
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
            let starting_date = $("#start_date_picker").val() ? $("#start_date_picker").val() : $state.params.start;
            let ending_date = $("#end_date_picker").val() ? $("#end_date_picker").val() : $state.params.end;
            dashboardHttpRequest.getReport('?type=' + $scope.report_data.report_category +
                '&start=' + starting_date +
                '&end=' + ending_date +
                '&suppliers=' + $scope.report_data.suppliers +
                '&s_types=' + $scope.report_data.settlement_types)
                .then(function (data) {
                    $scope.selected_table_report_category = $scope.report_data.report_category;
                    $scope.reports_result = data;
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.check_url_parameters = function () {
            $scope.report_data.report_category = $state.params.type;
            $scope.report_data.start_date = $state.params.start;
            $scope.report_data.end_date = $state.params.end;
            if (Array.isArray($state.params.suppliers)) {
                $scope.report_data.suppliers = $state.params.suppliers.map(Number)
            }
            else {
                if ($state.params.suppliers) {
                    $scope.report_data.suppliers.push(parseInt($state.params.suppliers))
                }
            }
            if (Array.isArray($state.params.s_types)) {
                $scope.report_data.settlement_types = $state.params.s_types
            }
            else {
                console.log($state.params.s_types);
                if ($state.params.s_types) {
                    $scope.report_data.settlement_types.push($state.params.s_types);
                }
            }
            if ($scope.report_data.report_category && $scope.report_data.start_date && $scope.report_data.end_date) {
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

        $scope.showInvoicePurchase = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.invoice_purchase_data = data['invoice'];
                        $rootScope.open_modal('show_invoice_purchase');
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

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
        };

        initialize();
    });