angular.module("dashboard")
    .controller("buyCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        var initialize = function () {
            $scope.is_in_edit_mode_supplier = false;
            $scope.error_message = '';
            $scope.current_menu_nav = "MAT";
            $scope.read_only_mode = false;
            $scope.can_add_material = false;
            $scope.can_add_shop_product = false;
            $scope.new_invoice_purchase_data = {
                'id': 0,
                'supplier_id': 0,
                'material_items': [],
                'shop_product_items': [],
                'total_price': 0,
                'settlement_type': 'CASH',
                'tax': 0,
                'discount': 0,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            $scope.search_data_material = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.search_data_shop_products = {
                'search_word': '',
                'username': $rootScope.user_data.username
            };
            $scope.is_in_edit_mode_supplier = false;
            $scope.printers = [];
            $scope.get_all_invoice_purchases();
            $scope.get_suppliers();
            $scope.get_materials();
            $scope.get_shop_products();
        };

        $scope.showInvoicePurchase = function (invoice_id) {
            $scope.read_only_mode = true;
            var sending_data = {
                'invoice_id': invoice_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_purchase_data = {
                            'id': data['invoice']['id'],
                            'supplier_id': data['invoice']['supplier_id'],
                            'material_items': data['invoice']['material_items'],
                            'shop_product_items': data['invoice']['shop_product_items'],
                            'total_price': data['invoice']['total_price'],
                            'settlement_type': data['invoice']['settlement_type'],
                            'tax': data['invoice']['tax'],
                            'discount': data['invoice']['discount'],
                            'branch_id': $rootScope.user_data.branch,
                            'username': $rootScope.user_data.username
                        };
                        $scope.openAddModal();
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

        $scope.changeMenuNav = function (name) {
            if (name === "MAT") {
                $scope.current_menu_nav = name;
            }
            else if (name === "SHOP") {
                $scope.current_menu_nav = name;
            }
        };

        $scope.addInvoicePurchase = function () {
            dashboardHttpRequest.addInvoicePurchase($scope.new_invoice_purchase_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoice_purchases();
                        $scope.resetFrom();
                        $scope.closeAddModal();
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

        $scope.get_all_invoice_purchases = function () {
            var data = {
                'username': $rootScope.user_data.username,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getAllInvoicePurchases(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.invoice_purchases = data['invoices']
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

        $scope.get_suppliers = function () {
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getSuppliers(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
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

        $scope.get_shop_products = function () {
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getShopProducts(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.shop_products = data['shop_products']
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

        $scope.changeItemNumber = function (item_index) {
            var new_number = $scope.new_invoice_purchase_data.material_items[item_index].nums;
            var item_price = $scope.new_invoice_purchase_data.material_items[item_index].price;
            $scope.new_invoice_purchase_data.material_items[item_index].total = new_number * item_price;
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_purchase_data.material_items.length; j++) {
                var entry2 = $scope.new_invoice_purchase_data.material_items[j];
                new_total_price += entry2.total;
            }

            $scope.new_invoice_purchase_data.total_price = new_total_price;
        };

        $scope.changeItemPrice = function (item_index) {
            var new_price = $scope.new_invoice_purchase_data.material_items[item_index].price;
            var item_nums = $scope.new_invoice_purchase_data.material_items[item_index].nums;
            $scope.new_invoice_purchase_data.material_items[item_index].total = new_price * item_nums;
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_purchase_data.material_items.length; j++) {
                var entry2 = $scope.new_invoice_purchase_data.material_items[j];
                new_total_price += entry2.total;
            }
            $scope.new_invoice_purchase_data.total_price = new_total_price;
        };

        $scope.add_item = function (id, name, price) {
            var int_price = parseInt(price);
            var int_id = parseInt(id);
            var is_fill = false;
            if ($scope.new_invoice_purchase_data.material_items.length === 0) {
                $scope.new_invoice_purchase_data.material_items.push({
                    'id': int_id,
                    'name': name,
                    'price': int_price,
                    'nums': 1,
                    'total': int_price,
                    'description': ''
                });
                $scope.new_invoice_purchase_data.total_price += int_price;
            }
            else {
                for (var i = 0; i < $scope.new_invoice_purchase_data.material_items.length; i++) {
                    var entry = $scope.new_invoice_purchase_data.material_items[i];
                    if (parseInt(entry.id) === int_id) {
                        entry.nums += 1;
                        entry.total += entry.price;
                        is_fill = true;
                        $scope.new_invoice_purchase_data.total_price += entry.price;
                        break;
                    }
                }
                if (!is_fill) {
                    $scope.new_invoice_purchase_data.material_items.push({
                        'id': int_id,
                        'name': name,
                        'price': int_price,
                        'nums': 1,
                        'total': int_price,
                        'description': ''
                    });
                    $scope.new_invoice_purchase_data.total_price += int_price;
                }
                is_fill = false;
            }
        };

        $scope.add_item_shop = function (id, name, price) {
            var int_price = parseInt(price);
            var int_id = parseInt(id);
            var is_fill = false;
            if ($scope.new_invoice_purchase_data.shop_product_items.length === 0) {
                $scope.new_invoice_purchase_data.shop_product_items.push({
                    'id': int_id,
                    'name': name,
                    'price': int_price,
                    'sale_price': int_price,
                    'nums': 1,
                    'total': int_price,
                    'description': ''
                });
                $scope.new_invoice_purchase_data.total_price += int_price;
            }
            else {
                for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                    var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                    if (parseInt(entry.id) === int_id) {
                        entry.nums += 1;
                        entry.total += entry.price;
                        is_fill = true;
                        $scope.new_invoice_purchase_data.total_price += entry.price;
                        break;
                    }
                }
                if (!is_fill) {
                    $scope.new_invoice_purchase_data.shop_product_items.push({
                        'id': int_id,
                        'name': name,
                        'price': int_price,
                        'sale_price': int_price,
                        'nums': 1,
                        'total': int_price,
                        'description': ''
                    });
                    $scope.new_invoice_purchase_data.total_price += int_price;
                }
                is_fill = false;
            }
        };

        $scope.changeItemShopPrice = function (item_index) {
            var new_price = $scope.new_invoice_purchase_data.shop_product_items[item_index].price;
            var item_nums = $scope.new_invoice_purchase_data.shop_product_items[item_index].nums;
            $scope.new_invoice_purchase_data.shop_product_items[item_index].total = new_price * item_nums;
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_purchase_data.material_items.length; j++) {
                var entry2 = $scope.new_invoice_purchase_data.material_items[j];
                new_total_price += entry2.total;
            }
            $scope.new_invoice_purchase_data.total_price = new_total_price;
        };

        $scope.changeItemShopNumber = function (item_index) {
            var new_number = $scope.new_invoice_purchase_data.shop_product_items[item_index].nums;
            var item_price = $scope.new_invoice_purchase_data.shop_product_items[item_index].price;
            $scope.new_invoice_purchase_data.shop_product_items[item_index].total = new_number * item_price;
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_purchase_data.material_items.length; j++) {
                var entry2 = $scope.new_invoice_purchase_data.material_items[j];
                new_total_price += entry2.total;
            }
            $scope.new_invoice_purchase_data.total_price = new_total_price;
        };

        $scope.get_materials = function () {
            var data = {
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getMaterials(data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.materials = data['materials'];
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
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closeErrorModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#errorModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.openAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
            $scope.read_only_mode = false;
            $scope.resetFrom();
        };

        $scope.search_material = function () {
            if ($scope.search_data_material.search_word === '') {
                $scope.get_materials();
                $scope.can_add_material = false;
            }
            else {
                dashboardHttpRequest.searchMaterials($scope.search_data_material)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.materials = data['materials'];
                            if ($scope.materials.length === 0) {
                                $scope.can_add_material = true;
                            }
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


        $scope.add_material_to_data_base_after_search = function (material_name) {
            var sending_data = {
                'material_name': material_name,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.addMaterial(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.search_data_material.search_word = "";
                        $scope.can_add_material = false;
                        $scope.search_material();
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

        $scope.search_shop_products = function () {
            if ($scope.search_data_shop_products.search_word === '') {
                $scope.get_shop_products();
                $scope.can_add_shop_product = false;
            }
            else {
                dashboardHttpRequest.searchShopProducts($scope.search_data_shop_products)
                    .then(function (data) {
                        if (data['response_code'] === 2) {
                            $scope.shop_products = data['shop_products'];
                            if ($scope.shop_products.length === 0) {
                                $scope.can_add_shop_product = true;
                            }
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


        $scope.add_shop_product_to_data_base_after_search = function (shop_product_name) {
            var sending_data = {
                'shop_product_name': shop_product_name,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.addShopProduct(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.search_data_shop_products.search_word = "";
                        $scope.can_add_shop_product = false;
                        $scope.search_shop_products();
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

        $scope.delete_invoice_purchase = function (invoice_id) {
            var sending_data = {
                'invoice_id': invoice_id,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.deleteInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoice_purchases();
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

        $scope.openPermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('show');
                $('#addModal').css('z-index', 1000);
            })(jQuery);
        };

        $scope.closePermissionModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#closeInvoicePermissionModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
        };

        $scope.resetFrom = function () {
            $scope.new_invoice_purchase_data = {
                'id': 0,
                'supplier_id': 0,
                'material_items': [],
                'shop_product_items': [],
                'total_price': 0,
                'settlement_type': 'CASH',
                'tax': 0,
                'discount': 0,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
        };
        initialize();
    });