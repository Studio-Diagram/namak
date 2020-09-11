angular.module("dashboard")
    .controller("branchDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.branch_data = {
                name: '',
                address: '',
                start_working_time: '',
                end_working_time: ''
            };
            $scope.get_branch_data();
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
                            $scope.branch_data.start_working_time = $('#start-time-clock').val();
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
                            $scope.branch_data.end_working_time = $('#end-time-clock').val();
                        }
                    }
                });
            })(jQuery);
        };

        $scope.get_branch_data = function () {
            dashboardHttpRequest.getBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.setDefaultData(data.branch);
                    $scope.show_branch_data = data.branch;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.open_modal('errorModal', 'editBranchDetailsModal');
                });
        };

        $scope.updateBranch = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.branch_data.start_working_time = $('#start-time-clock').val();
                $scope.branch_data.end_working_time = $('#end-time-clock').val();
            })(jQuery);
            dashboardHttpRequest.updateBranch($rootScope.user_data.branch, $scope.branch_data)
                .then(function (data) {
                    $scope.setDefaultData(data.branch);
                    $scope.show_branch_data = data.branch;
                    $scope.close_modal('editBranchDetailsModal');
                }, function (error) {
                    $scope.error_message = error;
                    $rootScope.open_modal('errorModal', 'editBranchDetailsModal');
                });
        };

        $scope.setDefaultData = function (data) {
            $scope.branch_data.name = data.name;
            $scope.branch_data.address = data.address;
            $scope.branch_data.start_working_time = data.start_working_time;
            $scope.branch_data.end_working_time = data.end_working_time;
        };

        initialize();
    });