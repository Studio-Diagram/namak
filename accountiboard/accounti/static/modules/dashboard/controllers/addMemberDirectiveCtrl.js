angular.module("dashboard")
    .controller("addMemberDirectiveCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, offlineAPIHttpRequest) {
        var initialize = function () {
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
                'member_id': 0,
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

            $scope.init_assets_member_page();
        };

        $scope.init_assets_member_page = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#expire_credit_date").datepicker();
                });
                $(document).ready(function () {
                    $("#start_credit_date").datepicker();
                });
            })(jQuery);

            $scope.config_clock();
            $scope.set_today_for_credit();
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

        $scope.show_member_profile_data = function (member_id) {
            $scope.new_credit_data.member_id = member_id;
            $scope.gift_code_data.member_id = member_id;
            var sending_data = {
                "member_id": member_id
            };
            dashboardHttpRequest.memberCredits(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.member_credit_data = data['all_credits'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
            $rootScope.open_modal("showMemberProfileModal");
        };

        $scope.create_credit = function () {
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
                        $scope.resetForm();
                        $rootScope.close_modal("showMemberProfileModal");
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.addMember = function () {
            dashboardHttpRequest.addMember($scope.new_member_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.create_member_offline(data['created_member']);
                        $scope.get_members_data($rootScope.user_data);
                        $scope.close_modal('addMemberModal');
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });
        };

        $scope.editMember = function (member_id) {
            var data = {
                'branch': $rootScope.user_data.branch,
                'member_id': member_id
            };
            dashboardHttpRequest.getMember(data)
                .then(function (data) {
                    $scope.new_member_data = {
                        'member_id': data['member']['id'],
                        'first_name': data['member']['first_name'],
                        'last_name': data['member']['last_name'],
                        'card_number': data['member']['card_number'],
                        'year_of_birth': data['member']['year_of_birth'],
                        'month_of_birth': data['member']['month_of_birth'],
                        'day_of_birth': data['member']['day_of_birth'],
                        'phone': data['member']['phone'],
                        'intro': data['member']['intro'],
                        'branch': $rootScope.user_data.branch
                    };
                    $rootScope.open_modal('addMemberModal');
                }, function (error) {
                });

        };

        $scope.create_member_offline = function (online_server_response) {
            var sending_data = {
                'payload': {
                    "last_name": online_server_response['last_name'],
                    "card_number": online_server_response['card_number'],
                    "method": online_server_response['method'],
                    "member_primary_key": online_server_response['member_primary_key']
                }
            };
            offlineAPIHttpRequest.create_member(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                });
        };

        $scope.set_today_for_credit = function () {
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

        $scope.reset_member_form = function () {
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
                'member_id': 0,
                'total_credit': 0,
                'expire_date': '',
                'expire_time': '00:00',
                'start_date': '',
                'start_time': '00:00',
                'credit_category': ''
            };

            $scope.member_credit_data = [];
        };


        initialize();
    });