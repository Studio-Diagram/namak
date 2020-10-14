angular.module("dashboard")
    .controller("reportsCtrl", function ($scope, $rootScope, $state, dashboardHttpRequest) {
        var initialize = function () {
            $scope.reports_result = {
                total_invoices: 0,
                total_price: 0,
                results: []
            };
            $scope.config_date_pickers();
            $scope.report_data = {
                report_category: "",
                start_date: "",
                end_date: "",
                suppliers: [],
                settlement_types: [],
                employees: [],
                branch_id: $rootScope.user_data.branch
            };
            $scope.headers = {
                INVOICE_SALE: [
                    {
                        name: "شماره سند",
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
                        name: "شعبه",
                        key: "branch_name"
                    }
                ],
                INVOICE_EXPENSE: [
                    {
                        name: "شماره سند",
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
                        name: "طرف حساب",
                        key: "supplier"
                    },
                    {
                        name: "دسته‌بندی",
                        key: "expense_category"
                    },
                    {
                        name: "نوع پرداخت",
                        key: "settlement_type"
                    },
                    {
                        name: "شعبه",
                        key: "branch_name"
                    }
                ],
                INVOICE_PAY: [
                    {
                        name: "شماره سند",
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
                        name: "طرف حساب",
                        key: "supplier"
                    },
                    {
                        name: "نوع پرداخت",
                        key: "settle_type"
                    },
                    {
                        name: "شماره ارجاع",
                        key: "backup_code"
                    },
                    {
                        name: "شعبه",
                        key: "branch_name"
                    }
                ],
                INVOICE_PURCHASE: [
                    {
                        name: "شماره سند",
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
                        name: "طرف حساب",
                        key: "supplier"
                    },
                    {
                        name: "نوع فاکتور",
                        key: "settlement_type"
                    },
                    {
                        name: "شعبه",
                        key: "branch_name"
                    }
                ],
                INVOICE_RETURN: [
                    {
                        name: "شماره سند",
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
                        name: "طرف حساب",
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
                    },
                    {
                        name: "شعبه",
                        key: "branch_name"
                    }
                ],
                INVOICE_SALARY: [
                    {
                        name: "شماره سند",
                        key: "id"
                    },
                    {
                        name: "کارمند",
                        key: "employee"
                    },
                    {
                        name: "مبلغ کل",
                        key: "price"
                    },
                    {
                        name: "تاریخ پرداخت ",
                        key: "invoice_date"
                    },
                    {
                        name: "نوع پرداخت",
                        key: "settlement_type"
                    },
                    {
                        name: "شعبه",
                        key: "branch_name"
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

            $scope.invoice_type_configs = {
                INVOICE_SALE: {
                    price_fields: ["price"],
                    has_detail_button: false,
                    has_delete_button: false,
                    table_title: "فهرست تفکیکی"

                },
                INVOICE_PURCHASE: {
                    price_fields: ["price"],
                    has_detail_button: true,
                    has_delete_button: false,
                    table_title: "فهرست تفکیکی"
                },
                INVOICE_PAY: {
                    price_fields: ["price"],
                    has_detail_button: false,
                    has_delete_button: false,
                    table_title: "فهرست تفکیکی"
                },
                INVOICE_EXPENSE: {
                    price_fields: ["price"],
                    has_detail_button: false,
                    has_delete_button: false,
                    table_title: "فهرست تفکیکی"
                },
                INVOICE_RETURN: {
                    price_fields: ["price"],
                    has_detail_button: false,
                    has_delete_button: false,
                    table_title: "فهرست تفکیکی"
                },
                INVOICE_SALARY: {
                    price_fields: ["price"],
                    has_detail_button: false,
                    has_delete_button: false,
                    table_title: "فهرست تفکیکی"
                }
            };

            $scope.invoice_types = [
                {
                    id: "INVOICE_SALE",
                    name: "فروش"
                },
                {
                    id: "INVOICE_PURCHASE",
                    name: "خرید"
                },
                {
                    id: "INVOICE_EXPENSE",
                    name: "هزینه"
                },
                {
                    id: "INVOICE_PAY",
                    name: "پرداخت"
                },
                {
                    id: "INVOICE_SALARY",
                    name: "پرداخت حقوق"
                },
                {
                    id: "INVOICE_RETURN",
                    name: "مرجوعی"
                }
            ];
            $rootScope.is_page_loading = false;
            $scope.get_suppliers();
            $scope.check_url_parameters();
            $scope.get_employees_data($rootScope.user_data);
        };

        $scope.change_invoice_type_report = function (type) {
            jQuery.noConflict();
            (function ($) {
                $("#start_date_picker").val("");
                $("#end_date_picker").val("");
            })(jQuery);
            $scope.report_data = {
                report_category: "",
                start_date: "",
                end_date: "",
                suppliers: [],
                settlement_types: [],
                employees: [],
                branch_id: $rootScope.user_data.branch
            };
            $scope.reports_result = {
                total_invoices: 0,
                total_price: 0,
                results: []
            };
            $scope.report_data.report_category = type;
            $scope.change_url_params();
        };

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                });
        };

        $scope.get_report = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.starting_date = $("#start_date_picker").val() ? $("#start_date_picker").val() : $state.params.start;
                $scope.ending_date = $("#end_date_picker").val() ? $("#end_date_picker").val() : $state.params.end;
            })(jQuery);
            if (!$scope.report_data.report_category) $scope.report_data.report_category = "";
            dashboardHttpRequest.getReport('?type=' + $scope.report_data.report_category +
                '&start=' + $scope.starting_date +
                '&end=' + $scope.ending_date +
                '&suppliers=' + $scope.report_data.suppliers +
                '&s_types=' + $scope.report_data.settlement_types +
                '&employees=' + $scope.report_data.employees +
                '&branch=' + $scope.report_data.branch_id)
                .then(function (data) {
                    $scope.selected_table_report_category = $scope.report_data.report_category;
                    $scope.reports_result = data;
                }, function (error) {});
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
                if ($state.params.s_types) {
                    $scope.report_data.settlement_types.push($state.params.s_types);
                }
            }
            if (Array.isArray($state.params.employees)) {
                $scope.report_data.employees = $state.params.employees
            }
            else {
                if ($state.params.employees) {
                    $scope.report_data.employees.push(parseInt($state.params.employees));
                }
            }
            if ($scope.report_data.report_category && $scope.report_data.start_date && $scope.report_data.end_date) {
                $scope.get_report();
            }
        };

        $scope.change_url_params = function () {
            jQuery.noConflict();
            (function ($) {
                $state.go('dashboard.accounting.reports', {
                    type: $scope.report_data.report_category,
                    start: $scope.report_data.start_date = $("#start_date_picker").val(),
                    end: $scope.report_data.end_date = $("#end_date_picker").val(),
                    suppliers: $scope.report_data.suppliers,
                    s_types: $scope.report_data.settlement_types,
                    employees: $scope.report_data.employees
                }, {
                    notify: false,
                    reload: false,
                    location: 'replace',
                    inherit: true
                });
            })(jQuery);
        };

        $scope.showInvoicePurchase = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id
            };
            dashboardHttpRequest.getInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.invoice_purchase_data = data['invoice'];
                        $rootScope.open_modal('show_invoice_purchase');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                });
        };

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
        };
        $scope.get_employees_data = function (data) {
            dashboardHttpRequest.getEmployees(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.employees = data['employees'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                });
        };

        initialize();
    });