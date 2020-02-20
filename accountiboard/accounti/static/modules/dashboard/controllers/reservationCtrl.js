angular.module("dashboard")
    .controller("reservationCtrl", function ($scope, $interval, $rootScope, $filter, $state, $http, $timeout, $window, dashboardHttpRequest, $compile, $stateParams) {
            var initialize = function () {
                $scope.tomorrow_date = "";
                $scope.fixed_date = "";
                jQuery.noConflict();
                (function ($) {
                    $(document).ready(function () {
                        $("#datepicker").datepicker();
                    });
                })(jQuery);
                $scope.error_message = '';
                $scope.all_today_reserves = [];
                $scope.starting_selected_time = {
                    "is_hour": 0,
                    "time": 0,
                    "is_fill": 0,
                    'class_name': '',
                    'table_name': '',
                    'index': ''
                };
                $scope.ending_selected_time = {
                    "is_hour": 0,
                    "time": 0,
                    "is_fill": 0,
                    'class_name': '',
                    'table_name': '',
                    'index': ''
                };
                $scope.new_reserve_data = {
                    'reserve_id': 0,
                    'numbers': 0,
                    'start_time': '',
                    'end_time': '',
                    'customer_name': '',
                    'phone': '',
                    'reserve_date': '',
                    'reserve_state': '',
                    'tables_id': [],
                    'username': $rootScope.user_data.username,
                    'branch': $rootScope.user_data.branch
                };
                $scope.config_clock();
                $scope.get_today_for_reserve();
                $scope.get_tables_data_for_main_page($rootScope.user_data);
                $scope.get_working_time();

                // Avoid Closing Drop down when clicking inside
                $(document).on('click', '.dropdown-menu', function (e) {
                    e.stopPropagation();
                });

                $window.onkeyup = function (event) {
                    if (event.keyCode === 27) {
                        jQuery.noConflict();
                        (function ($) {
                            $($scope.starting_selected_time.class_name).css("background", "none");
                            $('.tooltipM').fadeOut()
                        })(jQuery);
                        $scope.starting_selected_time = {
                            "is_hour": 0,
                            "time": 0,
                            "is_fill": 0,
                            'class_name': '',
                            'table_name': '',
                            'index': ''
                        };
                        $scope.ending_selected_time = {
                            "is_hour": 0,
                            "time": 0,
                            "is_fill": 0,
                            'class_name': '',
                            'table_name': '',
                            'index': ''
                        };
                        $scope.new_reserve_data.tables_id = [];
                        $scope.closeAddModal();
                        $scope.closeCompleteReserveModal();
                        $scope.closeAddWalkedModal();
                        $scope.closeWaitingListModal();
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
                };
                $timeout(function () {
                    $scope.grey_past_hours();
                }, 1000);
            };

            $scope.grey_past_hours = function () {
                if ($scope.today_date === $scope.fixed_date) {
                    var diff = 1000 * 60 * 15;
                    var date = new Date();
                    var rounded = new Date(Math.round(date.getTime() / diff) * diff);
                    if ((Number($scope.working_times[0].hour) === rounded.getHours() && Number($scope.working_times[0].minute) > rounded.getMinutes()) || Number($scope.working_times[0].hour) > rounded.getHours()) {
                        return
                    }
                    for (var i = 0; i < $scope.working_times.length; i++) {
                        if (Number($scope.working_times[i].hour) === rounded.getHours() && Number($scope.working_times[i].minute) === rounded.getMinutes()) {
                            break
                        }
                        jQuery.noConflict();
                        (function ($) {
                            $('.reservationCell.' + "H" + $scope.working_times[i].hour + "M" + $scope.working_times[i].minute).css("background", "var(--pageBorder)");
                            $('.reservationCell.' + "H" + $scope.working_times[i].hour + "M" + $scope.working_times[i].minute).css("border-color", "var(--pageBG)");
                        })(jQuery);
                    }
                }
            };

            $scope.cross_hover = function (hour, min, table, event) {
                if ($scope.last_table_hover) {
                    jQuery.noConflict();
                    (function ($) {
                        $('#tablename-' + $scope.last_table_hover.table_name).css("background", "none");
                    })(jQuery);
                }
                if ($scope.last_row_hover) {
                    jQuery.noConflict();
                    (function ($) {
                        $('.reservationCell.' + $scope.last_row_hover).css("background", "none");
                    })(jQuery);
                }
                $scope.last_row_hover = 'H' + hour + 'M' + min;
                $scope.last_table_hover = table;
                jQuery.noConflict();
                (function ($) {
                    $('#tablename-' + table.table_name).css("background", "#fff");
                    $('.' + 'H' + hour + 'M' + min).css("background", "#fff");
                })(jQuery);
                if ($scope.starting_selected_time.class_name) {
                    jQuery.noConflict();
                    (function ($) {
                        $($scope.starting_selected_time.class_name).css("background", "rgb(197, 197, 197)");
                    })(jQuery);
                }
                $scope.grey_past_hours();
            };

            $scope.clicking_reserve = function (hour, min, is_hour, table, event, index) {
                var class_name = event.target.className;
                if (class_name.split(" ")[1] === "reservationCell") {
                    if ($scope.ending_selected_time.is_fill === 0) {
                        if ($scope.starting_selected_time.is_fill === 0) {
                            for (var j = 0; j < $scope.categorized_tables_data.length; j++) {
                                for (var i = 0; i < $scope.categorized_tables_data[j].tables.length; i++) {
                                    if ($scope.categorized_tables_data[j].tables[i].table_id === table.table_id) {
                                        $scope.categorized_tables_data[j].tables[i].is_checked = 1;
                                        $scope.categorized_tables_data[j].tables[i].is_checked_m = 1;
                                        $scope.new_reserve_data.tables_id.push(table.table_id);
                                        break;
                                    }
                                }
                            }
                            if (Number(is_hour) === 0) {
                                $scope.starting_selected_time.is_hour = 0;
                                $scope.starting_selected_time.time = hour + ":" + min;
                                $scope.starting_selected_time.is_fill = 1;
                                $scope.starting_selected_time.class_name = event.target;
                                $scope.starting_selected_time.table_name = table.table_name;
                                $scope.starting_selected_time.index = index;
                            }
                            else if (Number(is_hour) === 1) {
                                $scope.starting_selected_time.is_hour = 1;
                                $scope.starting_selected_time.time = hour + ":" + min;
                                $scope.starting_selected_time.is_fill = 1;
                                $scope.starting_selected_time.class_name = event.target;
                                $scope.starting_selected_time.table_name = table.table_name;
                                $scope.starting_selected_time.index = index;
                            }
                            jQuery.noConflict();
                            (function ($) {
                                $(event.target).css("background", "rgb(197, 197, 197)");
                            })(jQuery);
                        }
                        else if ($scope.starting_selected_time.is_fill === 1) {
                            hour = $scope.working_times[index + 1].hour;
                            min = $scope.working_times[index + 1].minute;
                            is_hour = $scope.working_times[index + 1].is_hour;
                            if ($scope.starting_selected_time.table_name === table.table_name && index > $scope.starting_selected_time.index) {
                                if (Number(is_hour) === 0) {
                                    $scope.ending_selected_time.is_hour = 0;
                                    $scope.ending_selected_time.time = hour + ":" + min;
                                    $scope.ending_selected_time.is_fill = 1;
                                    $scope.ending_selected_time.class_name = event.target;
                                }
                                else if (Number(is_hour) === 1) {
                                    $scope.ending_selected_time.is_hour = 1;
                                    $scope.ending_selected_time.time = hour + ":" + min;
                                    $scope.ending_selected_time.is_fill = 1;
                                    $scope.ending_selected_time.class_name = event.target;
                                }
                                $scope.new_reserve_data.start_time = $scope.starting_selected_time.time;
                                $scope.new_reserve_data.end_time = $scope.ending_selected_time.time;
                                jQuery.noConflict();
                                (function ($) {
                                    $('.tooltipM').fadeIn().css(({left: event.pageX, top: event.pageY}));
                                })(jQuery);
                            }
                        }
                    }
                }
            };


            $scope.get_working_time = function () {
                var sending_data = {
                    'username': $rootScope.user_data.username,
                    'branch': $rootScope.user_data.branch
                };
                dashboardHttpRequest.getWorkingTime(sending_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.working_times = data['working_data'];
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


            $scope.get_today_for_reserve = function () {
                jQuery.noConflict();
                (function ($) {
                    $scope.all_today_reserves.forEach(function insert_code(item, index) {
                        var div_data = "";
                        $('#tablename-' + item.table_name).find($(".H" + item.start_time_hour + "M" + item.start_time_min)).html(div_data);
                    });
                })(jQuery);
                var sending_data = {
                    'branch': $rootScope.user_data.branch,
                    'username': $rootScope.user_data.username
                };
                dashboardHttpRequest.getTodayForReserve(sending_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.fixed_date = data['today_for_reserve'];
                            $scope.today_date = data['today_for_reserve'];
                            $scope.tomorrow_date = data['tomorrow_for_reserve'];
                            $scope.new_reserve_data.reserve_date = $scope.fixed_date;
                            $scope.get_reserves_data($rootScope.user_data, $scope.fixed_date);
                        }
                        else if (data['response_code'] === 3) {

                        }
                    }, function (error) {
                        console.log(error);
                    });
            };

            $scope.changeTableCheckBox = function (is_checked, table_id) {
                var index_of_table_id = $scope.new_reserve_data.tables_id.indexOf(table_id);
                if (index_of_table_id === -1) {
                    $scope.new_reserve_data.tables_id.push(table_id);
                }
                else {
                    $scope.new_reserve_data.tables_id.splice(index_of_table_id, 1);
                }
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
                            var diff = 1000 * 60 * 15;
                            var date = new Date();
                            var rounded = new Date(Math.round(date.getTime() / diff) * diff);
                            $scope.new_reserve_data.start_time = rounded.getHours() + ":" + rounded.getMinutes();
                            $scope.add_reserve();
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

            $scope.delete_reserve = function (reserve_id) {
                var sending_data = {
                    'username': $rootScope.user_data.username,
                    'branch': $rootScope.user_data.branch,
                    "reserve_id": reserve_id
                };
                dashboardHttpRequest.deleteReserve(sending_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.change_date();
                            $scope.closePermissionModal();
                            $scope.closeAddModal();
                            $scope.closeAddWalkedModal();
                            $scope.get_waiting_list();
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

            $scope.kill_grey_background = function () {
                if ($scope.today_date !== $scope.fixed_date) {
                    for (var i = 0; i < $scope.working_times.length; i++) {
                        jQuery.noConflict();
                        (function ($) {
                            $('.reservationCell.' + "H" + $scope.working_times[i].hour + "M" + $scope.working_times[i].minute).css("background", "none");
                            $('.reservationCell.' + "H" + $scope.working_times[i].hour + "M" + $scope.working_times[i].minute).css("border-color", "var(--pageBorder)");
                        })(jQuery);
                    }
                }
            };

            $scope.change_date = function () {
                $scope.fixed_date = $("#datepicker").val();
                $scope.new_reserve_data.reserve_date = $scope.fixed_date;
                jQuery.noConflict();
                (function ($) {
                    $scope.all_today_reserves.forEach(function insert_code(item, index) {
                        var div_data = "";
                        $('#tablename-' + item.table_name).find($(".H" + item.start_time_hour + "M" + item.start_time_min)).html(div_data);
                    });
                })(jQuery);
                $scope.grey_past_hours();
                $scope.kill_grey_background();
                $scope.get_reserves_data($rootScope.user_data, $scope.fixed_date);
            };

            $scope.get_tomorrow_reserves = function () {
                $scope.fixed_date = $scope.tomorrow_date;
                $scope.new_reserve_data.reserve_date = $scope.tomorrow_date;
                jQuery.noConflict();
                (function ($) {
                    $scope.all_today_reserves.forEach(function insert_code(item, index) {
                        var div_data = "";
                        $('#tablename-' + item.table_name).find($(".H" + item.start_time_hour + "M" + item.start_time_min)).html(div_data);
                    });
                })(jQuery);
                $scope.kill_grey_background();
                $scope.get_reserves_data($rootScope.user_data, $scope.tomorrow_date);
            };


            $scope.get_tables_data_for_main_page = function (data) {
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
                $scope.max_category_size = 0;
                for (var j = 0; j < $scope.categorized_tables_data.length; j++) {
                    if ($scope.max_category_size < $scope.categorized_tables_data[j].tables.length) {
                        $scope.max_category_size = $scope.categorized_tables_data[j].tables.length;
                    }
                }
            };

            $scope.get_tables_data = function () {
                for (var j = 0; j < $scope.categorized_tables_data.length; j++) {
                    for (var i = 0; i < $scope.categorized_tables_data[j].tables.length; i++) {
                        $scope.categorized_tables_data[j].tables[i].is_checked = 0;
                        $scope.categorized_tables_data[j].tables[i].is_checked_m = 0;
                    }
                }
            };

            $scope.get_reserves_data = function (data, date) {
                var sending_data = {
                    "username": data.username,
                    "branch": data.branch,
                    "date": date
                };
                dashboardHttpRequest.getAllReserves(sending_data)
                    .then(function (data) {
                        $rootScope.is_page_loading = false;
                        if (data['response_code'] === 2) {
                            $scope.all_today_reserves = data['all_today_reserves'];
                            jQuery.noConflict();
                            (function ($) {
                                $scope.all_today_reserves.forEach(function insert_code(item, index) {
                                    var div_data = $compile("<div ng-click='edit_reserve(" + item.id + ")' class=\"reservationItem " + item.reserve_state + " " + item.duration_class_name + "\" role=\"button\" href=\"\">\n" +
                                        "                                        <span class=\"reservationCount\"><i class=\"fas fa-users\"></i>" + $filter('persianNumber')(item.numbers) + "</span>\n" +
                                        "                                        <span class=\"reservationName\">\n" +
                                        "                                            " + item.customer_name + "\n" +
                                        "                                        </span>\n" +
                                        "                                    </div>")($scope);
                                    $('#tablename-' + item.table_name).find($(".H" + item.start_time_hour + "M" + item.start_time_min)).html(div_data);
                                });
                            })(jQuery);
                            $scope.grey_past_hours();
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $rootScope.is_page_loading = false;
                        $scope.error_message = 500;
                        $scope.openErrorModal();
                    });
            };

            $scope.get_waiting_list = function () {
                var sending_data = {
                    "username": $rootScope.user_data.username,
                    "branch": $rootScope.user_data.branch,
                    "date": $scope.today_date
                };
                dashboardHttpRequest.getWaitingList(sending_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.waiting_list = data['all_today_waiting_list'];
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

            $scope.add_reserve = function () {
                dashboardHttpRequest.addReserve($scope.new_reserve_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.change_date();
                            $scope.closeAddModal();
                            $scope.closeAddWalkedModal();
                            $scope.closeCompleteReserveModal();
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

            $scope.add_waiting_list = function () {
                dashboardHttpRequest.addWaitingList($scope.new_reserve_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.new_reserve_data.customer_name = "";
                            $scope.new_reserve_data.start_time = "";
                            $scope.new_reserve_data.numbers = 0;
                            $scope.new_reserve_data.phone = "";
                            $scope.get_waiting_list();
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

            $scope.edit_reserve = function (reserve_id) {
                $scope.is_in_edit_mode_reserve = true;
                var data = {
                    'username': $rootScope.user_data.username,
                    'reserve_id': reserve_id
                };
                dashboardHttpRequest.getReserve(data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.tables = data['reserve_data']['tables'];
                            $scope.new_reserve_data = {
                                'reserve_id': data['reserve_data']['reserve_id'],
                                'numbers': data['reserve_data']['numbers'],
                                'start_time': data['reserve_data']['start_time'],
                                'end_time': data['reserve_data']['end_time'],
                                'customer_name': data['reserve_data']['customer_name'],
                                'phone': data['reserve_data']['phone'],
                                'reserve_date': $scope.fixed_date,
                                'reserve_state': data['reserve_data']['reserve_state'],
                                'tables_id': data['reserve_data']['tables_id'],
                                'username': $rootScope.user_data.username,
                                'branch': $rootScope.user_data.branch
                            };
                            for (var m = 0; m < $scope.new_reserve_data.tables_id.length; m++) {
                                var table_id = $scope.new_reserve_data.tables_id[m];
                                for (var j = 0; j < $scope.categorized_tables_data.length; j++) {
                                    for (var i = 0; i < $scope.categorized_tables_data[j].tables.length; i++) {
                                        if ($scope.categorized_tables_data[j].tables[i].table_id === table_id) {
                                            $scope.categorized_tables_data[j].tables[i].is_checked = 1;
                                            $scope.categorized_tables_data[j].tables[i].is_checked_m = 1;
                                            break;
                                        }
                                    }
                                }
                            }
                            if ($scope.new_reserve_data.reserve_state === "walked") {
                                $scope.openAddWalkedModal();
                            }
                            else {
                                $scope.openAddModal();
                            }
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


            $scope.openErrorModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#errorModal').modal('show');
                    $('#addReservationModal').css('z-index', 1000);
                    $('#addWalkedModal').css('z-index', 1000);
                })(jQuery);
            };

            $scope.closeErrorModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#errorModal').modal('hide');
                    $('#addReservationModal').css('z-index', "");
                    $('#addWalkedModal').css('z-index', "");
                })(jQuery);
            };

            $scope.openAddModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#addReservationModal').modal('show');
                })(jQuery);
                $scope.new_reserve_data.reserve_state = 'waiting';
            };

            $scope.closeAddModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#addReservationModal').modal('hide');
                    $scope.resetFrom();
                })(jQuery);
            };

            $scope.openAddWalkedModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#addWalkedModal').modal('show');
                })(jQuery);
                $scope.new_reserve_data.reserve_state = 'walked';
                $scope.new_reserve_data.customer_name = 'حضوری';
                $scope.new_reserve_data.phone = "NO_PHONE";
            };

            $scope.closeAddWalkedModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#addWalkedModal').modal('hide');
                    $scope.resetFrom();
                })(jQuery);
            };

            $scope.openWaitingListModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#waitingListModal').modal('show');
                })(jQuery);
                $scope.get_waiting_list();
                $scope.new_reserve_data.reserve_state = 'call_waiting';
                $scope.new_reserve_data.new_reserve_data = $scope.today_date;
            };

            $scope.closeWaitingListModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#waitingListModal').modal('hide');
                    $scope.resetFrom();
                })(jQuery);
            };

            $scope.openCompleteReserveModal = function (reserve_kind) {
                $scope.new_reserve_data.reserve_state = reserve_kind;
                jQuery.noConflict();
                (function ($) {
                    $('#completeReserveModal').modal('show');
                })(jQuery);
            };

            $scope.closeCompleteReserveModal = function () {
                jQuery.noConflict();
                (function ($) {
                    $('#completeReserveModal').modal('hide');
                    $('.tooltipM').fadeOut();
                    $scope.resetFrom();
                })(jQuery);
            };

            $scope.openPermissionModal = function (will_be_deleted) {
                $scope.reserve_will_delete = will_be_deleted;
                jQuery.noConflict();
                (function ($) {
                    $('#permissionModal').modal('show');
                    $('#addReservationModal').css('z-index', 1000);
                    $('#completeReserveModal').css('z-index', 1000);
                    $('#addWalkedModal').css('z-index', 1000);
                })(jQuery);
            };

            $scope.closePermissionModal = function () {
                $scope.reserve_will_delete = 0;
                jQuery.noConflict();
                (function ($) {
                    $('#permissionModal').modal('hide');
                    $('#addReservationModal').css('z-index', "");
                    $('#completeReserveModal').css('z-index', "");
                    $('#addWalkedModal').css('z-index', "");
                })(jQuery);
            };

            $scope.gone_reserve = function () {
                var diff = 1000 * 60 * 15;
                var date = new Date();
                var rounded = new Date(Math.round(date.getTime() / diff) * diff);
                $scope.new_reserve_data.end_time = rounded.getHours() + ":" + rounded.getMinutes();
                $scope.add_reserve();
            };

            $scope.config_clock = function () {
                jQuery.noConflict();
                (function ($) {
                    var choices = ["00", "15", "30", "45"];
                    $('#start-time-clock-1').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#start-time-clock-1').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#start-time-clock-1').val("");
                            }
                            else {
                                $scope.new_reserve_data.start_time = $('#start-time-clock-1').val();
                            }
                        }
                    });
                    $('#end-time-clock-1').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#end-time-clock-1').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#end-time-clock-1').val("");
                            }
                            else {
                                $scope.new_reserve_data.end_time = $('#end-time-clock-1').val();
                            }
                        }
                    });
                    $('#start-time-clock-2').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#start-time-clock-2').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#start-time-clock-2').val("");
                            }
                            else {
                                $scope.new_reserve_data.start_time = $('#start-time-clock-2').val();
                            }
                        }
                    });
                    $('#end-time-clock-2').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#end-time-clock-2').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#end-time-clock-2').val("");
                            }
                            else {
                                $scope.new_reserve_data.end_time = $('#end-time-clock-2').val();
                            }
                        }
                    });
                    $('#start-time-clock-3').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#start-time-clock-3').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#start-time-clock-3').val("");
                            }
                            else {
                                $scope.new_reserve_data.start_time = $('#start-time-clock-3').val();
                            }
                        }
                    });
                    $('#end-time-clock-3').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#end-time-clock-3').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#end-time-clock-3').val("");
                            }
                            else {
                                $scope.new_reserve_data.end_time = $('#end-time-clock-3').val();
                            }
                        }
                    });
                    $('#start-time-clock-waiting-list').clockpicker({
                        donetext: 'تایید',
                        autoclose: true,
                        afterShow: function () {
                            $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                                return !($.inArray($(element).text(), choices) != -1)
                            }).remove();
                        },
                        afterDone: function () {
                            var seleceted_min = $('#start-time-clock-waiting-list').val().split(":")[1];
                            if (!choices.includes(seleceted_min)) {
                                $('#start-time-clock-waiting-list').val("");
                            }
                            else {
                                $scope.new_reserve_data.start_time = $('#start-time-clock-waiting-list').val();
                            }
                        }
                    });
                })(jQuery);
            };

            $scope.resetFrom = function () {
                $scope.get_tables_data();
                $scope.new_reserve_data = {
                    'reserve_id': 0,
                    'numbers': 0,
                    'start_time': '',
                    'end_time': '',
                    'customer_name': '',
                    'phone': '',
                    'reserve_date': $scope.new_reserve_data.reserve_date,
                    'reserve_state': '',
                    'tables_id': [],
                    'username': $rootScope.user_data.username,
                    'branch': $rootScope.user_data.branch
                };
                jQuery.noConflict();
                (function ($) {
                    $($scope.starting_selected_time.class_name).css("background", "none");
                })(jQuery);
                $scope.starting_selected_time = {
                    "is_hour": 0,
                    "hour": 0,
                    "minute": 0,
                    "is_fill": 0,
                    'class_name': ''
                };
                $scope.ending_selected_time = {
                    "is_hour": 0,
                    "hour": 0,
                    "minute": 0,
                    "is_fill": 0,
                    'class_name': ''
                };
            };

            initialize();
        }
    );