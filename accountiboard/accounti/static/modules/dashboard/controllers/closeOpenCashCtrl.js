angular.module("dashboard")
    .controller("closeOpenCashCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.get_all_cashes();
        };

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.log_out = function () {
            dashboardHttpRequest.logOut($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $window.location.href = '/';
                        $rootScope.user_data = {
                            "username": '',
                            "branch": ''
                        };
                    }
                    else if (data['response_code'] === 3) {
                        $window.location.href = '/';
                        $rootScope.user_data = {
                            "username": '',
                            "branch": ''
                        };
                    }
                }, function (error) {
                    console.log(error);
                });
        };


        $scope.close_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.closeCash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.log_out();
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

        $scope.get_all_cashes = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getAllCashes(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.all_cashes = data['all_cashes'];
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

        $scope.openPermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closePermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        initialize();
    });