angular.module("dashboard")
    .controller("dashboardCtrl", function ($scope, $rootScope, $filter, $state, $auth, $interval, $http, $location, $timeout, dashboardHttpRequest, $window, $transitions) {
            var initialize = function () {
                if ($location.search().status && $location.search().token) {
                    data = {
                        "status": $location.search().status,
                        "token": $location.search().token
                    };
                    dashboardHttpRequest.payirVerifyGenToken(data)
                        .then(function (data) {
                            $auth.setToken(data['token']);
                            if (data["bundle_activation_status"] === "activated")
                                $scope.transaction_successful_activated = true;
                            else if (data["bundle_activation_status"] === "reserved")
                                $scope.transaction_successful_reserved = true;
                            else
                                $scope.transaction_unsuccessful = true;

                            $rootScope.open_modal('transactionResultModal');
                        }, function (error) {
                            $scope.error_message = error.data.error_msg;
                            $rootScope.open_modal('mainErrorModal');
                        });
                    $location.search('status', null);
                    $location.search('token', null);
                }
                $rootScope.is_page_loading = true;
                $rootScope.is_sub_page_loading = true;
                $rootScope.get_today_var = $scope.get_today();
                if (localStorage.user && localStorage.branch && localStorage.branches && localStorage.user_roles) {
                    if (!$scope.isAuthenticated()) {
                        $window.location.href = '/';
                    }
                    else {
                        $rootScope.user_data = {
                            "username": JSON.parse(localStorage.user),
                            "branch": JSON.parse(localStorage.branch),
                            "branches": JSON.parse(localStorage.branches)
                        };
                        $rootScope.user_full_name = JSON.parse(localStorage.full_name);
                        $rootScope.organization_name = JSON.parse(localStorage.organization_name);
                        $rootScope.user_branches = JSON.parse(localStorage.branches);
                        for (var i = 0; i < $rootScope.user_branches.length; i++) {
                            if ($rootScope.user_branches[i].id === $rootScope.user_data.branch) {
                                $rootScope.selecetd_branch = $rootScope.user_branches[i];
                                break;
                            }
                        }
                        $rootScope.user_roles = JSON.parse(localStorage.user_roles);
                        $rootScope.cash_data = {
                            'cash_id': 0
                        };
                        $scope.new_bug_data = {
                            title: "",
                            text: "",
                            image: "",
                            image_name: ""
                        };
                        $scope.branch_name = $rootScope.selecetd_branch.name;
                        $scope.get_today_cash();
                        $scope.get_news();
                    }
                }
                else {
                    window.location.replace("/");
                }

                $transitions.onBefore({}, function (transition) {
                    if (transition._targetState._identifier !== $state.current.name) {
                        $rootScope.is_page_loading = true;
                    }
                });

                $window.onkeyup = function (event) {
                    if (event.ctrlKey && event.keyCode === 49) {
                        $state.go('dashboard.quickAccess');
                    }
                    if (event.ctrlKey && event.keyCode === 50) {
                        $state.go('dashboard.cash_manager.salon');
                    }
                    if (event.ctrlKey && event.keyCode === 51) {
                        $state.go('dashboard.reservation');
                    }
                    if (event.ctrlKey && event.keyCode === 52) {
                        $state.go('dashboard.member_manager.member');
                    }
                    if (event.ctrlKey && event.keyCode === 54) {

                    }
                    if (event.ctrlKey && event.keyCode === 55) {
                        $state.go('dashboard.account_manager.buy');
                    }
                    if (event.ctrlKey && event.keyCode === 56) {

                    }
                    if (event.ctrlKey && event.keyCode === 57) {
                        $state.go('dashboard.manager.addEmployee');
                    }
                };
            };

            $rootScope.show_toast = function (message, type) {
                $rootScope.toast_message = message;
                $rootScope.toast_type = type;
                jQuery.noConflict();
                (function ($) {
                    var toast_object = $('.toast');
                    toast_object.toast({delay: 3000});
                    toast_object.toast('show');
                })(jQuery);
            };

            $rootScope.isActive = function (path) {
                return ($location.path().substr(0, path.length) === path);
            };

            $scope.log_out = function () {
                $auth.logout();
                $window.location.href = '/';
            };

            $scope.isAuthenticated = function () {
                return $auth.isAuthenticated();
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
                        $scope.error_message = error;
                        $scope.openErrorModal();
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
                // return week[d] + " " + day + " " + months[month - 1] + " " + year;
                return day + " " + months[month - 1];
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

            $rootScope.open_modal = function (modal_id, modal_has_to_fade_out) {
                jQuery.noConflict();
                (function ($) {
                    $('#' + modal_id).modal('show');
                })(jQuery);
                if (modal_has_to_fade_out) {
                    jQuery.noConflict();
                    (function ($) {
                        $('#' + modal_has_to_fade_out).css('z-index', 1000);
                    })(jQuery);
                }
            };

            $rootScope.changeBranch = function (selected_branch) {
                localStorage.branch = JSON.stringify(selected_branch.id);
                $rootScope.user_data.branch = selected_branch.id;
                $rootScope.selected_branch = selected_branch;
                $scope.$root.selected_branch = selected_branch;
                $scope.branch_name = selected_branch.name;
                $state.go("dashboard.cash_manager.salon", {}, {reload: true});
            };

            $rootScope.close_modal = function (modal_id, modal_has_to_fade_in) {
                jQuery.noConflict();
                (function ($) {
                    $('#' + modal_id).modal('hide');
                })(jQuery);
                if (modal_has_to_fade_in) {
                    jQuery.noConflict();
                    (function ($) {
                        $('#' + modal_has_to_fade_in).css('z-index', "");
                    })(jQuery);
                }
            };


            $rootScope.open_modalv2 = function (modal_id, modal_has_to_fade_out) {
                $scope.last_modal = modal_has_to_fade_out;
                jQuery.noConflict();
                (function ($) {
                    $('#' + modal_id).modal('show');
                })(jQuery);
                if (modal_has_to_fade_out) {
                    jQuery.noConflict();
                    (function ($) {
                        $('#' + modal_has_to_fade_out).css('z-index', 1000);
                    })(jQuery);
                }
            };
            $rootScope.close_modalv2 = function (modal_id) {
                jQuery.noConflict();
                (function ($) {
                    $('#' + modal_id).modal('hide');
                })(jQuery);
                if ($scope.last_modal) {
                    jQuery.noConflict();
                    (function ($) {
                        $('#' + $scope.last_modal).css('z-index', "");
                    })(jQuery);
                }
            };

            $scope.open_user_profile = function () {
                dashboardHttpRequest.getUserProfile()
                    .then(function (data) {
                        $scope.user_profile_data = data['_item'];
                    }, function (error) {
                        $scope.error_message = error.data.error_msg;
                        $rootScope.open_modal('mainErrorModal', 'userProfileModal');
                    });
                $rootScope.open_modal('userProfileModal');
            };

            $scope.update_profile = function () {
                dashboardHttpRequest.updateProfile($scope.user_profile_data)
                    .then(function (data) {
                        $rootScope.close_modal('userProfileModal');
                        $rootScope.show_toast("با موفقیت انجام شد", 'success');
                    }, function (error) {
                        $scope.error_message = error.data.error_msg;
                        $rootScope.open_modal('mainErrorModal', 'userProfileModal');
                    });
            };

            $rootScope.collapseLeftSidebar = function () {
                jQuery.noConflict();
                (function ($) {
                    if ($('#leftSidebarWrapper.collapseComplete').length && $('#rightSidebarPageContentWrapper.collapseComplete').length) {
                        $('#leftSidebarWrapper').removeClass('collapseComplete');
                        $('#rightSidebarPageContentWrapper').removeClass('collapseComplete');
                    }
                    else {
                        $('#leftSidebarWrapper').addClass('collapseComplete');
                        $('#rightSidebarPageContentWrapper').addClass('collapseComplete');
                    }
                })(jQuery);
            };

            $scope.get_news = function () {
                dashboardHttpRequest.get_news()
                    .then(function (data) {
                        $rootScope.all_news = data['results'];
                    }, function (error) {
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            };

            $scope.bugReportFileChange = function () {
                jQuery.noConflict();
                (function ($) {
                    var fileName = $('#bugFile').val();
                    $('#bugFile').next('.custom-file-label').html(fileName);
                    var reader = new FileReader();
                    var $img = $("#bugFile")[0];
                    reader.onload = function (e) {
                        $scope.new_bug_data.image = e.target.result;
                        $scope.new_bug_data.image_name = $img.files[0].name;
                    };
                    reader.readAsDataURL($img.files[0]);
                })(jQuery);
            };

            $scope.send_bug_report = function () {
                dashboardHttpRequest.bug_report($scope.new_bug_data)
                    .then(function () {
                        $scope.new_bug_data = {
                            title: "",
                            text: "",
                            image: "",
                            image_name: ""
                        };
                        $rootScope.show_toast("با موفقیت انجام شد", 'success');
                    }, function (error) {
                        if (error.status < 500) {
                            $rootScope.show_toast(error.data.error_msg, 'danger');
                        }
                        else {
                            $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                        }
                    });
            };

            $scope.change_password = function () {
                dashboardHttpRequest.changePassword($scope.user_profile_data)
                    .then(function (data) {
                        $rootScope.close_modal('userProfileModal');
                        $rootScope.show_toast("با موفقیت انجام شد", 'success');
                    }, function (error) {
                        $scope.error_message = error.data.error_msg;
                        $rootScope.open_modal('mainErrorModal', 'userProfileModal');
                    });
            };

            initialize();

        }
    );