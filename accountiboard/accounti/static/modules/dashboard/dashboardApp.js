var myApp = angular.module('dashboard', ['ui.router', 'ngCookies', 'satellizer', 'ui.select', 'ngTagsInput']);

myApp.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if (event.which === 13) {
                scope.$apply(function () {
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});

myApp.config(function ($stateProvider, $authProvider) {
    $authProvider.tokenType = 'Bearer';
    var dashboard = {
        name: 'dashboard',
        url: '/dashboard'
    };
    var cafe_management = {
        name: 'dashboard.cafe_management',
        url: '/cafe',
        templateUrl: 'static/modules/dashboard/views/cafe_management.html'
    };
    var branch_management = {
        name: 'dashboard.branch_management',
        url: '/branch',
        templateUrl: 'static/modules/dashboard/views/branch_management.html'
    };
    var employee = {
        name: 'dashboard.cafe_management.employee',
        url: '/employee',
        templateUrl: 'static/modules/dashboard/views/add_employee.html'
    };
    var tables = {
        name: 'dashboard.branch_management.tables',
        url: '/tables',
        templateUrl: 'static/modules/dashboard/views/tables.html'
    };
    var menu_manager = {
        name: 'dashboard.branch_management.menu',
        url: '/menu',
        templateUrl: 'static/modules/dashboard/views/menu_manager.html'
    };
    var menu_general = {
        name: 'dashboard.branch_management.menu.general',
        url: '/general',
        templateUrl: 'static/modules/dashboard/views/menu.html'
    };
    var menu_printers = {
        name: 'dashboard.branch_management.menu.printers',
        url: '/printers',
        templateUrl: 'static/modules/dashboard/views/printers.html'
    };
    var branch_details = {
        name: 'dashboard.branch_management.details',
        url: '/details',
        templateUrl: 'static/modules/dashboard/views/branch_details.html'
    };
    var game_branch_details = {
        name: 'dashboard.branch_management.game_details',
        url: '/game_details',
        templateUrl: 'static/modules/dashboard/views/game_branch_details.html'
    };
    var member_manager = {
        name: 'dashboard.member_manager',
        url: '/member_manager',
        templateUrl: 'static/modules/dashboard/views/member_manager.html'
    };
    var member = {
        name: 'dashboard.member_manager.member',
        url: '/member',
        templateUrl: 'static/modules/dashboard/views/member.html'
    };
    var lottery = {
        name: 'dashboard.member_manager.lottery',
        url: '/lottery',
        templateUrl: 'static/modules/dashboard/views/lottery.html'
    };

    var branch = {
        name: 'dashboard.cafe_management.branch',
        url: '/branch',
        templateUrl: 'static/modules/dashboard/views/branch.html'
    };
    var cash_manager = {
        name: 'dashboard.cash_manager',
        url: '/cash_manager',
        templateUrl: 'static/modules/dashboard/views/cash-manager.html'
    };
    var salon = {
        name: 'dashboard.cash_manager.salon',
        url: '/salon/:table_name',
        params: {
            "table_name": {
                dynamic: true,
                value: null
            }
        },
        templateUrl: 'static/modules/dashboard/views/salon.html'
    };
    var account_manager = {
        name: 'dashboard.account_manager',
        url: '/account_manager',
        templateUrl: 'static/modules/dashboard/views/account-manager.html'
    };
    var buy = {
        name: 'dashboard.account_manager.buy',
        url: '/buy',
        templateUrl: 'static/modules/dashboard/views/buy.html'
    };
    var pay = {
        name: 'dashboard.account_manager.pay',
        url: '/pay',
        templateUrl: 'static/modules/dashboard/views/pays.html'
    };
    var expense = {
        name: 'dashboard.account_manager.expense',
        url: '/expense',
        templateUrl: 'static/modules/dashboard/views/expense.html'
    };
    var suppliers = {
        name: 'dashboard.account_manager.suppliers',
        url: '/suppliers',
        templateUrl: 'static/modules/dashboard/views/suppliers.html'
    };
    var reports = {
        name: 'dashboard.account_manager.reports',
        url: '/reports?type&start&end&branches&suppliers&s_types',
        params: {
            "type": {
                dynamic: true,
                value: null
            },
            "start": {
                dynamic: true,
                value: null
            },
            "end": {
                dynamic: true,
                value: null
            },
            "branches": {
                dynamic: true,
                value: null
            },
            "suppliers": {
                dynamic: true,
                value: null
            },
            "s_types": {
                dynamic: true,
                value: null
            }
        },
        templateUrl: 'static/modules/dashboard/views/reports.html'
    };
    var supplier = {
        name: 'dashboard.account_manager.supplier',
        url: '/supplier/:supplier',
        templateUrl: 'static/modules/dashboard/views/supplier.html'
    };
    var detail = {
        name: 'dashboard.account_manager.detail',
        url: '/supplier/:detailState/:supplier',
        templateUrl: 'static/modules/dashboard/views/detail.html'
    };

    var invoiceReturn = {
        name: 'dashboard.account_manager.return',
        url: '/return',
        templateUrl: 'static/modules/dashboard/views/return.html'
    };

    var expenseCategory = {
        name: 'dashboard.manager.expenseCat',
        url: '/expenseCat',
        templateUrl: 'static/modules/dashboard/views/expense_category.html'
    };

    var reservation = {
        name: 'dashboard.reservation',
        url: '/reservation',
        templateUrl: 'static/modules/dashboard/views/reservation.html'
    };

    var open_close_cash = {
        name: 'dashboard.account_manager.manage_cash',
        url: '/manage_cash',
        templateUrl: 'static/modules/dashboard/views/open_close_cash.html'
    };

    var open_close_cash_detail = {
        name: 'dashboard.account_manager.manage_cash_detail',
        url: '/manage_cash/:cash_id',
        templateUrl: 'static/modules/dashboard/views/open_close_cash_detail.html'
    };

    var big_cash_detail_view_in_open_close_cash = {
        name: 'dashboard.account_manager.manage_cash_detail_big',
        url: '/manage_cash/:cash_id/detail',
        template: '<cash-detail-directive></cash-detail-directive>',
        params: {
            "display_cash_number": true,
            "show_submit_today_cash_button": false,
            "show_print_today_cash_button": false,
        }
    };

    var cash = {
        name: 'dashboard.cash_manager.cash',
        url: '/cash/:cash_id',
        template: '<cash-detail-directive></cash-detail-directive>',
        params: {
            "display_cash_number": false,
            "show_submit_today_cash_button": true,
            "show_print_today_cash_button": true,
        }
    };

    var quick_access = {
        name: 'dashboard.quickAccess',
        url: '/quickAccess',
        templateUrl: 'static/modules/dashboard/views/quick-access.html'
    };

    var banking = {
        name: 'dashboard.cafe_management.banking',
        url: '/banking',
        templateUrl: 'static/modules/dashboard/views/banking.html'
    };
    var stocks = {
        name: 'dashboard.cafe_management.stocks',
        url: '/stocks',
        templateUrl: 'static/modules/dashboard/views/stocks.html'
    };

    var namak = {
        name: 'dashboard.cafe_management.namak',
        url: '/namak',
        templateUrl: 'static/modules/dashboard/views/namak.html'
    };

    var bundles = {
        name: 'dashboard.cafe_management.namak.bundles',
        url: '/bundles',
        templateUrl: 'static/modules/dashboard/views/bundles.html'
    };

    var buy_bundle = {
        name: 'dashboard.cafe_management.namak.buy_bundle',
        url: '/buy-bundle',
        templateUrl: 'static/modules/dashboard/views/buy_bundle.html'
    };

    var transactions = {
        name: 'dashboard.cafe_management.namak.transactions',
        url: '/transactions',
        templateUrl: 'static/modules/dashboard/views/transactions.html'
    };

    $stateProvider.state(dashboard);
    $stateProvider.state(cafe_management);
    $stateProvider.state(branch_management);
    $stateProvider.state(employee);
    $stateProvider.state(menu_manager);
    $stateProvider.state(menu_general);
    $stateProvider.state(menu_printers);
    $stateProvider.state(branch_details);
    $stateProvider.state(game_branch_details);
    $stateProvider.state(member);
    $stateProvider.state(branch);
    $stateProvider.state(cash_manager);
    $stateProvider.state(salon);
    $stateProvider.state(cash);
    $stateProvider.state(account_manager);
    $stateProvider.state(buy);
    $stateProvider.state(pay);
    $stateProvider.state(expense);
    $stateProvider.state(suppliers);
    $stateProvider.state(reports);
    $stateProvider.state(supplier);
    $stateProvider.state(detail);
    $stateProvider.state(invoiceReturn);
    $stateProvider.state(expenseCategory);
    $stateProvider.state(reservation);
    $stateProvider.state(open_close_cash);
    $stateProvider.state(open_close_cash_detail);
    $stateProvider.state(big_cash_detail_view_in_open_close_cash);
    $stateProvider.state(tables);
    $stateProvider.state(member_manager);
    $stateProvider.state(lottery);
    $stateProvider.state(quick_access);
    $stateProvider.state(banking);
    $stateProvider.state(stocks);
    $stateProvider.state(namak);
    $stateProvider.state(bundles);
    $stateProvider.state(buy_bundle);
    $stateProvider.state(transactions);
});

angular.module("dashboard")
    .filter("persianNumber", function () {
        return function (number) {
            var translation = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
            var persianNumber = '';
            var englishNumber = String(number);
            for (var i = 0; i < englishNumber.length; i++) {
                var translatedChar = (isNaN(englishNumber.charAt(i)) || englishNumber.charAt(i) == ' ' || englishNumber.charAt(i) == '\n') ? englishNumber.charAt(i) : translation[parseInt(englishNumber.charAt(i))];
                persianNumber = persianNumber + translatedChar;
            }
            return persianNumber;
        };
    });

myApp.directive('format', function ($filter) {
    'use strict';

    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) {
                return;
            }

            ctrl.$formatters.unshift(function () {
                return $filter('number')(ctrl.$modelValue);
            });

            ctrl.$parsers.unshift(function (viewValue) {
                var plainNumber = viewValue.replace(/[\,\.]/g, ''),
                    b = $filter('number')(plainNumber);

                elem.val(b);

                return plainNumber;
            });
        }
    };
});


