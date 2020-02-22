angular.module("dashboard")
    .controller("salonCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, $stateParams, $state, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.current_menu_nav = "MENU";
            $scope.invoice_delete_description = "";
            $scope.disable_print_after_save_all_buttons = false;
            $scope.is_in_edit_mode_invoice = false;
            $scope.first_time_edit_payment_init = true;
            $scope.selected_category = {
                "items": []
            };
            $scope.editable_invoice = {
                "invoice_id": 0,
                "cash": 5000,
                "pos": 0,
                "total": 0
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
                'total_price': 0,
                'cash': 0,
                'card': 0,
                'discount': 0,
                'tip': 0,
                'total_credit': 0,
                'used_credit': 0,
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id,
                'username': $rootScope.user_data.username
            };

            $scope.will_delete_items = {
                'invoice_id': 0,
                'shop': [],
                'menu': [],
                'game': [],
                "message": '',
                'username': $rootScope.user_data.username
            };

            $scope.tables_have_invoice = [];

            $scope.selected_table_data = [];

            $scope.tables = [];

            $scope.search_data_menu_item = {
                'search_word': '',
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };

            $scope.search_data_shop_products = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.get_today_cash();
            $scope.get_menu_items_with_categories_data($rootScope.user_data);
            $scope.get_tables_data($rootScope.user_data);
            $scope.get_shop_products();
            $scope.get_menu_item_data($rootScope.user_data);
            $window.onkeyup = function (event) {
                if (event.keyCode === 27) {
                    $scope.closeAddInvoiceModal();
                    $scope.closePayModal();
                    $scope.closeTimeCalcModal();
                    $scope.closeDeleteModal();
                    $scope.closeErrorModal();
                    $scope.closeDeleteInvoiceModal();
                    $rootScope.close_modal("editSettledInvoicePayment", "viewInvoiceModal");
                    $rootScope.close_modal("viewInvoiceModal");
                }
                if (event.ctrlKey && event.keyCode === 49) {

                }
                if (event.ctrlKey && event.keyCode === 50) {
                    $state.go('cash_manager.salon');
                }
                if (event.ctrlKey && event.keyCode === 51) {
                    $state.go('reservation');
                }
                if (event.ctrlKey && event.keyCode === 52) {
                    $state.go('member');
                }
                if (event.ctrlKey && event.keyCode === 53) {
                    $state.go('boardgame');
                }
                if (event.ctrlKey && event.keyCode === 54) {

                }
                if (event.ctrlKey && event.keyCode === 55) {
                    $state.go('account_manager.buy');
                }
                if (event.ctrlKey && event.keyCode === 56) {

                }
                if (event.ctrlKey && event.keyCode === 57) {
                    $state.go('manager.addEmployee');
                }
            }
        };

        $scope.perform_credit = function () {
            $scope.disable_print_after_save_all_buttons = true;
            var sending_data = {
                'username': $rootScope.user_data.username,
                'invoice_id': $scope.new_invoice_data.invoice_sales_id
            };
            dashboardHttpRequest.performCredit(sending_data)
                .then(function (data) {
                    $scope.disable_print_after_save_all_buttons = false;
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data.used_credit += data['used_credit'];
                        $scope.new_invoice_data.total_credit -= data['used_credit'];
                        $scope.getAllTodayInvoices();
                        $scope.current_selected_table_name = $stateParams.table_name;
                        if ($scope.current_selected_table_name) {
                            $scope.selectTable($scope.current_selected_table_name);
                        }
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.edit_settled_invoice_payment = function () {
            var sending_data = {
                "username": $rootScope.user_data.username,
                "invoice_data": $scope.editable_invoice
            };
            dashboardHttpRequest.editPaymentInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.close_modal('editSettledInvoicePayment', 'viewInvoiceModal')
                        $rootScope.close_modal("viewInvoiceModal");
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $rootScope.cash_data.cash_id = data['cash_id'];
                        $scope.new_invoice_data.cash_id = data['cash_id'];
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.cash_data.cash_id = 0;
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.settleInvoice = function () {
            var sending_data = {
                'invoice_id': $scope.new_invoice_data.invoice_sales_id,
                'cash': $scope.new_invoice_data.cash,
                'card': $scope.new_invoice_data.card,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.settleInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.closePayModal();
                        $scope.getAllTodayInvoices();
                        $scope.closeAddInvoiceModal();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.closePayModal();
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.closePayModal();
                    $scope.openErrorModal();
                });
        };

        $scope.print_data = function (invoice_id, print_kind, invoice_data) {
            $scope.disable_print_after_save_all_buttons = true;
            if (print_kind === "CASH") {
                $scope.ready_for_settle(invoice_id);
                var sending_data = {
                    'is_customer_print': 1,
                    'invoice_id': invoice_id
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
                    $scope.error_message = "Printer Server not connected.";
                    $scope.openErrorModal();
                });
            }
            else if (print_kind === "NO-CASH") {
                var sending_data = {
                    'is_customer_print': 0,
                    'invoice_id': invoice_id,
                    'invoice_data': invoice_data
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
                                $scope.disable_print_after_save_all_buttons = false;
                            }
                            else if (data['response_code'] === 3) {
                                $scope.disable_print_after_save_all_buttons = false;
                                $scope.error_message = data['error_msg'];
                                $scope.openErrorModal();
                            }
                        }, function (error) {
                            $scope.disable_print_after_save_all_buttons = false;
                            $scope.error_message = 500;
                            $scope.closeTimeCalcModal();
                            $scope.openErrorModal();
                        });
                }, function errorCallback(response) {
                    $scope.disable_print_after_save_all_buttons = false;
                    $scope.error_message = "Printer Server not connected.";
                    $scope.openErrorModal();
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
                        $scope.get_shop_products();
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.getAllTodayInvoices();
                        $scope.clear_invoice_sale();
                        $scope.closeAddInvoiceModal();
                        // printing after saving
                        var sending_data = {
                            'invoice_id': data['new_invoice_id'],
                            'activate_is_print': false
                        };
                        dashboardHttpRequest.printAfterSave(sending_data)
                            .then(function (data) {
                                if (data['response_code'] === 2) {
                                    $scope.print_data_info = data['printer_data'];
                                    $scope.print_data(sending_data['invoice_id'], "NO-CASH", $scope.print_data_info);
                                }
                                else if (data['response_code'] === 3) {
                                    $scope.error_message = data['error_msg'];
                                    $scope.openErrorModal();
                                }
                            }, function (error) {
                                $scope.error_message = 500;
                                $scope.closeTimeCalcModal();
                                $scope.openErrorModal();
                            });

                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
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
                        $scope.get_shop_products();
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.getAllTodayInvoices();
                        $scope.print_data(new_invoice_id, 'CASH');
                        $scope.refreshInvoice(data['new_invoice_id']);
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.payModalChangeNumber = function () {
            $scope.new_invoice_data.card = Number($scope.new_invoice_data.total_price) - Number($scope.new_invoice_data.cash) - Number($scope.new_invoice_data.discount) + Number($scope.new_invoice_data.tip) - Number($scope.new_invoice_data.used_credit);
        };

        $scope.edit_payment_modal_changer = function () {
            if ($scope.first_time_edit_payment_init) {
                $scope.editable_invoice = {
                    "invoice_id": $scope.new_invoice_data.invoice_sales_id,
                    "cash": $scope.new_invoice_data.cash_amount,
                    "pos": $scope.new_invoice_data.pos_amount,
                    "total": $scope.new_invoice_data.cash_amount + $scope.new_invoice_data.pos_amount
                };
                $timeout(function () {
                    $scope.first_time_edit_payment_init = false;
                }, 2000);
            }
            else{
                $scope.editable_invoice.pos = $scope.editable_invoice.total - $scope.editable_invoice.cash;
            }
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addInvoiceModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.can_settle_invoice = function () {
            $('#settle_button').prop("disabled", false);
            if ($scope.new_invoice_data.current_game.start_time || !$scope.new_invoice_data.invoice_sales_id)
                $('#settle_button').prop("disabled", true);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
        };

        $scope.openTimeCalcModal = function () {
            $scope.calculateTime();
            jQuery.noConflict();
            (function ($) {
                $('#timeCalcModal').modal('show');
                $('#addInvoiceModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeTimeCalcModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#timeCalcModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
        };

        $scope.openPermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('show');
                $('#addInvoiceModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closePermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
        };

        $scope.calculateTime = function () {
            dashboardHttpRequest.timeCalc($scope.new_invoice_data.current_game)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.calcedPoints = data['price'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.closeTimeCalcModal();
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.closeTimeCalcModal();
                    $scope.openErrorModal();
                });
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
                        $scope.get_shop_products();
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.refreshInvoiceInPayModal(data['new_invoice_id']);
                        $scope.getAllTodayInvoices();
                        $scope.disable_print_after_save_all_buttons = false;
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                        $scope.disable_print_after_save_all_buttons = false;
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
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

        $scope.openDeleteModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#deleteItemsModal').modal('show');
                $('#addInvoiceModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeDeleteModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#deleteItemsModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
            $scope.read_only_mode = false;
        };

        $scope.openDeleteInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#deleteInvoiceModal').modal('show');
                $('#addInvoiceModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeDeleteInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#deleteInvoiceModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
        };

        $scope.delete_invoice = function () {
            var sending_data = {
                "invoice_id": $scope.new_invoice_data.invoice_sales_id,
                "description": $scope.invoice_delete_description,
                "username": $rootScope.user_data.username,
                "branch_id": $rootScope.user_data.branch
            };
            dashboardHttpRequest.deleteInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.invoice_delete_description = "";
                        $scope.closeDeleteInvoiceModal();
                        $scope.closeAddInvoiceModal();
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
            $scope.closeDeleteModal();
        };

        $scope.delete_items = function () {
            dashboardHttpRequest.deleteItems($scope.will_delete_items)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.closeDeleteModal();
                        $scope.closeAddInvoiceModal();
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
            $scope.closeDeleteModal();
        };

        $scope.will_delete_items_adder = function (deleted_type, p_id) {
            if (deleted_type === 'shop') {
                var found = $scope.will_delete_items.shop.findIndex(function (element) {
                    return element === p_id;
                });
                if (found !== -1) {
                    $scope.will_delete_items.shop.splice(found, 1);
                }
                else if (found === -1) {
                    $scope.will_delete_items.shop.push(p_id);
                }
            }
            else if (deleted_type === 'menu') {
                var found2 = $scope.will_delete_items.menu.findIndex(function (element) {
                    return element === p_id;
                });
                if (found2 !== -1) {
                    $scope.will_delete_items.menu.splice(found2, 1);
                }
                else if (found2 === -1) {
                    $scope.will_delete_items.menu.push(p_id);
                }
            }
            else if (deleted_type === 'game') {
                var found3 = $scope.will_delete_items.game.findIndex(function (element) {
                    return element === p_id;
                });
                if (found3 !== -1) {
                    $scope.will_delete_items.game.splice(found3, 1);
                }
                else if (found3 === -1) {
                    $scope.will_delete_items.game.push(p_id);
                }
            }
        };

        $scope.get_shop_products = function () {
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getShopProducts(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.shop_products_original = data['shop_products'];
                        $scope.shop_products = data['shop_products'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
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

        $scope.add_item_shop = function (id, name, price) {
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
            if (name === "MENU") {
                $scope.current_menu_nav = name;
            }
            else if (name === "SHOP") {
                $scope.current_menu_nav = name;
            }
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
                $scope.new_invoice_data.table_name = table_name;
                for (var i = 0; i < $scope.all_today_invoices.length; i++) {
                    if ($scope.all_today_invoices[i].table_name === table_name && $scope.all_today_invoices[i].is_settled === 0) {
                        $scope.selected_table_data.push($scope.all_today_invoices[i]);
                    }
                }
            }
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
                'username': $rootScope.user_data.username
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
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.getAllInvoiceGames = function (invoice_id) {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username,
                "invoice_id": parseInt(invoice_id)
            };
            dashboardHttpRequest.getAllInvoiceGames(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data.games = data['games'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.endCurrentGame = function (game_id) {
            $scope.disable_print_after_save_all_buttons = true;
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username,
                "game_id": parseInt(game_id)
            };
            dashboardHttpRequest.endCurrentGame(sending_data)
                .then(function (data) {
                    $scope.disable_print_after_save_all_buttons = false;
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_data.current_game = {
                            'id': 0,
                            'numbers': 0,
                            'start_time': ''
                        };
                        $scope.can_settle_invoice();
                        $scope.refreshInvoice($scope.new_invoice_data.invoice_sales_id);
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                    $scope.error_message = 500;
                    $scope.openErrorModal();
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
                        $scope.get_shop_products();
                        $scope.new_invoice_data.current_game.id = data['new_game_id'];
                        $scope.getAllTodayInvoices();
                        $scope.clear_invoice_sale();
                        $scope.closeAddInvoiceModal();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                    $scope.disable_print_after_save_all_buttons = false;
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                    $scope.disable_print_after_save_all_buttons = false;
                });
        };

        $scope.get_menu_items_with_categories_data = function (data) {
            dashboardHttpRequest.getMenuItemsWithCategories(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.menu_items_with_categories = data['menu_items_with_categories'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
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
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.categorize_tables = function (tables_data) {
            $scope.categorized_tables_data = [
                {
                    "table_category_name": "A",
                    "tables": []
                }
            ];
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
                'username': $rootScope.user_data.username,
                'member_id': 0,
                'card_number': card_number
            };
            dashboardHttpRequest.getMember(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        var first_name = data['member']['first_name'];
                        var last_name = data['member']['last_name'];
                        $scope.new_invoice_data.member_id = data['member']['id'];
                        $scope.new_invoice_data.member_name = first_name + " " + last_name;
                        $scope.new_invoice_data.member_data = first_name + " " + last_name;

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

        $scope.showCollapse = function (collapse_id) {
            jQuery.noConflict();
            (function ($) {
                for (var i = 0; i < $scope.menu_items_with_categories.length; i++) {
                    $("#menuNavCollapse" + i).collapse('hide');
                }
                $("#menuNavCollapse" + collapse_id).collapse('toggle');
            })(jQuery);
            $scope.selected_category = $scope.menu_items_with_categories[collapse_id];
            $scope.selected_menu_nav_cat = collapse_id;
        };

        $scope.get_menu_item_data = function (data) {
            dashboardHttpRequest.getMenuItems(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.menu_items_original = data['menu_items'];
                        $scope.menu_items = data['menu_items'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
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
            if ($scope.new_invoice_data.member_id === 0) {
                $scope.get_member_data('0000');
            }
        };

        $scope.closeAddInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addInvoiceModal').modal('hide');
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addInvoiceModal').css('z-index', "");
            })(jQuery);
            $scope.showCollapse(0);
            $scope.reset_deleted_items();
            $scope.clear_invoice_sale();
        };

        $scope.openViewInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#viewInvoiceModal').modal('show');
            })(jQuery);
        };

        $scope.closeViewInvoiceModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#viewInvoiceModal').modal('hide');
            })(jQuery);
            $scope.reset_deleted_items();
        };

        $scope.editInvoice = function (invoice_id) {
            $scope.is_in_edit_mode_invoice = true;
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
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
                            'total_price': data['invoice']['total_price'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id,
                            'username': $rootScope.user_data.username
                        };
                        $scope.can_settle_invoice();
                        $scope.openAddInvoiceModal();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.initiate_edit_payment_invoice_sale = function () {
            $scope.editable_invoice = {
                "invoice_id": $scope.new_invoice_data.invoice_sales_id,
                "cash": $scope.new_invoice_data.cash_amount,
                "pos": $scope.new_invoice_data.pos_amount,
                "total": $scope.new_invoice_data.cash_amount + $scope.new_invoice_data.pos_amount
            };
            $rootScope.open_modal('editSettledInvoicePayment', 'viewInvoiceModal');
        };

        $scope.showInvoice = function (invoice_id) {
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
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
                            'total_price': data['invoice']['total_price'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            "cash_amount": Number(data['invoice']['cash_amount']),
                            "pos_amount": Number(data['invoice']['pos_amount']),
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openViewInvoiceModal();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };


        $scope.refreshInvoice = function (invoice_id) {
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
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
                            'total_price': data['invoice']['total_price'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'cash': 0,
                            'card': 0,
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id,
                            'username': $rootScope.user_data.username
                        };
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.refreshInvoiceInPayModal = function (invoice_id) {
            $scope.will_delete_items.invoice_id = invoice_id;
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
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
                            'total_price': data['invoice']['total_price'],
                            'discount': data['invoice']['discount'],
                            'tip': data['invoice']['tip'],
                            'total_credit': data['invoice']['total_credit'],
                            'used_credit': data['invoice']['used_credit'],
                            'cash': 0,
                            'card': 0,
                            'branch_id': $rootScope.user_data.branch,
                            'cash_id': $rootScope.cash_data.cash_id,
                            'username': $rootScope.user_data.username
                        };
                        jQuery.noConflict();
                        (function ($) {
                            $scope.new_invoice_data.card = Number($scope.new_invoice_data.total_price) - Number($scope.new_invoice_data.discount) + Number($scope.new_invoice_data.tip) - Number($scope.new_invoice_data.used_credit);
                            $scope.new_invoice_data.cash = 0;
                            $('#payModal').modal('show');
                            $('#addInvoiceModal').css('z-index', 1000);
                        })(jQuery);
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        $scope.set_class_name = function (table_name) {
            if ($scope.current_selected_table_name === table_name && $scope.tables_have_invoice.indexOf(table_name) !== -1) {
                return 'mainButton greenButton fullWidthButton';
            }
            else if ($scope.current_selected_table_name === table_name && $scope.tables_have_invoice.indexOf(table_name) === -1) {
                return 'mainButton blackButton fullWidthButton';
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
                'total_price': 0,
                'cash': 0,
                'card': 0,
                'discount': 0,
                'tip': 0,
                'total_credit': 0,
                'used_credit': 0,
                'branch_id': $rootScope.user_data.branch,
                'cash_id': $rootScope.cash_data.cash_id,
                'username': $rootScope.user_data.username
            };
            $scope.new_invoice_data.table_id = last_table_id;
            $scope.new_invoice_data.table_name = $scope.current_selected_table_name;
        };

        $scope.ready_for_settle = function (invoice_id) {
            var sending_data = {
                "invoice_id": invoice_id,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.readyForSettle(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.getAllTodayInvoices();
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.disable_print_after_save_all_buttons = false;
                    $scope.error_message = 500;
                    $scope.closeTimeCalcModal();
                    $scope.openErrorModal();
                });
        };

        $scope.reset_deleted_items = function () {
            $scope.will_delete_items = {
                'invoice_id': 0,
                'shop': [],
                'menu': [],
                'game': [],
                "message": '',
                'username': $rootScope.user_data.username
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