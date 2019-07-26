angular.module("dashboard")
    .controller("memberCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_member_data = {
                'member_id': 0,
                'first_name': '',
                'last_name': '',
                'card_number': '',
                'year_of_birth': '',
                'month_of_birth': '',
                'day_of_birth': '',
                'phone': '',
                'intro': 'other',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.serach_data_member = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.get_members_data($rootScope.user_data);
        };

        $scope.get_members_data = function (data) {
            dashboardHttpRequest.getMembers(data)
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
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addMember($scope.new_member_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_members_data($rootScope.user_data);
                            $scope.closeAddMemberModal();
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
            else {
                dashboardHttpRequest.addMember($scope.new_member_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_members_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddMemberModal();
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

        $scope.getMember = function (member_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'member_id': member_id
            };
            dashboardHttpRequest.getMember(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['member'];
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


        $scope.editMember = function (member_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
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

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addMemberModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addMemberModal').css('z-index', "");
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
                'intro': 'other',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddMemberModal();
        };
        initialize();
    });