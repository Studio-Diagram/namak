angular.module("dashboard")
    .controller("memberCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, offlineAPIHttpRequest) {
        var initialize = function () {
            $scope.member_table_headers = [
                {
                    name: "نام مشتری",
                    key: "last_name"
                },
                {
                    name: "شماره تلفن",
                    key: "phone"
                },
                {
                    name: "شماره عضویت",
                    key: "card_number"
                }
            ];
            $scope.member_table_configs = {
                price_fields: [],
                has_detail_button: true,
                has_second_button_on_right_side: true,
                has_row_numbers: false,
                right_side_button_text: "وضعیت پروفایل"
            };

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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
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
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
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

        $scope.get_members_data = function (data) {
            dashboardHttpRequest.getMembers(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.members = data['members'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
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
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {
                        $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                    });
            }
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

        $scope.resetForm = function () {
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

        initialize();
    });