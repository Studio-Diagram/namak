angular.module("dashboard")
    .controller("buyBundleCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {

            $rootScope.is_page_loading = false;

            $scope.one_month = true;
            $scope.discount_amount = 0;

            $scope.AVAILABLE_BUNDLES = {
                "STANDARDNORMAL_30" :  100_000,
                "STANDARDNORMAL_90" :  300_000,
                "STANDARDNORMAL_365" : 1_000_000,

                "STANDARDBG_30" :  100_000,
                "STANDARDBG_90" :  300_000,
                "STANDARDBG_365" : 1_000_000,

                "ENTERPRISE_30" :  200_000,
                "ENTERPRISE_90" :  500_000,
                "ENTERPRISE_365" : 2_000_000,
            }

        };


        $scope.openBuyBundleModal = function (plan_type) {

            switch (plan_type) {
                case 'standard_normal':
                    $scope.plan_type = 'standard_normal';
                    $scope.chosen_bundle = "STANDARDNORMAL_";
                    $scope.chosen_bundle_plus_days = "STANDARDNORMAL_30";
                    $scope.one_month_price = $scope.AVAILABLE_BUNDLES.STANDARDNORMAL_30;
                    $scope.three_month_price = $scope.AVAILABLE_BUNDLES.STANDARDNORMAL_90;
                    $scope.twelve_month_price = $scope.AVAILABLE_BUNDLES.STANDARDNORMAL_365;
                    break;
                case 'standard_bg':
                    $scope.plan_type = 'standard_bg';
                    $scope.chosen_bundle = "STANDARDBG_";
                    $scope.chosen_bundle_plus_days = "STANDARDBG_30";
                    $scope.one_month_price = $scope.AVAILABLE_BUNDLES.STANDARDBG_30;
                    $scope.three_month_price = $scope.AVAILABLE_BUNDLES.STANDARDBG_90;
                    $scope.twelve_month_price = $scope.AVAILABLE_BUNDLES.STANDARDBG_365;
                    break;
            }

            $rootScope.open_modal('buyBundleModal');

        };


        $scope.buy_bundle = function () {
            var data = {
                "bundle": $scope.chosen_bundle_plus_days
            };
            if ($scope.entered_discount) data.discount_code = $scope.entered_discount;

            dashboardHttpRequest.buyBundle(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $window.location.href = data.redirect;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = error.data.error_msg;
                    $rootScope.open_modal('mainErrorModal');
                });
        };


        $scope.check_discount = function () {
            var data = {
                "bundle": $scope.chosen_bundle_plus_days,
                "code": $scope.entered_discount
            };
            dashboardHttpRequest.checkBundleDiscount(data)
                .then(function (data) {
                    $scope.discount_checked = true;
                    $scope.discount_applied = true;
                    $scope.discount_amount = data.amount;
                }, function (error) {
                    $scope.discount_checked = true;
                    $scope.discount_applied = false;
                });
        };

        $scope.add_days_to_bundle = function (days) {
            if (days == 30) {
                $scope.chosen_bundle_plus_days = $scope.chosen_bundle + "30";
                $scope.one_month = true;
                $scope.three_month = false;
                $scope.twelve_month = false;
            }
            if (days == 90) {
                $scope.chosen_bundle_plus_days = $scope.chosen_bundle + "90";
                $scope.one_month = false;
                $scope.three_month = true;
                $scope.twelve_month = false;
            }
            if (days == 365) {
                $scope.chosen_bundle_plus_days = $scope.chosen_bundle + "365";
                $scope.one_month = false;
                $scope.three_month = false;
                $scope.twelve_month = true;
            }

        };


        initialize();
    });