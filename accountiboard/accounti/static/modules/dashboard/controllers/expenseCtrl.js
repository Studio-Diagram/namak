angular.module("dashboard")
    .controller("expenseCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.set_today_for_invoice();
            $scope.new_invoice_expense_data = {
                'id': 0,
                'factor_number': 0,
                'expense_id': 0,
                'expense_kind': '',
                'expense_tags': [],
                'supplier_id': 0,
                'services': [
                    {
                        'service_name': '',
                        'price': 0,
                        'description': ''
                    }
                ],
                'total_price': 0,
                'settlement_type': '',
                'tax': 0,
                'discount': 0,
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': ''
            };
            $scope.search_data_expense = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };
            $scope.headers = [
                {
                    name: "شماره فاکتور",
                    key: "factor_number"
                },
                {
                    name: "طرف حساب",
                    key: "supplier_name"
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
                    name: "مبلغ هزینه",
                    key: "total_price"
                },
                {
                    name: "تاریخ",
                    key: "date"
                }
            ];
            $scope.search_data_tags = {
                'search_word': ''
            };
            $scope.table_config = {
                price_fields: ["payment_amount"],
                has_detail_button: false,
                has_delete_button: true,
                has_row_numbers: false
            };
            $scope.get_all_expense_tags();
            $scope.get_expenses();
            $scope.get_suppliers();
            $scope.get_banking_data();
            $scope.get_stocks_data();
        };

        $scope.compare_before_exit = function () {
            return angular.toJson($scope.first_initial_value_of_invoice_expense) === angular.toJson($scope.new_invoice_expense_data);
        };

        $scope.search_tags = function () {
            $scope.expense_tags = $filter('filter')($scope.expense_tags_original, {'name': $scope.search_data_tags.search_word});
        };

        $scope.add_tag = function (tag_id, tag_name) {
            var already_added = false;
            if (!tag_id) {
                $scope.new_invoice_expense_data.expense_tags.push({
                    name: tag_name
                });
                return true
            }
            $scope.new_invoice_expense_data.expense_tags.forEach(function (item) {
                if (item.id === tag_id) {
                    already_added = true;
                }
            });
            if (!already_added) {
                $scope.new_invoice_expense_data.expense_tags.push({
                    id: tag_id,
                    name: tag_name
                });
                return true;
            }
            else {
                return false;
            }
        };

        $scope.add_tag_after_enter = function () {
            for (var index = 0; index < $scope.expense_tags_original.length; index++) {
                var item = $scope.expense_tags_original[index];
                if (item.name === $scope.search_data_tags.search_word) {
                    if ($scope.add_tag(item.id, item.name)) {
                        $scope.search_data_tags.search_word = "";
                    }
                    return true
                }
            }
            for (var index_t = 0; index_t < $scope.new_invoice_expense_data.expense_tags.length; index_t++) {
                var element = $scope.new_invoice_expense_data.expense_tags[index_t];
                if (element.name === $scope.search_data_tags.search_word) {
                    return true
                }
            }
            if ($scope.search_data_tags.search_word) {
                $scope.add_tag(0, $scope.search_data_tags.search_word);
                $scope.search_data_tags.search_word = "";
            }
        };

        $scope.delete_tag = function (tag_index) {
            $scope.new_invoice_expense_data.expense_tags.splice(tag_index, 1);
        };

        $scope.set_today_for_invoice = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    var date = new Date();
                    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                    $("#datepicker").datepicker();
                    $('#datepicker').datepicker('setDate', today);
                });
            })(jQuery);
        };

        $scope.get_all_expense_tags = function () {
            dashboardHttpRequest.getAllExpenseTags($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.expense_tags = data['tags'];
                        $scope.expense_tags_original = data['tags'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.loadTags = function ($query) {
            return $scope.expense_tags.filter(function (tag) {
                return tag.name.toLowerCase().indexOf($query.toLowerCase()) !== -1;
            });
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
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.addExpense = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_invoice_expense_data.date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addExpense($scope.new_invoice_expense_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_expenses();
                        $scope.get_all_expense_tags();
                        $scope.resetFrom();
                        $rootScope.close_modal('addModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.delete_invoice_expense = function (invoice_id) {
            dashboardHttpRequest.deleteInvoiceExpense(invoice_id)
                .then(function (data) {
                    $scope.get_expenses();
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.searchExpense = function () {
            if ($scope.search_data_expense.search_word === '') {
                $scope.get_expenses();
            }
            else {
                dashboardHttpRequest.searchExpense($scope.search_data_expense)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.expenses = data['expenses'];
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {
                        $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                    });
            }
        };

        $scope.get_expenses = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getAllExpenses(data)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.expenses = data['invoices'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.deleteNewItem = function (item_index) {
            $scope.new_invoice_expense_data.services.splice(item_index, 1);
        };

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_expense_data.factor_number = data['next_factor_number'];
                        $scope.first_initial_value_of_invoice_expense = angular.copy($scope.new_invoice_expense_data);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBankingByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    $scope.allbanking_names = [];
                    data['bank'].forEach(function (bank) {
                        $scope.allbanking_names.push({'id': bank.id, 'name': bank.name});
                    });

                    data['tankhah'].forEach(function (tankhah) {
                        $scope.allbanking_names.push({'id': tankhah.id, 'name': tankhah.name});
                    });

                    data['cash_register'].forEach(function (cash_register) {
                        $scope.allbanking_names.push({'id': cash_register.id, 'name': cash_register.name});
                    });

                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_stocks_data = function () {
            dashboardHttpRequest.getStockByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    angular.copy($rootScope.user_data.branches, $scope.branches);
                    $scope.stocks = data['stocks'];

                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.resetFrom = function () {
            $scope.new_invoice_expense_data = {
                'id': 0,
                'factor_number': 0,
                'expense_id': 0,
                'expense_kind': '',
                'expense_tags': [],
                'supplier_id': 0,
                'services': [
                    {
                        'service_name': '',
                        'price': 0,
                        'description': ''
                    }
                ],
                'total_price': 0,
                'settlement_type': '',
                'tax': 0,
                'discount': 0,
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': ''
            };
        };

        $scope.change_total_price = function () {
            $scope.new_invoice_expense_data.total_price = 0;
            for (var i = 0; i < $scope.new_invoice_expense_data.services.length; i++) {
                $scope.new_invoice_expense_data.total_price += Number($scope.new_invoice_expense_data.services[i].price);
            }

            $scope.new_invoice_expense_data.total_price = Number($scope.new_invoice_expense_data.total_price) + Number($scope.new_invoice_expense_data.tax) - Number($scope.new_invoice_expense_data.discount);
        };

        $scope.add_new_row_to_services = function () {
            $scope.new_invoice_expense_data.services.push({
                'service_name': '',
                'price': 0,
                'description': ''
            });
        };

        $scope.save_and_open_modal = function () {
            $scope.addExpense();
            $timeout(function () {
                $scope.set_today_for_invoice();
                $rootScope.open_modal('addModal');
                $scope.getNextFactorNumber('EXPENSE');
            }, 1000);
        };

        initialize();
    });