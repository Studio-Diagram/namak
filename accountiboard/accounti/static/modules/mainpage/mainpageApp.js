var myApp = angular.module('mainpage', ['ui.router', 'ngCookies', 'satellizer']);

myApp.config(function ($stateProvider, $authProvider) {
    $authProvider.tokenType = 'Token';
    var loginState = {
        name: 'login',
        url: '',
        templateUrl: 'static/modules/mainpage/views/login.html'
    };

    $stateProvider.state(loginState);
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