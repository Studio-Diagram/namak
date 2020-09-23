angular.module("dashboard")
    .controller("salonCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, $stateParams, $state, dashboardHttpRequest, offlineAPIHttpRequest, $auth) {
        var initialize = function () {
            $scope.static_guest_name = "";
            $scope.search_member_data = "";
            $scope.is_in_edit_mode = false;
            $scope.deleting_invoice_id = 0;
            $scope.current_menu_nav = "MENU";
            $scope.invoice_delete_description = "";
            $scope.disable_print_after_save_all_buttons = false;
            $scope.is_in_edit_mode_invoice = false;
            $scope.price_per_hour_person = 100000;
            $scope.credit_state = "SHOW_CREDITS";
            $scope.menu_items_with_categories = [];
            $scope.deleting_item = {
                type: "",
                id: 0
            };
            $scope.selected_category = {
                "items": []
            };
            $scope.night_report_inputs = {
                "income_report": 0,
                "outcome_report": 0,
                "event_tickets": 0,
                "current_money_in_cash": 0
            };
            $scope.new_invoice_data = {
                'invoice_sales_id': 0,
                'table_id': 0,
                'table_name': 0,
                'member_id': 0,
                'guest_numbers': 0,
                'member_name': '',
                'member_data': '',
                'current_game': {
                    'id': 0,
                    'numbers': 0,
                    'start_time': ''
                },
                'menu_items_old': [],
                'menu_items_new': [],
                'shop_items_old': [],
                'shop_items_new': [],
                'games': [],
                'sum_all_games': {
                    total_seconds: 0,
                    total_price: 0,
                    total_hours: 0,
                    total_minutes: 0
                },
                'total_price': 0,
                'cash': 0,
                'card': 0,
                'discount': 0,
                'tip': 0,
                'total_credit': 0,
                'used_credit': 0,
                'credits_data': [],
                'static_guest_name': "",
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };

            $scope.will_delete_items = {
                'invoice_id': 0,
                'shop': [],
                'menu': [],
                'game': [],
                "message": ''
            };

            $scope.new_member_data = {
                'member_id': 0,
                'first_name': '',
                'last_name': '',
                'card_number': '',
                'year_of_birth': '',
                'month_of_birth': '',
                'day_of_birth': '',
                'phone': '',
                'intro': null,
                'branch': $rootScope.user_data.branch
            };

            $scope.tables_have_invoice = [];

            $scope.selected_table_data = [];

            $scope.tables = [];

            $scope.search_data_menu_item = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch
            };

            $scope.search_data_shop_products = {
                'search_word': ''
            };
            $scope.new_credit_data = {
                'member_id': $scope.new_invoice_data.member_id,
                'total_credit': 0,
                'expire_date': '',
                'expire_time': '00:00',
                'start_date': '',
                'start_time': '00:00',
                'credit_category': ''
            };

            $scope.credit_categories = [
                {key: "BAR", name: "آیتم‌های بار"},
                {key: "KITCHEN", name: "آیتم‌های آشپزخانه"},
                {key: "OTHER", name: "آیتم‌های سایر"},
                {key: "SHOP", name: "محصولات فروشگاهی"},
                {key: "GAME", name: "بازی"}
            ];

            $scope.check_cash();
            $scope.get_menu_items_with_categories_data($rootScope.user_data);
            $scope.get_tables_data($rootScope.user_data);
            $scope.get_shop_products();
            $scope.get_menu_item_data($rootScope.user_data);
            $window.onkeyup = function (event) {
                if (event.keyCode === 27) {
                    $scope.closeAddInvoiceModal();
                    $scope.closePayModal();
                    $scope.closeDeleteModal();
                    $rootScope.close_modal("editSettledInvoicePayment", "viewInvoiceModal");
                    $rootScope.close_modal("viewInvoiceModal");
                }
            };
        };

        $scope.compare_before_exit = function () {
            return JSON.stringify($scope.first_initial_value_of_invoice_sale) === JSON.stringify($scope.new_invoice_data);
        };

        $scope.config_clock = function () {
            jQuery.noConflict();
            (function ($) {
                var choices = ["00", "15", "30", "45"];
                $('#expire_credit_time').clockpicker({
                    donetext: 'تایید',
                    autoclose: true,
                    afterShow: function () {
                        $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                            return !($.inArray($(element).text(), choices) != -1)
                        }).remove();
                    },
                    afterDone: function () {
                        var selected_min = $('#expire_credit_time').val().split(":")[1];
                        if (!choices.includes(selected_min)) {
                            $('#expire_credit_time').val("");
                        }
                        else {
                            $scope.new_reserve_data.start_time = $('#expire_credit_time').val();
                        }
                    }
                });
                $('#start_credit_time').clockpicker({
                    donetext: 'تایید',
                    autoclose: true,
                    afterShow: function () {
                        $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                            return !($.inArray($(element).text(), choices) != -1)
                        }).remove();
                    },
                    afterDone: function () {
                        var seleceted_min = $('#start_credit_time').val().split(":")[1];
                        if (!choices.includes(seleceted_min)) {
                            $('#start_credit_time').val("");
                        }
                        else {
                            $scope.new_reserve_data.start_time = $('#start_credit_time').val();
                        }
                    }
                });
            })(jQuery);
        };

        $scope.convert_total_seconds_to_hours_minutes = function () {
            var hours = String($scope.new_invoice_data.sum_all_games.total_hours);
            var minutes = String($scope.new_invoice_data.sum_all_games.total_minutes);
            if (hours.length === 1) {
                hours = "0" + hours
            }
            if (minutes.length === 1) {
                minutes = "0" + minutes
            }
            return hours + ":" + minutes
        };

        $scope.setStaticGuestName = function (guest_name) {
            $scope.new_invoice_data.static_guest_name = guest_name;
            if (!guest_name) $scope.new_invoice_data.member_data = "مهمان";
            else $scope.new_invoice_data.member_data = guest_name;
        };

        $scope.clickOnMemberInput = function () {
            $scope.current_menu_nav = "MEMBER";
            jQuery.noConflict();
            (function ($) {
                $timeout(function () {
                    $('#searchMemberInput').focus();
                });
            })(jQuery);
        };

        $scope.set_today_for_credit_start_date = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    var date = new Date();
                    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                    $("#start_credit_date").datepicker();
                    $('#start_credit_date').datepicker('setDate', today);
                });
            })(jQuery);
        };


        $scope.change_credit_menu_state = function (state_name) {
            $scope.credit_state = state_name;
            if (state_name === "ADD_CREDITS") {
                $timeout(function () {
                    jQuery.noConflict();
                    (function ($) {
                        $(document).ready(function () {
                            $("#expire_credit_date").datepicker();
                        });
                        $(document).ready(function () {
                            $("#start_credit_date").datepicker();
                        });
                    })(jQuery);
                    $scope.set_today_for_credit_start_date();
                    $scope.config_clock();
                })
            }
        };

        $scope.add_member_and_add_to_invoice = function () {
            dashboardHttpRequest.addMember($scope.new_member_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        var first_name = data['created_member']['first_name'];
                        var last_name = data['created_member']['last_name'];
                        $scope.create_member_offline(data['created_member']);
                        $scope.new_invoice_data.member_id = data['created_member']['member_primary_key'];
                        $scope.new_invoice_data.member_name = first_name + " " + last_name;
                        $scope.new_invoice_data.member_data = first_name + " " + last_name;
                        $rootScope.show_toast("عضو جدید با موفقیت اضافه شد.", 'success');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.create_member_offline = function (online_server_response) {
            var sending_data = {
                'payload': {
                    "last_name": online_server_response['last_name'],
                    "card_number": online_server_response['card_number'],
                    "method": online_server_response['method'],
                    "member_primary_key": online_server_response['member_primary_key']
                },
                'username': $rootScope.user_data.username
            };
            offlineAPIHttpRequest.create_member(sending_data);
        };

        $scope.show_today_invoices = function () {
            $scope.current_selected_table_name = "";
            $scope.new_invoice_data.table_id = 0;
            $state.go('dashboard.cash_manager.salon', {table_name: ""}, {
                notify: false,
                reload: false,
                location: 'replace',
                inherit: true
            });
        };

        $scope.get_status_data = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };
            dashboardHttpRequest.getTodayStatus(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.status = data['all_today_status'];
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.check_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.checkCashExist(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.cash_state = "";
                        $scope.get_today_cash();
                    }
                    else if (data['response_code'] === 3) {
                        if (data['error_mode'] === "NO_CASH") {
                            $rootScope.cash_state = "NO_CASH";
                        }
                        else if (data['error_mode'] === "OLD_CASH") {
                            $rootScope.cash_state = "OLD_CASH";
                            $scope.get_today_cash();
                        }
                        else if (data['error_mode'] === "OLD_CASH_WITH_UNSETTLED_INVOICES") {
                            $rootScope.cash_state = "OLD_CASH_WITH_UNSETTLED_INVOICES";
                            $scope.get_today_cash();
                        }
                    }
                    $rootScope.is_page_loading = false;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                });
        };

        $scope.close_cash = function () {
            var sending_data = {
                'night_report_inputs': $scope.night_report_inputs,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.closeCash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.close_cash_offline();
                        $scope.print_night_report();
                        $scope.log_out();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.close_cash_offline = function () {
            var sending_data = {
                'night_report_inputs': $scope.night_report_inputs,
                'branch_id': $rootScope.user_data.branch
            };
            offlineAPIHttpRequest.close_cash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                });
        };

        $scope.log_out = function () {
            $auth.logout();
            $window.location.href = '/';
        };

        $scope.print_night_report = function () {
            var sending_data = {
                'cash_id': $rootScope.cash_data.cash_id,
                'location_url': "https://namak.works/"
            };
            $http({
                method: 'POST',
                url: 'http://127.0.0.1:8000/printNightReport',
                data: sending_data,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(function successCallback(response) {

            }, function errorCallback(response) {
                $rootScope.show_toast("اتصال سرور پرینتر نمک برقرار نیست، مجددا برنامه پرینتر نمک را اجرا کنید", 'danger');
            });
        };

        $scope.open_cash = function () {
            dashboardHttpRequest.openCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.open_cash_offline(data['new_cash_id']);
                        $scope.get_today_cash();
                        $state.go("dashboard.cash_manager.salon", {}, {reload: true});
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.open_cash_offline = function (new_cash_id) {
            var sending_data = {
                "branch": $rootScope.user_data.branch,
                "cash_server_id": new_cash_id
            };
            offlineAPIHttpRequest.open_cash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                });
        };

        $scope.create_credit = function () {
            $scope.new_credit_data.member_id = $scope.new_invoice_data.member_id;
            jQuery.noConflict();
            (function ($) {
                $scope.new_credit_data.expire_date = $("#expire_credit_date").val();
                $scope.new_credit_data.expire_time = $("#expire_credit_time").val();
                $scope.new_credit_data.start_date = $("#start_credit_date").val();
                $scope.new_credit_data.start_time = $("#start_credit_time").val();
            })(jQuery);
            dashboardHttpRequest.createCredit($scope.new_credit_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.credit_state = "SHOW_CREDITS";
                        for (var i = 0; i < $scope.new_invoice_data.credits_data.length; i++) {
                            if ($scope.new_invoice_data.credits_data[i].type === $scope.new_credit_data.credit_category) {
                                $scope.new_invoice_data.credits_data[i].total_price += parseInt($scope.new_credit_data.total_credit);
                                $scope.new_invoice_data.total_credit += parseInt($scope.new_credit_data.total_credit);
                                break;
                            }
                        }
                        $scope.new_credit_data = {
                            'member_id': $scope.new_invoice_data.member_id,
                            'total_credit': 0,
                            'expire_date': '',
                            'expire_time': '00:00',
                            'start_date': '',
                            'start_time': '00:00',
                            'credit_category': ''
                        };
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.perform_credit = function () {
            var sending_data = {
                'invoice_id': $scope.new_invoice_data.invoice_sales_id
            };
            if ($scope.new_invoice_data.total_price > $scope.new_invoice_data.used_credit) {
                dashboardHttpRequest.performCredit(sending_data)
                    .then(function (data) {
                        $scope.disable_print_after_save_all_buttons = false;
                        if (data['response_code'] === 2) {
                            $scope.new_invoice_data.used_credit += data['used_credit'];
                            $scope.new_invoice_data.total_credit -= data['used_credit'];
                            $scope.current_selected_table_name = $stateParams.table_name;
                            if ($scope.current_selected_table_name) {
                                $scope.selectTable($scope.current_selected_table_name);
                            }
                            $scope.new_invoice_data.credits_data = data['credits_data'];
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {
                        $scope.disable_print_after_save_all_buttons = false;
                    });
            }
        };

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $rootScope.cash_data.cash_id = data['cash_id'];
                        $scope.new_invoice_data.cash_id = data['cash_id'];
                        $scope.first_initial_value_of_invoice_sale = angular.copy($scope.new_invoice_data);
                        if ($rootScope.cash_state) {
                            $scope.get_status_data();
                        }
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.cash_data.cash_id = 0;
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                });
        };

        $scope.settleInvoice = function () {
            var sending_data = {
                'invoice_id': $scope.new_invoice_data.invoice_sales_id,
                'cash': $scope.new_invoice_data.cash,
                'card': $scope.new_invoice_data.card,
            };
            dashboardHttpRequest.settleInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.settle_invoice_offline();
                        $scope.closePayModal();
                        $scope.get_shop_products();
                        $scope.closeAddInvoiceModal();
                        if ($rootScope.cash_state === "OLD_CASH_WITH_UNSETTLED_INVOICES") {
                            $scope.check_cash();
                        }
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.settle_invoice_offline = function () {
            var sending_data = {
                'invoice_id': $scope.new_invoice_data.invoice_sales_id,
                'cash': $scope.new_invoice_data.cash,
                'card': $scope.new_invoice_data.card
            };
            offlineAPIHttpRequest.settle_invoice_sale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                });
        };

        $scope.print_data = function (invoice_id, print_kind, invoice_data) {
            $scope.disable_print_after_save_all_buttons = true;
            if (print_kind === "CASH") {
                $scope.ready_for_settle(invoice_id);
                var sending_data = {
                    'is_customer_print': 1,
                    'invoice_id': invoice_id,
                    'location_url': "https://namak.works/"
                };
                $http({
                    method: 'POST',
                    url: 'http://127.0.0.1:8000/printData',
                    data: sending_data,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(function successCallback(response) {
                    $scope.disable_print_after_save_all_buttons = false;
                }, function errorCallback(response) {
                    $scope.disable_print_after_save_all_buttons = false;
                    $rootScope.show_toast("اتصال سرور پرینتر نمک برقرار نیست، مجددا برنامه پرینتر نمک را اجرا کنید", 'danger');
                });
            }
            else if (print_kind === "NO-CASH") {
                var sending_data = {
                    'is_customer_print': 0,
                    'invoice_id': invoice_id,
                    'invoice_data': invoice_data,
                    'location_url': "https://namak.works/"
                };
                $http({
                    method: 'POST',
                    url: 'http://127.0.0.1:8000/printData',
                    data: sending_data,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).then(function successCallback(response) {
                    var sending_data_2 = {
                        'invoice_id': invoice_id,
                        'activate_is_print': true
                    };
                    dashboardHttpRequest.printAfterSave(sending_data_2)
                        .then(function (data) {
                            if (data['response_code'] === 2) {
                                $scope.print_after_save_offline(sending_data_2);
                                $scope.disable_print_after_save_all_buttons = false;
                            }
                            else if (data['response_code'] === 3) {
                                $scope.disable_print_after_save_all_buttons = false;
                                $rootScope.show_toast(data.error_msg, 'danger');
                            }
                        }, function (error) {
                            $scope.disable_print_after_save_all_buttons = false;
                        });
                }, function errorCallback(response) {
                    $scope.disable_print_after_save_all_buttons = false;
                    $rootScope.show_toast("اتصال سرور پرینتر نمک برقرار نیست، مجددا برنامه پرینتر نمک را اجرا کنید", 'danger');
                });
            }
        };


        $scope.print_after_save = function (invoice_id) {
            $scope.disable_print_after_save_all_buttons = true;
            if ($scope.is_in_edit_mode_invoice) {
                $scope.new_invoice_data['in_edit_mode'] = "IN_EDIT_MODE";
            }
            else {
                $scope.new_invoice_data['in_edit_mode'] = "OUT_EDIT_MODE";
            }
            $scope.is_in_edit_mode_invoice = false;
            $scope.new_invoice_data.referal_page = $state.current.name;
            $scope.new_invoice_data.method_name = "print_after_save";
            dashboardHttpRequest.addInvoiceSales($scope.new_invoice_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data['invoice_sales_current_created_game_server_primary_key'] = data['new_game_id'];
                        $scope.new_invoice_data['invoice_sales_server_primary_key'] = data['new_invoice_id'];
                        $scope.create_invoice_sale_offline($scope.new_invoice_data);
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.refreshInvoice(data['new_invoice_id']);
                        // printing after saving
                        var sending_data = {
                            'invoice_id': data['new_invoice_id'],
                            'activate_is_print': false
                        };
                        dashboardHttpRequest.printAfterSave(sending_data)
                            .then(function (data) {
                                if (data['response_code'] === 2) {
                                    $scope.print_after_save_offline(sending_data);
                                    $scope.print_data_info = data['printer_data'];
                                    $scope.print_data(sending_data['invoice_id'], "NO-CASH", $scope.print_data_info);
                                }
                                else if (data['response_code'] === 3) {
                                    $rootScope.show_toast(data.error_msg, 'danger');
                                }
                            });

                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };


        $scope.print_cash = function () {
            $scope.disable_print_after_save_all_buttons = true;
            if ($scope.is_in_edit_mode_invoice) {
                $scope.new_invoice_data['in_edit_mode'] = "IN_EDIT_MODE";
            }
            else {
                $scope.new_invoice_data['in_edit_mode'] = "OUT_EDIT_MODE";
            }
            $scope.is_in_edit_mode_invoice = false;
            $scope.new_invoice_data.referal_page = $state.current.name;
            $scope.new_invoice_data.method_name = "print_cash";
            dashboardHttpRequest.addInvoiceSales($scope.new_invoice_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        var new_invoice_id = data['new_invoice_id'];
                        $scope.new_invoice_data['invoice_sales_current_created_game_server_primary_key'] = data['new_game_id'];
                        $scope.new_invoice_data['invoice_sales_server_primary_key'] = data['new_invoice_id'];
                        $scope.create_invoice_sale_offline($scope.new_invoice_data);
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.print_data(new_invoice_id, 'CASH');
                        $scope.refreshInvoice(data['new_invoice_id']);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.payModalChangeNumber = function () {
            $scope.new_invoice_data.card = Number($scope.new_invoice_data.total_price) - Number($scope.new_invoice_data.cash) - Number($scope.new_invoice_data.discount) + Number($scope.new_invoice_data.tip) - Number($scope.new_invoice_data.used_credit);
        };

        $scope.can_settle_invoice = function () {
            jQuery.noConflict();
            (function ($) {
                $('#settle_button').prop("disabled", false);
                if ($scope.new_invoice_data.current_game.start_time)
                    $('#settle_button').prop("disabled", true);
            })(jQuery);
        };

        $scope.openPayModal = function () {
            $scope.disable_print_after_save_all_buttons = true;
            if ($scope.is_in_edit_mode_invoice) {
                $scope.new_invoice_data['in_edit_mode'] = "IN_EDIT_MODE";
            }
            else {
                $scope.new_invoice_data['in_edit_mode'] = "OUT_EDIT_MODE";
            }
            $scope.is_in_edit_mode_invoice = false;
            $scope.new_invoice_data.referal_page = $state.current.name;
            $scope.new_invoice_data.method_name = "openPayModal";
            dashboardHttpRequest.addInvoiceSales($scope.new_invoice_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data['invoice_sales_current_created_game_server_primary_key'] = data['new_game_id'];
                        $scope.new_invoice_data['invoice_sales_server_primary_key'] = data['new_invoice_id'];
                        $scope.create_invoice_sale_offline($scope.new_invoice_data);
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.refreshInvoiceInPayModal(data['new_invoice_id']);
                        $scope.disable_print_after_save_all_buttons = false;
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                        $scope.disable_print_after_save_all_buttons = false;
                    }
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                });
        };

        $scope.closePayModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#payModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
        };

        $scope.openDeleteModal = function (deleting_item_type, deleting_item_id) {
            $scope.deleting_item = {
                type: deleting_item_type,
                id: deleting_item_id
            };
            $rootScope.open_modal('deleteItemsModal', 'addInvoiceModal');
        };

        $scope.closeDeleteModal = function () {
            $rootScope.close_modal('deleteItemsModal', 'addInvoiceModal');
            $scope.read_only_mode = false;
        };

        $scope.openDeleteInvoiceModal = function (invoice_id) {
            $scope.deleting_invoice_id = invoice_id;
            $rootScope.open_modal('deleteInvoiceModal');
        };

        $scope.delete_invoice = function () {
            var sending_data = {
                "invoice_id": $scope.deleting_invoice_id,
                "description": $scope.invoice_delete_description
            };
            dashboardHttpRequest.deleteInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.delete_invoice_offline(sending_data);
                        $scope.invoice_delete_description = "";
                        $scope.deleting_invoice_id = 0;
                        $scope.close_modal('deleteInvoiceModal');
                        $scope.getAllTodayInvoices();
                        if ($rootScope.cash_state === "OLD_CASH_WITH_UNSETTLED_INVOICES") {
                            $scope.check_cash();
                        }
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.delete_items = function () {
            if ($scope.deleting_item.type === "MENU")
                $scope.will_delete_items.menu.push($scope.deleting_item.id);
            else if ($scope.deleting_item.type === "SHOP")
                $scope.will_delete_items.shop.push($scope.deleting_item.id);
            else if ($scope.deleting_item.type === "GAME")
                $scope.will_delete_items.game.push($scope.deleting_item.id);
            dashboardHttpRequest.deleteItems($scope.will_delete_items)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.delete_items_offline($scope.will_delete_items);
                        $scope.closeDeleteModal();
                        $scope.refreshInvoice($scope.will_delete_items.invoice_id);
                        $scope.will_delete_items.game = [];
                        $scope.will_delete_items.shop = [];
                        $scope.will_delete_items.menu = [];
                        $scope.will_delete_items.message = "";
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.get_shop_products = function () {
            dashboardHttpRequest.getShopProducts($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.shop_products_original = data['shop_products'];
                        $scope.shop_products = data['shop_products'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.changeItemShopNumber = function (item_index) {
            var new_number = $scope.new_invoice_data.shop_items_new[item_index].nums;
            var item_price = $scope.new_invoice_data.shop_items_new[item_index].price;
            $scope.new_invoice_data.shop_items_new[item_index].total = new_number * item_price;
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_data.shop_items_new.length; i++) {
                var entry = $scope.new_invoice_data.shop_items_new[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_data.shop_items_old.length; j++) {
                var entry2 = $scope.new_invoice_data.shop_items_old[j];
                new_total_price += entry2.total;
            }
            for (var m = 0; m < $scope.new_invoice_data.menu_items_new.length; m++) {
                var entry3 = $scope.new_invoice_data.menu_items_new[m];
                new_total_price += entry3.total;
            }
            for (var n = 0; n < $scope.new_invoice_data.menu_items_old.length; n++) {
                var entry4 = $scope.new_invoice_data.menu_items_old[n];
                new_total_price += entry4.total;
            }
            for (var g = 0; g < $scope.new_invoice_data.games.length; g++) {
                var entry5 = $scope.new_invoice_data.games[g];
                new_total_price += entry5.total;
            }
            $scope.new_invoice_data.total_price = new_total_price;
        };

        $scope.add_item_shop = function (id, name, price, real_numbers) {
            if (real_numbers <= 0) {
                return false
            }
            var int_price = parseInt(price);
            var int_id = parseInt(id);
            var is_fill = false;
            if ($scope.new_invoice_data.shop_items_new.length === 0) {
                $scope.new_invoice_data.shop_items_new.push({
                    'id': int_id,
                    'name': name,
                    'price': int_price,
                    'sale_price': int_price,
                    'nums': 1,
                    'total': int_price,
                    'description': ''
                });
                $scope.new_invoice_data.total_price += int_price;
            }
            else {
                for (var i = 0; i < $scope.new_invoice_data.shop_items_new.length; i++) {
                    var entry = $scope.new_invoice_data.shop_items_new[i];
                    if (parseInt(entry.id) === int_id) {
                        entry.nums += 1;
                        entry.total += entry.price;
                        is_fill = true;
                        $scope.new_invoice_data.total_price += entry.price;
                        break;
                    }
                }
                if (!is_fill) {
                    $scope.new_invoice_data.shop_items_new.push({
                        'id': int_id,
                        'name': name,
                        'price': int_price,
                        'sale_price': int_price,
                        'nums': 1,
                        'total': int_price,
                        'description': ''
                    });
                    $scope.new_invoice_data.total_price += int_price;
                }
                is_fill = false;
            }
        };

        $scope.deleteNewItem = function (item_index) {
            $scope.new_invoice_data.total_price -= $scope.new_invoice_data.menu_items_new[item_index].price * $scope.new_invoice_data.menu_items_new[item_index].nums;
            $scope.new_invoice_data.menu_items_new.splice(item_index, 1);
        };

        $scope.deleteNewItemShop = function (item_index) {
            $scope.new_invoice_data.total_price -= $scope.new_invoice_data.shop_items_new[item_index].price * $scope.new_invoice_data.shop_items_new[item_index].nums;
            $scope.new_invoice_data.shop_items_new.splice(item_index, 1);
        };

        $scope.changeMenuNav = function (name) {
            $scope.current_menu_nav = name;
        };

        $scope.changeItemNumber = function (item_index) {
            var new_number = $scope.new_invoice_data.menu_items_new[item_index].nums;
            var item_price = $scope.new_invoice_data.menu_items_new[item_index].price;
            $scope.new_invoice_data.menu_items_new[item_index].total = new_number * item_price;
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_data.menu_items_new.length; i++) {
                var entry = $scope.new_invoice_data.menu_items_new[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_data.menu_items_old.length; j++) {
                var entry2 = $scope.new_invoice_data.menu_items_old[j];
                new_total_price += entry2.total;
            }
            for (var m = 0; m < $scope.new_invoice_data.shop_items_new.length; m++) {
                var entry3 = $scope.new_invoice_data.shop_items_new[m];
                new_total_price += entry3.total;
            }
            for (var n = 0; n < $scope.new_invoice_data.shop_items_old.length; n++) {
                var entry4 = $scope.new_invoice_data.shop_items_old[n];
                new_total_price += entry4.total;
            }
            for (var g = 0; g < $scope.new_invoice_data.games.length; g++) {
                var entry5 = $scope.new_invoice_data.games[g];
                new_total_price += entry5.total;
            }

            $scope.new_invoice_data.total_price = new_total_price;
        };

        $scope.selectTable = function (table_name) {
            $state.go($state.current, {table_name: table_name}, {
                notify: false,
                reload: false,
                location: 'replace',
                inherit: true
            });
            $scope.current_selected_table_name = table_name;
            $scope.selected_table_data = [];
            var found_table = $filter('filter')($scope.tables, {'table_name': table_name});
            if (found_table.length) {
                $scope.new_invoice_data.table_id = found_table[0].table_id;
                for (var i = 0; i < $scope.all_today_invoices.length; i++) {
                    if ($scope.all_today_invoices[i].table_name === table_name && $scope.all_today_invoices[i].is_settled === 0) {
                        $scope.selected_table_data.push($scope.all_today_invoices[i]);
                    }
                }
            }
            $scope.first_initial_value_of_invoice_sale = angular.copy($scope.new_invoice_data);
            $rootScope.is_page_loading = false;
        };

        $scope.check_table_has_invoice = function () {
            $scope.tables_have_invoice = [];
            for (var i = 0; i < $scope.all_today_invoices.length; i++) {
                if ($scope.tables_have_invoice.indexOf($scope.all_today_invoices[i].table_name) === -1 && $scope.all_today_invoices[i].is_settled === 0) {
                    $scope.tables_have_invoice.push($scope.all_today_invoices[i].table_name);
                }
            }
        };

        $scope.getAllTodayInvoices = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id,
            };
            dashboardHttpRequest.getAllTodayInvoices(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.all_today_invoices = data['all_today_invoices'];
                        $scope.check_table_has_invoice();
                        $scope.current_selected_table_name = $stateParams.table_name;
                        if ($scope.current_selected_table_name) {
                            $scope.selectTable($scope.current_selected_table_name);
                        }
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.getAllInvoiceGames = function (invoice_id) {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                "invoice_id": parseInt(invoice_id)
            };
            dashboardHttpRequest.getAllInvoiceGames(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data.games = data['games'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.endCurrentGame = function (game_id) {
            $scope.disable_print_after_save_all_buttons = true;
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                "game_id": parseInt(game_id)
            };
            dashboardHttpRequest.endCurrentGame(sending_data)
                .then(function (data) {
                    $scope.disable_print_after_save_all_buttons = false;
                    if (data['response_code'] === 2) {
                        $scope.end_current_game_offline(sending_data);
                        $scope.new_invoice_data.current_game = {
                            'id': 0,
                            'numbers': 0,
                            'start_time': ''
                        };
                        $scope.can_settle_invoice();
                        $scope.refreshInvoice($scope.new_invoice_data.invoice_sales_id);
                        $rootScope.show_toast("بازی با موفقیت پایان یافت.", 'success');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                });
        };

        $scope.addGuestNums = function (numbers) {
            $scope.new_invoice_data.guest_numbers = parseInt(numbers);
        };

        $scope.add_item = function (id, name, price) {
            var int_price = parseInt(price);
            var int_id = parseInt(id);
            var is_fill = false;
            $scope.new_invoice_data.total_price += int_price;
            if ($scope.new_invoice_data.menu_items_new.length === 0) {
                $scope.new_invoice_data.menu_items_new.push({
                    'id': int_id,
                    'name': name,
                    'price': int_price,
                    'nums': 1,
                    'total': int_price,
                    'description': ''
                });
            }
            else {
                for (var i = 0; i < $scope.new_invoice_data.menu_items_new.length; i++) {
                    var entry = $scope.new_invoice_data.menu_items_new[i];
                    if (parseInt(entry.id) === int_id) {
                        entry.nums += 1;
                        entry.total += int_price;
                        is_fill = true;
                        break;
                    }
                }
                if (!is_fill) {
                    $scope.new_invoice_data.menu_items_new.push({
                        'id': int_id,
                        'name': name,
                        'price': int_price,
                        'nums': 1,
                        'total': int_price,
                        'description': ''
                    });
                }
                is_fill = false;
            }
        };

        $scope.start_game = function () {
            var now = new Date();
            $scope.new_invoice_data.current_game.start_time = now.getHours() + ":" + now.getMinutes();
            if ($scope.new_invoice_data.guest_numbers === 0) {
                $scope.new_invoice_data.guest_numbers = $scope.new_invoice_data.current_game.numbers;
            }
        };

        $scope.saveInvoice = function () {
            $scope.disable_print_after_save_all_buttons = true;
            if ($scope.is_in_edit_mode_invoice) {
                $scope.new_invoice_data['in_edit_mode'] = "IN_EDIT_MODE";
            }
            else {
                $scope.new_invoice_data['in_edit_mode'] = "OUT_EDIT_MODE";
            }
            $scope.is_in_edit_mode_invoice = false;
            $scope.new_invoice_data.referal_page = $state.current.name;
            $scope.new_invoice_data.method_name = "SaveInvoice";
            dashboardHttpRequest.addInvoiceSales($scope.new_invoice_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data['invoice_sales_current_created_game_server_primary_key'] = data['new_game_id'];
                        $scope.new_invoice_data['invoice_sales_server_primary_key'] = data['new_invoice_id'];
                        $scope.create_invoice_sale_offline($scope.new_invoice_data);
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.refreshInvoice(data['new_invoice_id']);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                    $scope.disable_print_after_save_all_buttons = false;
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                });
        };

        $scope.create_invoice_sale_offline = function (payload) {
            offlineAPIHttpRequest.create_new_invoice_sales(payload)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {

                });
        };

        $scope.end_current_game_offline = function (payload) {
            offlineAPIHttpRequest.end_current_game(payload)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {

                });
        };

        $scope.ready_for_settle_offline = function (payload) {
            offlineAPIHttpRequest.ready_for_settle(payload)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {

                });
        };

        $scope.print_after_save_offline = function (payload) {
            offlineAPIHttpRequest.print_after_save(payload)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {

                });
        };

        $scope.delete_items_offline = function (payload) {
            offlineAPIHttpRequest.delete_items(payload)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {

                });
        };

        $scope.delete_invoice_offline = function (payload) {
            offlineAPIHttpRequest.delete_invoice(payload)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                });
        };

        $scope.get_menu_items_with_categories_data = function (data) {
            dashboardHttpRequest.getMenuItemsWithCategories(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.menu_items_with_categories = data['menu_items_with_categories'];
                        if ($scope.menu_items_with_categories.length) $scope.showCollapse(0);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.get_tables_data = function (data) {
            dashboardHttpRequest.getTables(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.tables = data['tables'];
                        $scope.categorize_tables($scope.tables);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.categorize_tables = function (tables_data) {
            $scope.categorized_tables_data = [];
            for (var i = 0; i < tables_data.length; i++) {
                var category_find = $filter('filter')($scope.categorized_tables_data, {'table_category_name': tables_data[i].table_category_name});
                if (category_find.length === 0) {
                    $scope.categorized_tables_data.push(
                        {
                            "table_category_name": tables_data[i].table_category_name,
                            "tables": [tables_data[i]]
                        }
                    );
                }
                else {
                    category_find[0].tables.push(tables_data[i]);
                }
            }
        };

        $scope.get_member_data = function (card_number) {
            var data = {
                'member_id': 0,
                'card_number': card_number,
                'branch': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getMember(data)
                .then(function (data) {
                    var first_name = data['member']['first_name'];
                    var last_name = data['member']['last_name'];
                    $scope.new_invoice_data.member_id = data['member']['id'];
                    $scope.new_invoice_data.member_name = first_name + " " + last_name;
                    $scope.new_invoice_data.member_data = first_name + " " + last_name;
                    $scope.new_invoice_data.credits_data = data['member']['credits_data'];
                });
        };

        $scope.showCollapse = function (collapse_id) {
            $scope.selected_category = $scope.menu_items_with_categories[collapse_id];
        };

        $scope.get_menu_item_data = function (data) {
            dashboardHttpRequest.getMenuItems(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.menu_items_original = data['menu_items'];
                        $scope.menu_items = data['menu_items'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.search_shop_products = function () {
            $scope.shop_products = $filter('filter')($scope.shop_products_original, {'name': $scope.search_data_shop_products.search_word});
        };
        $scope.searchMenuItem = function () {
            $scope.menu_items = $filter('filter')($scope.menu_items_original, {'name': $scope.search_data_menu_item.search_word});
        };

        $scope.openAddInvoiceModal = function () {
            $scope.can_settle_invoice();
            jQuery.noConflict();
            (function ($) {
                $('#addInvoiceModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addInvoiceModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
            $scope.getAllTodayInvoices();
            $scope.showCollapse(0);
            $scope.reset_deleted_items();
            $scope.clear_invoice_sale();
        };

        $scope.saveAndCloseInvoice = function () {
            $scope.disable_print_after_save_all_buttons = true;
            if ($scope.is_in_edit_mode_invoice) {
                $scope.new_invoice_data['in_edit_mode'] = "IN_EDIT_MODE";
            }
            else {
                $scope.new_invoice_data['in_edit_mode'] = "OUT_EDIT_MODE";
            }
            $scope.is_in_edit_mode_invoice = false;
            $scope.new_invoice_data.referal_page = $state.current.name;
            $scope.new_invoice_data.method_name = "SaveInvoice";
            dashboardHttpRequest.addInvoiceSales($scope.new_invoice_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data['invoice_sales_current_created_game_server_primary_key'] = data['new_game_id'];
                        $scope.new_invoice_data['invoice_sales_server_primary_key'] = data['new_invoice_id'];
                        $scope.create_invoice_sale_offline($scope.new_invoice_data);
                        $scope.closeAddInvoiceModal();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                    $scope.disable_print_after_save_all_buttons = false;
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                });
        };

        $scope.editInvoice = function (invoice_id) {
            $scope.is_in_edit_mode_invoice = true;
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getInvoice(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                        $scope.new_invoice_data = {
                            'invoice_sales_id': data['invoice']['invoice_sales_id'],
                            'table_id': data['invoice']['table_id'],
                            'table_name': data['invoice']['table_name'],
                            'member_id': data['invoice']['member_id'],
                            'guest_numbers': data['invoice']['guest_numbers'],
                            'member_name': data['invoice']['member_name'],
                            'member_data': data['invoice']['member_data'],
                            'current_game': {
                                'id': data['invoice']['current_game']['id'],
                                'numbers': data['invoice']['current_game']['numbers'],
                                'start_time': data['invoice']['current_game']['start_time']
                            },
                            'menu_items_old': data['invoice']['menu_items_old'],
                            'shop_items_old': data['invoice']['shop_items_old'],
                            'menu_items_new': [],
                            'shop_items_new': [],
                            'games': data['invoice']['games'],
                            'sum_all_games': data['invoice']['sum_all_games'],
                            'total_price': data['invoice']['total_price'],
                            'cash': data['invoice']['cash_amount'],
                            'card': data['invoice']['pos_amount'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'credits_data': data['invoice']['credits_data'],
                            'static_guest_name': data['invoice']['static_guest_name'],
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id
                        };
                        $scope.first_initial_value_of_invoice_sale = angular.copy($scope.new_invoice_data);
                        $scope.can_settle_invoice();
                        $scope.openAddInvoiceModal();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.refreshInvoice = function (invoice_id) {
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getInvoice(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                        $scope.new_invoice_data = {
                            'invoice_sales_id': data['invoice']['invoice_sales_id'],
                            'table_id': data['invoice']['table_id'],
                            'table_name': data['invoice']['table_name'],
                            'member_id': data['invoice']['member_id'],
                            'guest_numbers': data['invoice']['guest_numbers'],
                            'member_name': data['invoice']['member_name'],
                            'member_data': data['invoice']['member_data'],
                            'current_game': {
                                'id': data['invoice']['current_game']['id'],
                                'numbers': data['invoice']['current_game']['numbers'],
                                'start_time': data['invoice']['current_game']['start_time']
                            },
                            'menu_items_old': data['invoice']['menu_items_old'],
                            'shop_items_old': data['invoice']['shop_items_old'],
                            'menu_items_new': [],
                            'shop_items_new': [],
                            'games': data['invoice']['games'],
                            'sum_all_games': data['invoice']['sum_all_games'],
                            'total_price': data['invoice']['total_price'],
                            'cash': data['invoice']['cash_amount'],
                            'card': data['invoice']['pos_amount'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'credits_data': data['invoice']['credits_data'],
                            'static_guest_name': data['invoice']['static_guest_name'],
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id
                        };
                        $scope.first_initial_value_of_invoice_sale = angular.copy($scope.new_invoice_data);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.refreshInvoiceInPayModal = function (invoice_id) {
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getInvoice(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                        $scope.new_invoice_data = {
                            'invoice_sales_id': data['invoice']['invoice_sales_id'],
                            'table_id': data['invoice']['table_id'],
                            'table_name': data['invoice']['table_name'],
                            'member_id': data['invoice']['member_id'],
                            'guest_numbers': data['invoice']['guest_numbers'],
                            'member_name': data['invoice']['member_name'],
                            'member_data': data['invoice']['member_data'],
                            'current_game': {
                                'id': data['invoice']['current_game']['id'],
                                'numbers': data['invoice']['current_game']['numbers'],
                                'start_time': data['invoice']['current_game']['start_time']
                            },
                            'menu_items_old': data['invoice']['menu_items_old'],
                            'shop_items_old': data['invoice']['shop_items_old'],
                            'menu_items_new': [],
                            'shop_items_new': [],
                            'games': data['invoice']['games'],
                            'sum_all_games': data['invoice']['sum_all_games'],
                            'total_price': data['invoice']['total_price'],
                            'cash': data['invoice']['cash_amount'],
                            'card': data['invoice']['pos_amount'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'credits_data': data['invoice']['credits_data'],
                            'static_guest_name': data['invoice']['static_guest_name'],
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id
                        };
                        $scope.first_initial_value_of_invoice_sale = angular.copy($scope.new_invoice_data);
                        jQuery.noConflict();
                        (function ($) {
                            $scope.new_invoice_data.card = Number($scope.new_invoice_data.total_price) - Number($scope.new_invoice_data.discount) + Number($scope.new_invoice_data.tip) - Number($scope.new_invoice_data.used_credit);
                            $scope.new_invoice_data.cash = 0;
                            $('#payModal').modal('show');
                            $('#addInvoiceModal').css('z-index', 1000);
                        })(jQuery);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                });
        };

        $scope.set_class_name = function (table_name) {
            if ($scope.current_selected_table_name === table_name && $scope.tables_have_invoice.indexOf(table_name) !== -1) {
                return 'mainButton greenButton fullWidthButton';
            }
            else if ($scope.current_selected_table_name === table_name && $scope.tables_have_invoice.indexOf(table_name) === -1) {
                return 'mainButton oilBlueButton fullWidthButton';
            }
            else if ($scope.current_selected_table_name !== table_name && $scope.tables_have_invoice.indexOf(table_name) !== -1) {
                return 'mainButton whiteButton fullWidthButton';
            }
            else if ($scope.current_selected_table_name !== table_name && $scope.tables_have_invoice.indexOf(table_name) === -1) {
                return 'mainButton grayButton fullWidthButton';
            }
        };

        $scope.table_factor_counts = function (table_name) {
            if ($scope.all_today_invoices) {
                var count = 0;
                for (var i = 0; i < $scope.all_today_invoices.length; i++) {
                    if ($scope.all_today_invoices[i].table_name === table_name && $scope.all_today_invoices[i].is_settled === 0) {
                        count += 1;
                    }
                }
                return count;
            }
        };

        $scope.clear_invoice_sale = function () {
            var last_table_id = $scope.new_invoice_data.table_id;
            $scope.new_invoice_data = {
                'invoice_sales_id': 0,
                'table_id': 0,
                'table_name': 0,
                'member_id': 0,
                'guest_numbers': 0,
                'member_name': '',
                'member_data': '',
                'current_game': {
                    'id': 0,
                    'numbers': 0,
                    'start_time': ''
                },
                'menu_items_old': [],
                'menu_items_new': [],
                'shop_items_old': [],
                'shop_items_new': [],
                'games': [],
                'sum_all_games': {
                    total_seconds: 0,
                    total_price: 0,
                    total_hours: 0,
                    total_minutes: 0
                },
                'total_price': 0,
                'cash': 0,
                'card': 0,
                'discount': 0,
                'tip': 0,
                'total_credit': 0,
                'used_credit': 0,
                'credits_data': [],
                'static_guest_name': "",
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id
            };
            $scope.first_initial_value_of_invoice_sale = angular.copy($scope.new_invoice_data);
            $scope.new_member_data = {
                'member_id': 0,
                'first_name': '',
                'last_name': '',
                'card_number': '',
                'year_of_birth': '',
                'month_of_birth': '',
                'day_of_birth': '',
                'phone': '',
                'intro': null,
                'branch': $rootScope.user_data.branch
            };
            $scope.new_credit_data = {
                'member_id': $scope.new_invoice_data.member_id,
                'total_credit': 0,
                'expire_date': '',
                'expire_time': '00:00',
                'start_date': '',
                'start_time': '00:00',
                'credit_category': ''
            };
            $scope.new_invoice_data.table_id = last_table_id;
        };

        $scope.ready_for_settle = function (invoice_id) {
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.readyForSettle(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.ready_for_settle_offline(sending_data);
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                });
        };

        $scope.reset_deleted_items = function () {
            $scope.will_delete_items = {
                'invoice_id': 0,
                'shop': [],
                'menu': [],
                'game': [],
                "message": ''
            };
        };

        $scope.return_status_badge_class_invoice = function (status) {
            if (status === "ORDERED") {
                return "badge badge-success";
            }
            else if (status === "NOT_ORDERED") {
                return "badge badge-danger";
            }
            else if (status === "WAIT_FOR_SETTLE") {
                return "badge badge-warning";
            }
            else if (status === "DO_NOT_WANT_ORDER") {
                return "badge badge-info";
            }
        };

        $scope.return_status_badge_class_game = function (status) {
            if (status === "END_GAME") {
                return "badge badge-success";
            }
            else if (status === "WAIT_GAME") {
                return "badge badge-danger";
            }
            else if (status === "PLAYING") {
                return "badge badge-info";
            }
            else if (status === "NO_GAME") {
                return "badge badge-info";
            }
        };

        initialize();
    });