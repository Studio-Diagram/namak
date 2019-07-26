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
        };

        $scope.get_branches_data = function (data) {
            dashboardHttpRequest.getBranches(data)
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
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addBranch($scope.new_branch_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_branches_data($rootScope.user_data);
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
            }
            else {
                dashboardHttpRequest.addBranch($scope.new_branch_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_branches_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddEmployeeModal();
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

        $scope.getBranch = function (branch_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'branch_id': branch_id
            };
            dashboardHttpRequest.getBranch(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['branch'];
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


        $scope.editBranch = function (branch_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
                'branch_id': branch_id
            };
            dashboardHttpRequest.getBranch(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_branch_data = {
                            'branch_id': data['branch']['id'],
                            'name': data['branch']['name'],
                            'address': data['branch']['address'],
                            'start_time': data['branch']['start_time'],
                            'end_time': data['branch']['end_time']
                        };
                        $scope.openAddBranchModal();
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

        $scope.resetFrom = function () {
            $scope.new_branch_data = {
                'branch_id': 0,
                'name': '',
                'address': '',
                'start_time': '',
                'end_time': '',
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