angular.module("dashboard")
    .controller("memberCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, offlineAPIHttpRequest) {
        var initialize = function () {
            $scope.member_table_headers = [
                {
                    name: "نام مشتری",
                    key: "full_name"
                },
                {
                    name: "شماره موبایل",
                    key: "phone",
                    is_number: true
                },
                {
                    name: "شماره مشتری",
                    key: "card_number",
                    is_number: true
                }
            ];
            $scope.member_table_configs = {
                price_fields: [],
                has_detail_button: true,
                has_second_button_on_right_side: false,
                has_row_numbers: false,
                right_side_button_text: "وضعیت پروفایل"
            };

            $scope.gift_code_data = {
                "gift_code": "",
                "member_id": ""
            };

            $scope.serach_data_member = {
                'search_word': '',
                'branch': $rootScope.user_data.branch
            };

            $scope.get_members_data($rootScope.user_data);
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

        initialize();
    });