angular.module("dashboard")
    .controller("quickAccessCtrl", function ($scope, $interval, $rootScope, $filter, $state, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#datepicker_pay").datepicker();
                    $("#datepicker_expense").datepicker();
                });
            })(jQuery);
            $scope.members = [];
            $scope.tags = [];

            $scope.invoice_settling = {
                'cash': 0,
                'card': 0,
                'total_price': 0,
                'discount': 0,
                'tip': 0
            };
            $scope.serach_data_member = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.check_cash();
        };

        $scope.get_today_for_reserve = function () {
            var sending_data = {
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getTodayForReserve(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.today_date = data['today_for_reserve'];
                        $scope.get_left_reserves();
                        $scope.get_not_come_reserves();
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

        $scope.delete_reserve = function (reserve_id) {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch,
                "reserve_id": reserve_id
            };
            dashboardHttpRequest.deleteReserve(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_not_come_reserves();
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

        $scope.arrive_reserve = function (reserve_id) {
            var sending_data = {
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch,
                "reserve_id": reserve_id
            };
            dashboardHttpRequest.arriveReserve(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_left_reserves();
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

        $scope.get_left_reserves = function () {
            var sending_data = {
                "username": $rootScope.user_data.username,
                "branch": $rootScope.user_data.branch,
                "hour": 1,
                "minutes": 0,
                "date": $scope.today_date
            };
            dashboardHttpRequest.getAllLeftReserves(sending_data)
                .then(function (data) {

                    if (data['response_code'] === 2) {
                        $scope.left_reserves = data['reserves'];
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

        $scope.get_not_come_reserves = function () {
            var sending_data = {
                "username": $rootScope.user_data.username,
                "branch": $rootScope.user_data.branch,
                "date": $scope.today_date
            };
            dashboardHttpRequest.getAllNotComeReserves(sending_data)
                .then(function (data) {

                    if (data['response_code'] === 2) {
                        $scope.not_come_reserves = data['reserves'];
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

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {

                    if (data['response_code'] === 2) {
                        $rootScope.cash_data.cash_id = data['cash_id'];
                        $scope.get_all_invoices_state_base(data['cash_id']);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.cash_data.cash_id = 0;
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.get_all_invoices_state_base = function (cash_id) {
            var sending_data = {
                "username": $rootScope.user_data.username,
                "branch_id": $rootScope.user_data.branch,
                "cash_id": cash_id
            };
            dashboardHttpRequest.getAllInvoicesStateBase(sending_data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.wait_for_settle_invoices_data = data['wait_for_settle_invoices_data'];
                        $scope.wait_game_invoices_data = data['wait_game_invoices_data'];
                        $scope.playing_game_invoices_data = data['playing_game_invoices_data'];
                        $scope.ordered_invoices_data = data['ordered_invoices_data'];
                        $scope.not_order_invoices_data = data['not_order_invoices_data'];
                        $scope.end_game_invoices_data = data['end_game_invoices_data'];
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

        $scope.searchMember = function () {
            if ($scope.serach_data_member.search_word === '') {
                $scope.members = [];
            }
            else {
                dashboardHttpRequest.searchMember($scope.serach_data_member)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.members = data['members'];
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModalQ').modal('show');
                $('#addMemberModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModalQ').modal('hide');
                $('#addMemberModal').css('z-index', "");
            })(jQuery);
        };

        $scope.endCurrentGame = function (game_id) {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username,
                "game_id": parseInt(game_id)
            };
            dashboardHttpRequest.endCurrentGame(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoices_state_base($rootScope.cash_data.cash_id);
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

        $scope.do_not_want_order = function (invoice_id) {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username,
                "invoice_id": parseInt(invoice_id)
            };
            dashboardHttpRequest.doNotWantOrder(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoices_state_base($rootScope.cash_data.cash_id);
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

        $scope.change_game_state = function (invoice_id, state) {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username,
                "invoice_id": parseInt(invoice_id),
                "state": state
            };
            dashboardHttpRequest.changeGameState(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoices_state_base($rootScope.cash_data.cash_id);
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

        $scope.set_pay_modal_data = function (invoice_id, total_price, discount, tip) {
            $scope.invoice_settling.id = invoice_id;
            $scope.invoice_settling.total_price = total_price;
            $scope.invoice_settling.discount = discount;
            $scope.invoice_settling.tip = tip;
            $scope.payModalChangeNumber();
            $scope.open_modal('payModal');
        };

        $scope.settleInvoice = function () {
            var sending_data = {
                'invoice_id': $scope.invoice_settling.id,
                'cash': $scope.invoice_settling.cash,
                'card': $scope.invoice_settling.card,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.settleInvoiceSale(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.close_modal('payModal');
                        $scope.get_all_invoices_state_base($rootScope.cash_data.cash_id);
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
            $scope.invoice_settling.card = Number($scope.invoice_settling.total_price) - Number($scope.invoice_settling.cash) - Number($scope.invoice_settling.discount) + Number($scope.invoice_settling.tip);
        };

        $scope.start_invoice_game = function (invoice_id, invoice_index) {
            var sending_data = {
                'invoice_id': invoice_id,
                'card_number': $scope.wait_game_invoices_data[invoice_index].card_number,
                'numbers': $scope.wait_game_invoices_data[invoice_index].player_numbers,
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch
            };
            dashboardHttpRequest.startInvoiceGame(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoices_state_base($rootScope.cash_data.cash_id);
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

        $scope.check_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.checkCashExist(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_today_for_reserve();
                        $scope.get_today_cash();
                    }
                    else if (data['response_code'] === 3) {
                        $state.go('cash_manager.salon');
                    }
                }, function (error) {
                    $scope.error_message = 500;
                    $scope.openErrorModal();
                });
        };

        initialize();
    });