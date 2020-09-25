angular.module("dashboard")
    .controller("expenseCategoryCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.new_expense_cat_data = {
                'expense_cat_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_expense_cat = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.expenseCatSearchWord = '';
            $scope.get_expense_cats_data($rootScope.user_data);
        };

        $scope.get_expense_cats_data = function (data) {
            dashboardHttpRequest.getAllExpenseCategories(data)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.expense_cats = data['all_expense_categories'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_page_loading = false;

                });
        };

        $scope.openAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addExpenseCategoryModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addExpenseCategoryModal').modal('hide');
            })(jQuery);
            $scope.resetFrom();
        };

        $scope.addExpenseCategory = function () {
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addExpenseCategory($scope.new_expense_cat_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_expense_cats_data($rootScope.user_data);
                            $scope.closeAddModal();
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {});
            }
            else {
                dashboardHttpRequest.addExpenseCategory($scope.new_expense_cat_data)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.get_expense_cats_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddModal();
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {});
            }
        };

        $scope.searchExpenseCategory = function () {
            if ($scope.search_data_expense_cat.search_word === '') {
                $scope.get_expense_cats_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchExpenseCategory($scope.search_data_expense_cat)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.expense_cats = data['all_expense_categories'];
                        }
                        else if (data['response_code'] === 3) {
                            $rootScope.show_toast(data.error_msg, 'danger');
                        }
                    }, function (error) {});
            }
        };

        $scope.editExpenseCategory = function (expense_cat_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
                'expense_cat_id': expense_cat_id
            };
            dashboardHttpRequest.getExpenseCategory(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_expense_cat_data = {
                            'expense_cat_id': data['expense_category']['id'],
                            'name': data['expense_category']['name']
                        };
                        $scope.openAddModal();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {

                });

        };

        $scope.resetFrom = function () {
            $scope.new_expense_cat_data = {
                'expense_cat_id': 0,
                'name': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddModal();
        };
        initialize();
    });