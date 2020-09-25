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
                }, function (error) {});

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
                }, function (error) {});
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
        };


        initialize();
    });