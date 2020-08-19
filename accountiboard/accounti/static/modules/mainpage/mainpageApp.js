var myApp = angular.module('mainpage', ['ui.router', 'ngCookies', 'satellizer']);

myApp.config(function ($stateProvider, $authProvider) {
    $authProvider.tokenType = 'Token';
    var main = {
        name: 'main',
        url: '',
        templateUrl: 'static/modules/mainpage/views/index.html'
    };
    var login = {
        name: 'login',
        url: '/login',
        templateUrl: 'static/modules/mainpage/views/login.html'
    };
    var register = {
        name: 'register',
        url: '/register',
        templateUrl: 'static/modules/mainpage/views/register.html'
    };

    $stateProvider.state(main);
    $stateProvider.state(login);
    $stateProvider.state(register);
});

angular.module("mainpage")
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

myApp.filter('counter', [function() {
    return function(seconds) {
        return new Date(1970, 0, 1).setSeconds(seconds);
    };
}]);