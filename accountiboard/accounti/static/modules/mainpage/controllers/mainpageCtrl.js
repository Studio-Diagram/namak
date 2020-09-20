angular.module("mainpage")
    .controller("mainpageCtrl", function ($scope, $interval, $rootScope, $filter, $http, $state, $auth, $timeout, $window, mainpageHttpRequest) {
        var initialize = function () {
            var reCaptcha_showing = $interval(function () {
                jQuery.noConflict();
                (function ($) {
                    var badge_object = $('.grecaptcha-badge');
                    if (badge_object) {
                        badge_object.css('visibility', 'hidden');
                        badge_object.css('opacity', '0');
                        $interval.cancel(reCaptcha_showing);
                    }
                })(jQuery);
            }, 100);
            $state.go('main.login');
        };

        initialize();
    });