angular.module("dashboard")
    .controller("branchCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_branch_data = {
                'branch_id': 0,
                'name': '',
                'address': '',
                'start_time': '',
                'end_time': '',
                "guest_pricing": false,
                "min_paid_price": 5000,
                'game_data': [
                    {
                        "which_hour": 1,
                        "price_per_hour": 0
                    },
                    {
                        "which_hour": 2,
                        "price_per_hour": 0
                    }
                ],
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_branch = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.branchSearchWord = '';
            $scope.get_branches_data($rootScope.user_data);
            $scope.config_clock();
        };

        $scope.config_clock = function () {
            jQuery.noConflict();
            (function ($) {
                var choices = ["00", "15", "30", "45"];
                $('#start-time-clock').clockpicker({
                    donetext: 'تایید',
                    autoclose: true,
                    afterShow: function () {
                        $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                            return !($.inArray($(element).text(), choices) != -1)
                        }).remove();
                    },
                    afterDone: function () {
                        var seleceted_min = $('#start-time-clock').val().split(":")[1];
                        if (!choices.includes(seleceted_min)) {
                            $('#start-time-clock').val("");
                        }
                        else {
                            $scope.new_branch_data.start_time = $('#start-time-clock').val();
                        }
                    }
                });
                $('#end-time-clock').clockpicker({
                    donetext: 'تایید',
                    autoclose: true,
                    afterShow: function () {
                        $(".clockpicker-minutes").find(".clockpicker-tick").filter(function (index, element) {
                            return !($.inArray($(element).text(), choices) != -1)
                        }).remove();
                    },
                    afterHide: function () {
                        var seleceted_min = $('#end-time-clock').val().split(":")[1];
                        if (!choices.includes(seleceted_min)) {
                            $('#end-time-clock').val("");
                        }
                        else {
                            $scope.new_branch_data.end_time = $('#end-time-clock').val();
                        }
                    }
                });
            })(jQuery);
        };

        $scope.get_branches_data = function (data) {
            dashboardHttpRequest.getBranches(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.branches = data['branches'];
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

        $scope.openAddBranchModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addBranchModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddBranchModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addBranchModal').modal('hide');
            })(jQuery);
        };

        $scope.addBranch = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_branch_data.start_time = $('#start-time-clock').val();
                $scope.new_branch_data.end_time = $('#end-time-clock').val();
            })(jQuery);
            dashboardHttpRequest.addBranch($scope.new_branch_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_branches_data($rootScope.user_data);
                        $scope.resetFrom();
                        $scope.closeAddBranchModal();
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

        $scope.searchBranch = function () {
            if ($scope.search_data_branch.search_word === '') {
                $scope.get_branches_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchBranch($scope.search_data_branch)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.branches = data['branches'];
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

        $scope.editBranch = function (branch_id) {
            $scope.is_in_edit_mode = true;
            dashboardHttpRequest.getBranch(branch_id)
                .then(function (data) {
                        $scope.new_branch_data = {
                            'branch_id': data['branch']['id'],
                            'name': data['branch']['name'],
                            'address': data['branch']['address'],
                            'start_time': data['branch']['start_working_time'],
                            'end_time': data['branch']['end_working_time'],
                            'game_data': data['branch']['game_data'],
                            'min_paid_price': data['branch']['min_paid_price'],
                            'guest_pricing': data['branch']['guest_pricing']
                        };
                        $scope.openAddBranchModal();
                }, function (error) {
                    $scope.error_message = error.data.error_msg;
                    $scope.openErrorModal();
                });

        };

        $scope.resetFrom = function () {
            $scope.new_branch_data = {
                'branch_id': 0,
                'name': '',
                'address': '',
                'start_time': '',
                'end_time': '',
                "min_paid_price": 5000,
                "guest_pricing": false,
                'game_data': [
                    {
                        "which_hour": 1,
                        "price_per_hour": 0
                    },
                    {
                        "which_hour": 2,
                        "price_per_hour": 0
                    }
                ],
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddBranchModal();
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addBranchModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addBranchModal').css('z-index', "");
            })(jQuery);
        };

        initialize();
    });