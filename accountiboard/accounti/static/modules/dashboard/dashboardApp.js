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
    $authProvider.tokenType = 'Token';
    var registerEmployee = {
        name: 'manager',
        url: '/manager',
        templateUrl: 'static/modules/dashboard/views/manager.html'
    };
    var addEmployee = {
        name: 'manager.addEmployee',
        url: '/addEmployee',
        templateUrl: 'static/modules/dashboard/views/add_employee.html'
    };
    var tables = {
        name: 'manager.tables',
        url: '/tables',
        templateUrl: 'static/modules/dashboard/views/tables.html'
    };
    var menuCategory = {
        name: 'manager.menuCategory',
        url: '/menuCategory',
        templateUrl: 'static/modules/dashboard/views/menu_category.html'
    };
    var menuItem = {
        name: 'manager.menuItem',
        url: '/menuItem',
        templateUrl: 'static/modules/dashboard/views/menu_item.html'
    };
    var member = {
        name: 'member',
        url: '/member',
        templateUrl: 'static/modules/dashboard/views/member.html'
    };
    var boardgame = {
        name: 'boardgame',
        url: '/boardgame',
        templateUrl: 'static/modules/dashboard/views/boardgame.html'
    };

    var stock = {
        name: 'manager.stock',
        url: '/stock',
        templateUrl: 'static/modules/dashboard/views/stock.html'
    };

    var branch = {
        name: 'manager.branch',
        url: '/branch',
        templateUrl: 'static/modules/dashboard/views/branch.html'
    };
    var cash_manager = {
        name: 'cash_manager',
        url: '/cash_manager',
        templateUrl: 'static/modules/dashboard/views/cash-manager.html'
    };
    var salon = {
        name: 'cash_manager.salon',
        url: '/salon',
        templateUrl: 'static/modules/dashboard/views/salon.html'
    };
    var invoices = {
        name: 'cash_manager.invoices',
        url: '/invoices',
        templateUrl: 'static/modules/dashboard/views/invoices.html'
    };
    var cash = {
        name: 'cash_manager.cash',
        url: '/cash',
        templateUrl: 'static/modules/dashboard/views/cash.html'
    };
    var account_manager = {
        name: 'account_manager',
        url: '/account_manager',
        templateUrl: 'static/modules/dashboard/views/account-manager.html'
    };
    var buy = {
        name: 'account_manager.buy',
        url: '/buy',
        templateUrl: 'static/modules/dashboard/views/buy.html'
    };
    var pay = {
        name: 'account_manager.pay',
        url: '/pay',
        templateUrl: 'static/modules/dashboard/views/pays.html'
    };
    var expense = {
        name: 'account_manager.expense',
        url: '/expense',
        templateUrl: 'static/modules/dashboard/views/expense.html'
    };
    var suppliers = {
        name: 'account_manager.suppliers',
        url: '/suppliers',
        templateUrl: 'static/modules/dashboard/views/suppliers.html'
    };
    var supplier = {
        name: 'account_manager.supplier',
        url: '/supplier/:supplier',
        templateUrl: 'static/modules/dashboard/views/supplier.html'
    };
    var detail = {
        name: 'account_manager.detail',
        url: '/supplier/:detailState/:supplier',
        templateUrl: 'static/modules/dashboard/views/detail.html'
    };

    var invoiceReturn = {
        name: 'account_manager.return',
        url: '/return',
        templateUrl: 'static/modules/dashboard/views/return.html'
    };

    var expenseCategory = {
        name: 'manager.expenseCat',
        url: '/expenseCat',
        templateUrl: 'static/modules/dashboard/views/expense_category.html'
    };

    var reservation = {
        name: 'reservation',
        url: '/reservation',
        templateUrl: 'static/modules/dashboard/views/reservation.html'
    };

    var open_close_cash = {
        name: 'account_manager.manage_cash',
        url: '/manage_cash',
        templateUrl: 'static/modules/dashboard/views/open_close_cash.html'
    };

    var cash_disable = {
        name: 'cash_disable',
        url: '/cash_disable/:state',
        templateUrl: 'static/modules/dashboard/views/cash-disable.html'
    };

    $stateProvider.state(registerEmployee);
    $stateProvider.state(addEmployee);
    $stateProvider.state(menuCategory);
    $stateProvider.state(menuItem);
    $stateProvider.state(member);
    $stateProvider.state(boardgame);
    $stateProvider.state(stock);
    $stateProvider.state(branch);
    $stateProvider.state(cash_manager);
    $stateProvider.state(salon);
    $stateProvider.state(invoices);
    $stateProvider.state(cash);
    $stateProvider.state(account_manager);
    $stateProvider.state(buy);
    $stateProvider.state(pay);
    $stateProvider.state(expense);
    $stateProvider.state(suppliers);
    $stateProvider.state(supplier);
    $stateProvider.state(detail);
    $stateProvider.state(invoiceReturn);
    $stateProvider.state(expenseCategory);
    $stateProvider.state(reservation);
    $stateProvider.state(open_close_cash);
    $stateProvider.state(tables);
    $stateProvider.state(cash_disable);
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