myApp.directive('selectOnClick', ['$window', function ($window) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.on('click', function () {
                if (!$window.getSelection().toString()) {
                    // Required for mobile Safari
                    this.setSelectionRange(0, this.value.length)
                }
            });
        }
    };
}]);

myApp.directive('tooltip', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.on('mouseenter', function () {
                jQuery.noConflict();
                (function ($) {
                    $(element[0]).tooltip('show');
                })(jQuery);
            });
        }
    };
});

myApp.filter('range', function () {
    return function (input, total) {
        total = parseInt(total);

        for (var i = 0; i < total; i++) {
            input.push(i);
        }

        return input;
    };
});

myApp.run(function ($window, $rootScope, $http) {
    $http({
        method: 'GET',
        url: 'https://namak.works/'
    }).then(function successCallback(response) {
        // this callback will be called asynchronously
        // when the response is available
    }, function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
    });
    $rootScope.online = navigator.onLine;
    $window.addEventListener("offline", function () {
        $rootScope.$apply(function () {
            $rootScope.online = false;
        });
    }, false);
    $window.addEventListener("online", function () {
        $rootScope.$apply(function () {
            $rootScope.online = true;
        });
    }, false);
});

myApp.directive('tableDirective', function () {
    return {
        restrict: 'EA',
        scope: {
            headers: '=',
            rows: '=',
            config: '=',
            detailCallback: '&',
            rightSideDetailCallback: '&'
        },
        templateUrl: '/static/modules/dashboard/directives/reusable-table.html',
        link: function (scope) {
            if (scope.config.has_second_button_on_right_side === undefined)
                scope.config.has_second_button_on_right_side = false;
            if (scope.config.has_row_numbers === undefined)
                scope.config.has_row_numbers = true;
        }
    }

});

