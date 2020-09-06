angular.module("dashboard")
    .controller("memberCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, offlineAPIHttpRequest) {
        var initialize = function () {
            $scope.gift_code_data = {
                "gift_code": "",
                "member_id": "",
                "username": $rootScope.user_data.username
            };
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    $("#expire_credit_date").datepicker();
                });
                $(document).ready(function () {
                    $("#start_credit_date").datepicker();
                });
            })(jQuery);
            $scope.new_credit_data = {
                'member_id': 0,
                'total_credit': 0,
                'expire_date': '',
                'expire_time': '00:00',
                'start_date': '',
                'start_time': '00:00',
                'credit_category': '',
                'username': $rootScope.user_data.username
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
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.serach_data_member = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.credit_categories = [
                {key: "BAR", name: "آیتم‌های بار"},
                {key: "KITCHEN", name: "آیتم‌های آشپزخانه"},
                {key: "OTHER", name: "آیتم‌های سایر"},
                {key: "SHOP", name: "محصولات فروشگاهی"},
                {key: "GAME", name: "بازی"}
            ];
            $scope.get_members_data($rootScope.user_data);
            $scope.config_clock();
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
                "member_id": member_id,
                "username": $rootScope.user_data.username
            };
            dashboardHttpRequest.memberCredits(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.member_credit_data = data['all_credits'];
                    }
                    else if (data['response_code'] === 3) {
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
            $rootScope.open_modal("showMemberProfileModal");
        };

        $scope.check_gift_code = function () {
            dashboardHttpRequest.checkGiftCode($scope.gift_code_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.show_member_profile_data($scope.gift_code_data.member_id);
                        $scope.gift_code_data.gift_code = "";
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
                        $scope.resetFrom();
                        $rootScope.close_modal("showMemberProfileModal");
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


        $scope.get_members_data = function (data) {
            dashboardHttpRequest.getMembers(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.members = data['members'];
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

        $scope.openAddMemberModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addMemberModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddMemberModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addMemberModal').modal('hide');
            })(jQuery);
        };

        $scope.addMember = function () {
            if (!$scope.new_member_data.card_number)
                 $scope.new_member_data.card_number = $scope.new_member_data.phone;
            dashboardHttpRequest.addMember($scope.new_member_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.create_member_offline(data['created_member']);
                        $scope.get_members_data($rootScope.user_data);
                        $scope.closeAddMemberModal();
                    }
                    else if (data['response_code'] === 3) {
                        if ($scope.new_member_data.card_number == $scope.new_member_data.phone)
                            $scope.new_member_data.card_number = '';
                        $scope.error_message = data['error_msg'];
                        $scope.openErrorModal();
                    }
                }, function (error) {
                    if ($scope.new_member_data.card_number == $scope.new_member_data.phone)
                        $scope.new_member_data.card_number = '';
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.searchMember = function () {
            if ($scope.serach_data_member.search_word === '') {
                $scope.get_members_data($rootScope.user_data);
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

        $scope.editMember = function (member_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'branch': $rootScope.user_data.branch,
                'member_id': member_id
            };
            dashboardHttpRequest.getMember(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
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
                            'branch': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openAddMemberModal();
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
            offlineAPIHttpRequest.create_member(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                    // $scope.error_message = error;
                    // $scope.openErrorModal();
                });
        };


        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addMemberModal').css('z-index', 1000);
                $('#showMemberProfileModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addMemberModal').css('z-index', "");
                $('#showMemberProfileModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
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
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.new_credit_data = {
                'member_id': 0,
                'total_credit': 0,
                'expire_date': '',
                'expire_time': '00:00',
                'start_date': '',
                'start_time': '00:00',
                'credit_category': '',
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddMemberModal();
        };
        initialize();
    });