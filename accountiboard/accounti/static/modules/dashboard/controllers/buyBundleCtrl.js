angular.module("dashboard")
    .controller("buyBundleCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $rootScope.is_page_loading = false;
            $scope.discount_amount = 0;

            $scope.AVAILABLE_BUNDLES = {
                "STANDARDNORMAL": {
                    30: {
                        "name": "یک ماهه حرفه ای",
                        "price": 100_000,
                    },
                    90: {
                        "name": "سه ماهه حرفه ای",
                        "price": 300_000,
                    },
                    365: {
                        "name": "یک ساله حرفه ای",
                        "price": 1_000_000,
                    },
                },
                "STANDARDBG": {
                    30: {
                        "name": "یک ماهه کافه بازی",
                        "price": 200_000,
                    },
                    90: {
                        "name": "سه ماهه کافه بازی",
                        "price": 600_000,
                    },
                    365: {
                        "name": "یک ساله کافه بازی",
                        "price": 2_000_000,
                    },
                },
            };

            $scope.days_in_farsi = {
                30: "یک ماهه",
                90: "سه ماهه",
                365: "یک ساله",
            };


        };


        $scope.openBuyBundleModal = function (plan_type) {
            $scope.current_days_selection = 30;
            $scope.entered_discount = "";
            $scope.discount_checked = false;
            $scope.discount_applied = false;
            $scope.discount_amount = 0;

            switch (plan_type) {
                case 'STANDARDNORMAL':
                    $scope.plan_type = 'STANDARDNORMAL';
                    $scope.current_bundle_selection = $scope.AVAILABLE_BUNDLES['STANDARDNORMAL'][30]
                    break;
                case 'STANDARDBG':
                    $scope.plan_type = 'STANDARDBG';
                    $scope.current_bundle_selection = $scope.AVAILABLE_BUNDLES['STANDARDBG'][30]
                    break;
            }

            $scope.chosen_bundle_plus_days = $scope.plan_type + "_" + $scope.current_days_selection;
            $rootScope.open_modal('buyBundleModal');

        };


        $scope.buy_bundle = function () {
            $scope.disable_buy_button = true;
            var data = {
                "bundle": $scope.chosen_bundle_plus_days,
                "discount_code": $scope.entered_discount
            };

            dashboardHttpRequest.buyBundle(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $window.location.href = data.redirect;
                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $rootScope.error_message = error.data.error_msg;
                    $scope.disable_buy_button = false;
                    $rootScope.open_modalv2('mainErrorModalv2', 'buyBundleModal');
                });
        };


        $scope.check_discount = function () {
            var data = {
                "bundle": $scope.chosen_bundle_plus_days,
                "discount_code": $scope.entered_discount
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

        $scope.select_bundle = function (days, bundle_data) {
            $scope.discount_checked = false;
            $scope.discount_applied = false;
            $scope.discount_amount = 0;
            $scope.current_days_selection = days;
            $scope.current_bundle_selection = bundle_data;
            $scope.chosen_bundle_plus_days = $scope.plan_type + "_" + days;
        };

        $scope.clear_discount = function () {
            $scope.discount_checked = false;
            $scope.discount_applied = false;
            $scope.discount_amount = 0;
        }


        initialize();
    });