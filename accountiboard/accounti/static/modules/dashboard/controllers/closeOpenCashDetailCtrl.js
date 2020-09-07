angular.module("dashboard")
    .controller("closeOpenCashDetailCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $stateParams) {
        var initialize = function () {
            $scope.error_message = '';
            $scope.cash_id = $stateParams.cash_id;
            $scope.get_cash();
        };

        $scope.get_cash = function () {
            dashboardHttpRequest.getCash($scope.cash_id)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.current_cash = data;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error.data.error_msg;
                    $scope.openErrorModal();
                });

        };

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
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



        initialize();
    });