myApp.directive('settledInvoiceModalDirective', function () {
    return {
        restrict: 'EA',
        templateUrl: '/static/modules/dashboard/directives/settled-invoice-modal.html',
        controller: 'settledInvoiceModalCtrl'
    }
});

myApp.directive('addMemberModalDirective', function () {
    return {
        restrict: 'EA',
        templateUrl: '/static/modules/dashboard/directives/add-member-modal.html',
        controller: 'addMemberDirectiveCtrl'
    }
});

myApp.directive('cashDetailDirective', function () {
    return {
        restrict: 'EA',
        templateUrl: '/static/modules/dashboard/directives/cash-detail.html',
        controller: 'cashDetailCtrl'
    }
});

function configureTemplateFactory($provide) {
    // Set a suffix outside the decorator function
    var cacheBuster = Date.now().toString();

    function templateFactoryDecorator($delegate) {
        var fromUrl = angular.bind($delegate, $delegate.fromUrl);
        $delegate.fromUrl = function (url, params) {
            if (url !== null && angular.isDefined(url) && angular.isString(url)) {
                url += (url.indexOf("?") === -1 ? "?" : "&");
                url += "v=" + cacheBuster;
            }

            return fromUrl(url, params);
        };

        return $delegate;
    }

    $provide.decorator('$templateFactory', ['$delegate', templateFactoryDecorator]);
}

myApp.config(['$provide', configureTemplateFactory]);

myApp.config(["$locationProvider", function ($locationProvider) {
    $locationProvider.html5Mode(true);
}]);

myApp.directive('popover', function ($compile) {
    return {
        restrict: 'EA',
        scope: {
            question: '@',
            text: '@',
            firstButtonText: '@',
            secondButtonText: '@',
            firstCallback: '&',
            secondCallback: '&'
        },
        link: function (scope, elem, $scope) {
            jQuery.noConflict();
            (function ($) {
                var content = `<div class="popoverWrapper"><div>
                    <p><i class="fas fa-exclamation-triangle"></i><span ng-bind="question"></span></p>
                    <p ng-bind="text"></p>
                    <a ng-if="firstButtonText" href="" ng-click="firstCallback()" 
                    class="mainButton redButton smallButton fullWidthButton" 
                    ng-bind="firstButtonText"></a>
                    <a ng-if="secondButtonText" href="" ng-click="secondCallback()" ng-bind="secondButtonText"
                    class="mainButton newGrayButton smallButton fullWidthButton"></a>
                    </div>
                    </div>`;
                var compileContent = $compile(content)(scope);
                var options = {
                    content: compileContent[0],
                    html: true
                };
                $(elem).popover(options);
            })(jQuery);

        }
    }
});