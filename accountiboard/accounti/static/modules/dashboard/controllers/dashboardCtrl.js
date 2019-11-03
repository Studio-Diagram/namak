angular.module("dashboard")
    .controller("dashboardCtrl", function ($scope, $rootScope, $filter, $state, $interval, $http, $location, $timeout, dashboardHttpRequest, $window) {
        var initialize = function () {
            $rootScope.is_page_loading = true;
            if (localStorage.user && localStorage.branch) {
                $rootScope.user_data = {
                    "username": JSON.parse(localStorage.user),
                    "branch": JSON.parse(localStorage.branch)
                };
                $rootScope.cash_data = {
                    'cash_id': 0
                };
                $rootScope.get_today_var = $scope.get_today();
                $scope.is_user_login($rootScope.user_data);
                //$scope.check_cash($rootScope.user_data);
                $scope.get_today_cash();
            }
            else {
                window.location.replace("/");
            }

            $window.onkeyup = function (event) {
                if (event.ctrlKey && event.keyCode === 49) {

                }
                if (event.ctrlKey && event.keyCode === 50) {
                    $state.go('cash_manager.salon');
                }
                if (event.ctrlKey && event.keyCode === 51) {
                    $state.go('reservation');
                }
                if (event.ctrlKey && event.keyCode === 52) {
                    $state.go('member');
                }
                if (event.ctrlKey && event.keyCode === 53) {
                    $state.go('boardgame');
                }
                if (event.ctrlKey && event.keyCode === 54) {

                }
                if (event.ctrlKey && event.keyCode === 55) {
                    $state.go('account_manager.buy');
                }
                if (event.ctrlKey && event.keyCode === 56) {

                }
                if (event.ctrlKey && event.keyCode === 57) {
                    $state.go('manager.addEmployee');
                }
            }
        };

        $rootScope.$on('$stateChangeStart',
            function (event, toState, toParams, fromState, fromParams, options) {
                $rootScope.is_page_loading = true;
            });

        $scope.isActive = function (path) {
            return ($location.path().substr(0, path.length) === path);
        };

        $scope.check_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.checkCashExist(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {
                        if (data['error_mode'] === "NO_CASH") {
                            $scope.openOpenCashModal();
                        }
                        if (data['error_mode'] === "OLD_CASH") {
                            $scope.openCloseCashModal();
                        }
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        $scope.open_cash = function () {
            var sending_data = {
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.openCash(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_today_cash();
                        $scope.closeOpenCashModal();
                    }
                    else if (data['response_code'] === 3) {

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
                        $scope.closeCloseCashModal();
                        $scope.openOpenCashModal();
                    }
                    else if (data['response_code'] === 3) {

                    }
                }, function (error) {
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.is_user_login = function (user_data) {
            dashboardHttpRequest.checkLogin(user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {

                    }
                    else if (data['response_code'] === 3) {
                        $window.location.href = '/';
                    }
                }, function (error) {
                    console.log(error);
                });
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

        $scope.get_today_cash = function () {
            dashboardHttpRequest.getTodayCash($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $rootScope.cash_data.cash_id = data['cash_id'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.cash_data.cash_id = 0;
                    }
                }, function (error) {
                    console.log(error);
                });
        };

        $scope.get_today = function () {
            week = new Array("يكشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه", "شنبه")
            months = new Array("فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند");
            today = new Date();
            d = today.getDay();
            day = today.getDate();
            month = today.getMonth() + 1;
            year = today.getYear();
            year = (window.navigator.userAgent.indexOf('MSIE') > 0) ? year : 1900 + year;
            if (year == 0) {
                year = 2000;
            }
            if (year < 100) {
                year += 1900;
            }
            y = 1;
            for (i = 0; i < 3000; i += 4) {
                if (year == i) {
                    y = 2;
                }
            }
            for (i = 1; i < 3000; i += 4) {
                if (year == i) {
                    y = 3;
                }
            }
            if (y == 1) {
                year -= ((month < 3) || ((month == 3) && (day < 21))) ? 622 : 621;
                switch (month) {
                    case 1:
                        (day < 21) ? (month = 10, day += 10) : (month = 11, day -= 20);
                        break;
                    case 2:
                        (day < 20) ? (month = 11, day += 11) : (month = 12, day -= 19);
                        break;
                    case 3:
                        (day < 21) ? (month = 12, day += 9) : (month = 1, day -= 20);
                        break;
                    case 4:
                        (day < 21) ? (month = 1, day += 11) : (month = 2, day -= 20);
                        break;
                    case 5:
                    case 6:
                        (day < 22) ? (month -= 3, day += 10) : (month -= 2, day -= 21);
                        break;
                    case 7:
                    case 8:
                    case 9:
                        (day < 23) ? (month -= 3, day += 9) : (month -= 2, day -= 22);
                        break;
                    case 10:
                        (day < 23) ? (month = 7, day += 8) : (month = 8, day -= 22);
                        break;
                    case 11:
                    case 12:
                        (day < 22) ? (month -= 3, day += 9) : (month -= 2, day -= 21);
                        break;
                    default:
                        break;
                }
            }
            if (y == 2) {
                year -= ((month < 3) || ((month == 3) && (day < 20))) ? 622 : 621;
                switch (month) {
                    case 1:
                        (day < 21) ? (month = 10, day += 10) : (month = 11, day -= 20);
                        break;
                    case 2:
                        (day < 20) ? (month = 11, day += 11) : (month = 12, day -= 19);
                        break;
                    case 3:
                        (day < 20) ? (month = 12, day += 10) : (month = 1, day -= 19);
                        break;
                    case 4:
                        (day < 20) ? (month = 1, day += 12) : (month = 2, day -= 19);
                        break;
                    case 5:
                        (day < 21) ? (month = 2, day += 11) : (month = 3, day -= 20);
                        break;
                    case 6:
                        (day < 21) ? (month = 3, day += 11) : (month = 4, day -= 20);
                        break;
                    case 7:
                        (day < 22) ? (month = 4, day += 10) : (month = 5, day -= 21);
                        break;
                    case 8:
                        (day < 22) ? (month = 5, day += 10) : (month = 6, day -= 21);
                        break;
                    case 9:
                        (day < 22) ? (month = 6, day += 10) : (month = 7, day -= 21);
                        break;
                    case 10:
                        (day < 22) ? (month = 7, day += 9) : (month = 8, day -= 21);
                        break;
                    case 11:
                        (day < 21) ? (month = 8, day += 10) : (month = 9, day -= 20);
                        break;
                    case 12:
                        (day < 21) ? (month = 9, day += 10) : (month = 10, day -= 20);
                        break;
                    default:
                        break;
                }
            }
            if (y == 3) {
                year -= ((month < 3) || ((month == 3) && (day < 21))) ? 622 : 621;
                switch (month) {
                    case 1:
                        (day < 20) ? (month = 10, day += 11) : (month = 11, day -= 19);
                        break;
                    case 2:
                        (day < 19) ? (month = 11, day += 12) : (month = 12, day -= 18);
                        break;
                    case 3:
                        (day < 21) ? (month = 12, day += 10) : (month = 1, day -= 20);
                        break;
                    case 4:
                        (day < 21) ? (month = 1, day += 11) : (month = 2, day -= 20);
                        break;
                    case 5:
                    case 6:
                        (day < 22) ? (month -= 3, day += 10) : (month -= 2, day -= 21);
                        break;
                    case 7:
                    case 8:
                    case 9:
                        (day < 23) ? (month -= 3, day += 9) : (month -= 2, day -= 22);
                        break;
                    case 10:
                        (day < 23) ? (month = 7, day += 8) : (month = 8, day -= 22);
                        break;
                    case 11:
                    case 12:
                        (day < 22) ? (month -= 3, day += 9) : (month -= 2, day -= 21);
                        break;
                    default:
                        break;
                }
            }
            return week[d] + " " + day + " " + months[month - 1] + " " + year;
        };

        var tick = function () {
            $rootScope.clock = Date.now();
        };

        tick();
        $interval(tick, 1000);


        $scope.openOpenCashModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#openCashModal').modal('show');
            })(jQuery);
        };

        $scope.closeOpenCashModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#openCashModal').modal('hide');
            })(jQuery);
        };

        $scope.openCloseCashModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeCashModal').modal('show');
            })(jQuery);
        };

        $scope.closeCloseCashModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeCashModal').modal('hide');
            })(jQuery);
        };

        $rootScope.open_modal = function (modal_id) {
            jQuery.noConflict();
            (function ($) {
                $('#' + modal_id).modal('show');
            })(jQuery);
        };

        $rootScope.close_modal = function (modal_id) {
            jQuery.noConflict();
            (function ($) {
                $('#' + modal_id).modal('hide');
            })(jQuery);
        };


        initialize();

    });