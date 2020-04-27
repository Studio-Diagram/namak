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
            'create_reserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "create_reserve/",
                    'data': data
                });
            },
            'create_waiting_reserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "create_waiting_reserve/",
                    'data': data
                });
            },
            'delete_reserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "delete_reserve/",
                    'data': data
                });
            },
            'arrive_reserve': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "arrive_reserve/",
                    'data': data
                });
            },
            'create_new_invoice_sales': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "create_new_invoice_sales/",
                    'data': data
                });
            },
            'end_current_game': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "end_current_game/",
                    'data': data
                });
            },
            'ready_for_settle': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "ready_for_settle/",
                    'data': data
                });
            },
            'print_after_save': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "print_after_save/",
                    'data': data
                });
            },
            'delete_items': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "delete_items/",
                    'data': data
                });
            },
            'delete_invoice': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "delete_invoice/",
                    'data': data
                });
            },
            'settle_invoice_sale': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "settle_invoice_sale/",
                    'data': data
                });
            },
            'close_cash': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "close_cash/",
                    'data': data
                });
            },
            'open_cash': function (data) {
                return this.request({
                    'method': "POST",
                    'url': "open_cash/",
                    'data': data
                });
            }
        };
        return service;

    });