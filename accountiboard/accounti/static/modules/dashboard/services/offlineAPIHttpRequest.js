angular.module('dashboard')
    .service('offlineAPIHttpRequest', function offlineAPIHttpRequest($q, $http, $auth, $cookies, $window) {
        var service = {
            'API_URL': "http://127.0.0.1:8000/offline_api/v1/",
            'use_session': false,
            'authenticated': null,
            'authPromise': null,
            'request': function (args) {
                if ($auth.getToken()) {
                    $http.defaults.headers.common.Authorization = 'Token ' + $auth.getToken();
                }
                // Continue
                params = args.params || {};
                args = args || {};
                var deferred = $q.defer(),
                    url = this.API_URL + args.url,
                    method = args.method || "GET",
                    params = params,
                    data = args.data || {};
                // Fire the request, as configured.
                $http({
                    url: url,
                    withCredentials: this.use_session,
                    method: method.toUpperCase(),
                    headers: {'X-CSRFToken': $cookies.get("csrftoken")},
                    params: params,
                    data: data
                }).then(angular.bind(this, function (data, status, headers, config) {
                        deferred.resolve(data['data'], status);
                    }), angular.bind(this, function (data, status, headers, config) {
                        console.log("error syncing with: " + url);
                        deferred.reject(data, status, headers, config);
                    }));
                return deferred.promise;
            },
            'create_member': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "create_member/",
                    'data': data
                });
            },
        };
        return service;

    });