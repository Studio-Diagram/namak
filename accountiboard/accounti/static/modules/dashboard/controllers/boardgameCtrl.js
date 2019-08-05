angular.module("dashboard")
    .controller("boardgameCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode = false;
            $scope.adding_boardgame = false;
            $scope.new_boardgame_data = {
                'boardgame_id': 0,
                'name': '',
                'category': '',
                'min_players': '',
                'max_players': '',
                'best_players': '',
                'rate': 1,
                'learning_time': '',
                'duration': '',
                'image_name': '',
                'image_path': '',
                'description': '',
                'bgg_code': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_boardgame = {
                'search_word': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.employeeSearchWord = '';
            $scope.get_boardgames_data($rootScope.user_data);
        };
        $scope.FileChange = function () {
            var fileName = $('#customFile').val();
            $('#customFile').next('.custom-file-label').html(fileName);
            var reader = new FileReader();
            var $img = $("#customFile")[0];
            reader.onload = function (e) {
                $scope.new_boardgame_data.image_path = e.target.result;
                $scope.new_boardgame_data.image_name = $img.files[0].name;
            };
            reader.readAsDataURL($img.files[0]);
        };

        $scope.get_boardgames_data = function (data) {
            dashboardHttpRequest.getBoardgames(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.boardgames = data['boardgames'];
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

        $scope.openAddBoardgameModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addBoardgameModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddBoardgameModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addBoardgameModal').modal('hide');
            })(jQuery);
        };

        $scope.addBoardgame = function () {
            $scope.adding_boardgame = true;
            if ($scope.is_in_edit_mode) {
                $scope.is_in_edit_mode = false;
                dashboardHttpRequest.addBoardgame($scope.new_boardgame_data)
                    .then(function (data) {
                        $scope.adding_boardgame = false;
                        if (data['response_code'] === 2) {
                            $scope.get_boardgames_data($rootScope.user_data);
                            $scope.closeAddBoardgameModal();
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.adding_boardgame = false;
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
            else {
                dashboardHttpRequest.addBoardgame($scope.new_boardgame_data)
                    .then(function (data) {
                        $scope.adding_boardgame = false;
                        if (data['response_code'] === 2) {
                            $scope.get_boardgames_data($rootScope.user_data);
                            $scope.resetFrom();
                            $scope.closeAddBoardgameModal();
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.adding_boardgame = false;
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
        };

        $scope.searchBoardgame = function () {
            if ($scope.search_data_boardgame.search_word === '') {
                $scope.get_boardgames_data($rootScope.user_data);
            }
            else {
                dashboardHttpRequest.searchBoardgame($scope.search_data_boardgame)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.boardgames = data['boardgames'];
                        }
                        else if (data['response_code'] === 3) {
                            $scope.error_message = data['error_msg'];
                            $scope.openErrorModal();
                        }
                    }, function (error) {
                        $scope.error_message = error;
                        $scope.openErrorModal();
                    });
            }
        };

        $scope.getBoardgame = function (boardgame_id) {
            var data = {
                'username': $rootScope.user_data.username,
                'boardgame_id': boardgame_id
            };
            dashboardHttpRequest.getBoardgame(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        return data['employee'];
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


        $scope.editBoardgame = function (boardgame_id) {
            $scope.is_in_edit_mode = true;
            var data = {
                'username': $rootScope.user_data.username,
                'boardgame_id': boardgame_id
            };
            dashboardHttpRequest.getBoardgame(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_boardgame_data = {
                            'boardgame_id': data['boardgame']['id'],
                            'name': data['boardgame']['name'],
                            'category': data['boardgame']['category'],
                            'min_players': data['boardgame']['min_players'],
                            'max_players': data['boardgame']['max_players'],
                            'best_players': data['boardgame']['best_players'],
                            'rate': data['boardgame']['rate'],
                            'learning_time': data['boardgame']['learning_time'],
                            'duration': data['boardgame']['duration'],
                            'image_name': data['boardgame']['image_name'],
                            'image_path': data['boardgame']['image_path'],
                            'description': data['boardgame']['description'],
                            'bgg_code': data['boardgame']['bgg_code'],
                        };
                        $('#customFile').next('.custom-file-label').html($scope.new_boardgame_data.image_name);
                        $scope.openAddBoardgameModal();
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

        $scope.openErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('show');
                $('#addBoardgameModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addBoardgameModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_boardgame_data = {
                'boardgame_id': 0,
                'name': '',
                'category': '',
                'min_players': '',
                'max_players': '',
                'best_players': '',
                'rate': 1,
                'learning_time': '',
                'duration': '',
                'image_name': '',
                'image_path': '',
                'description': '',
                'bgg_code': '',
                'branch': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $('#customFile').next('.custom-file-label').html("Choose File");

        };

        $scope.closeForm = function () {
            $scope.resetFrom();
            $scope.closeAddBoardgameModal();
        };
        initialize();
    });