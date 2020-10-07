angular.module("dashboard")
    .controller("buyCtrl", function ($scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest) {
        $rootScope.is_page_loading = false;
        var initialize = function () {
            $scope.selected_material = {
                "id": 0
            };
            $scope.set_today_for_invoice();
            $scope.is_in_edit_mode_supplier = false;
            $scope.current_menu_nav = "MATERIAL";
            $scope.read_only_mode = false;
            $scope.can_add_material = false;
            $scope.can_add_shop_product = false;
            $scope.favourite_materials = [];
            $scope.favourite_shops = [];
            $scope.new_invoice_purchase_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'material_items': [],
                'shop_product_items': [],
                'total_price': 0,
                'settlement_type': '',
                'tax': 0,
                'discount': 0,
                'date': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': ''
            };
            $scope.search_data_material = {
                'search_word': ''
            };
            $scope.search_data_shop_products = {
                'search_word': ''
            };
            $scope.headers = [
                {
                    name: "شماره فاکتور",
                    key: "factor_number"
                },
                {
                    name: "طرف حساب",
                    key: "supplier_name"
                },
                {
                    name: "مبلغ خرید",
                    key: "total_price"
                },
                {
                    name: "نوع پرداخت",
                    key: "kind"
                },
                {
                    name: "تاریخ خرید",
                    key: "date"
                }
            ];
            $scope.table_config = {
                price_fields: ["total_price"],
                has_detail_button: true,
                has_delete_button: true,
                has_row_numbers: false
            };
            $scope.is_in_edit_mode_supplier = false;
            $scope.printers = [];
            $scope.get_all_invoice_purchases();
            $scope.get_suppliers();
            $scope.get_materials();
            $scope.get_shop_products();
            $scope.get_banking_data();
            $scope.get_stocks_data();
            $scope.getNextFactorNumber('BUY');
        };

        $scope.compare_before_exit = function () {
            return angular.toJson($scope.first_initial_value_of_invoice_purchase) === angular.toJson($scope.new_invoice_purchase_data);
        };

        $scope.search_materials = function () {
            $scope.materials = $filter('filter')($scope.materials_original, {'name': $scope.search_data_material.search_word});
        };

        $scope.search_shop_products = function () {
            $scope.shop_products = $filter('filter')($scope.shop_products_original, {'name': $scope.search_data_shop_products.search_word});
        };

        $scope.add_material_check = function () {
            if ($scope.search_data_material.search_word) {
                for (var index = 0; index < $scope.materials.length; index++) {
                    var item = $scope.materials[index];
                    if (item.name === $scope.search_data_material.search_word) {
                        return false
                    }
                }
                return true
            }
            return false
        };

        $scope.add_shop_product_check = function () {
            if ($scope.search_data_shop_products.search_word) {
                for (var index = 0; index < $scope.shop_products.length; index++) {
                    var item = $scope.shop_products[index];
                    if (item.name === $scope.search_data_shop_products.search_word) {
                        return false
                    }
                }
                return true
            }
            return false
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBankingByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    $scope.allbanking_names = [];
                    data['bank'].forEach(function (bank) {
                        $scope.allbanking_names.push({'id': bank.id, 'name': bank.name});
                    });

                    data['tankhah'].forEach(function (tankhah) {
                        $scope.allbanking_names.push({'id': tankhah.id, 'name': tankhah.name});
                    });

                    data['cash_register'].forEach(function (cash_register) {
                        $scope.allbanking_names.push({'id': cash_register.id, 'name': cash_register.name});
                    });

                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_stocks_data = function () {
            dashboardHttpRequest.getStockByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    angular.copy($rootScope.user_data.branches, $scope.branches);
                    $scope.stocks = data['stocks'];

                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.add_material_item = function (item) {
            var material_item = item;
            $scope.add_item(material_item.id, material_item.name, material_item.price);
        };

        $scope.add_item_shop_from_search_dropdown = function (item) {
            var shop_p = item;
            $scope.add_item_shop(shop_p.id, shop_p.name, shop_p.price, shop_p.buy_price);
        };

        $scope.get_most_items_supplier = function (supplier_id) {
            for (var index = 0; index < $scope.suppliers.length; index++) {
                if ($scope.suppliers[index].id === supplier_id) {
                    $scope.selected_supplier_name = $scope.suppliers[index].name;
                    break;
                }
            }
        };

        $scope.set_today_for_invoice = function () {
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {
                    var date = new Date();
                    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                    $("#datepicker").datepicker();
                    $('#datepicker').datepicker('setDate', today);
                });
            })(jQuery);
        };

        $scope.showInvoicePurchase = function (invoice_id) {
            $scope.read_only_mode = true;
            var sending_data = {
                'invoice_id': invoice_id
            };
            dashboardHttpRequest.getInvoicePurchase(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_purchase_data = {
                            'id': data['invoice']['id'],
                            'factor_number': data['invoice']['factor_number'],
                            'supplier_id': data['invoice']['supplier_id'],
                            'material_items': data['invoice']['material_items'],
                            'shop_product_items': data['invoice']['shop_product_items'],
                            'total_price': data['invoice']['total_price'],
                            'settlement_type': data['invoice']['settlement_type'],
                            'tax': data['invoice']['tax'],
                            'discount': data['invoice']['discount'],
                            'branch_id': $rootScope.user_data.branch,
                            'banking_id': data['invoice']['banking']['id'],
                            'stock_id': data['invoice']['stock']['id'],
                        };
                        $scope.openAddModal();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.changeMenuNav = function (name) {
            $scope.current_menu_nav = name;
        };

        $scope.addInvoicePurchase = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_invoice_purchase_data.date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addInvoicePurchase($scope.new_invoice_purchase_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.get_all_invoice_purchases();
                        $scope.resetFrom();
                        $scope.closeAddModal();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_invoice_purchase_data.factor_number = data['next_factor_number'];
                        $scope.first_initial_value_of_invoice_purchase = angular.copy($scope.new_invoice_purchase_data);
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_all_invoice_purchases = function () {
            var data = {
                'branch_id': $rootScope.user_data.branch
            };
            dashboardHttpRequest.getAllInvoicePurchases(data)
                .then(function (data) {
                    $rootScope.is_sub_page_loading = false;
                    if (data['response_code'] === 2) {
                        $scope.invoice_purchases = data['invoices']
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.is_sub_page_loading = false;
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_suppliers = function () {
            dashboardHttpRequest.getSuppliers($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.suppliers = data['suppliers']
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.get_shop_products = function () {
            dashboardHttpRequest.getShopProducts($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.shop_products = data['shop_products'];
                        $scope.shop_products_original = data['shop_products'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
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

            $scope.new_invoice_purchase_data.total_price = Math.round(new_total_price);
        };

        $scope.display_float_to_int = function (price) {
            return Math.round(price);
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
            $scope.new_invoice_purchase_data.total_price = Math.round(new_total_price);
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
                        entry.total += parseInt(entry.price);
                        is_fill = true;
                        $scope.new_invoice_purchase_data.total_price += parseInt(entry.price);
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

        $scope.add_item_shop = function (id, name, price, buy_price) {
            var int_price = parseInt(price);
            var int_buy_price = parseInt(buy_price);
            var int_id = parseInt(id);
            var is_fill = false;
            if ($scope.new_invoice_purchase_data.shop_product_items.length === 0) {
                $scope.new_invoice_purchase_data.shop_product_items.push({
                    'id': int_id,
                    'name': name,
                    'price': int_buy_price,
                    'sale_price': int_price,
                    'nums': 1,
                    'total': int_buy_price,
                    'description': ''
                });
                $scope.new_invoice_purchase_data.total_price += int_buy_price;
            }
            else {
                for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                    var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                    if (parseInt(entry.id) === int_id) {
                        entry.nums += 1;
                        entry.total += parseInt(entry.price);
                        is_fill = true;
                        $scope.new_invoice_purchase_data.total_price += parseInt(entry.price);
                        break;
                    }
                }
                if (!is_fill) {
                    $scope.new_invoice_purchase_data.shop_product_items.push({
                        'id': int_id,
                        'name': name,
                        'price': int_buy_price,
                        'sale_price': int_price,
                        'nums': 1,
                        'total': int_buy_price,
                        'description': ''
                    });
                    $scope.new_invoice_purchase_data.total_price += int_buy_price;
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
            $scope.new_invoice_purchase_data.total_price = Math.round(new_total_price);
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
            $scope.new_invoice_purchase_data.total_price = Math.round(new_total_price);
        };

        $scope.get_materials = function () {
            dashboardHttpRequest.getMaterials($rootScope.user_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.materials = data['materials'];
                        $scope.materials_original = data['materials'];
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.openAddModal = function () {
            $scope.set_today_for_invoice();
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('show');
            })(jQuery);
        };

        $scope.closeAddModal = function () {
            jQuery.noConflict();
            (function ($) {
                $('#addModal').modal('hide');
                $('#addModal').css('z-index', "");
            })(jQuery);
            $scope.read_only_mode = false;
            $scope.resetFrom();
        };

        $scope.search_material = function (search_word, items) {
            $scope.can_add_material = !items.length;
            $scope.search_data_material.search_word = search_word;
        };

        $scope.add_material_to_data_base_after_search = function (material_name) {
            var sending_data = {
                'material_name': material_name,
                'branch': $rootScope.user_data.branch
            };
            dashboardHttpRequest.addMaterial(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        var new_material = data['new_material'];
                        $scope.add_item(new_material.id, new_material.name, new_material.price);
                        $scope.search_data_material.search_word = "";
                        $scope.can_add_material = false;
                        $scope.get_materials();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.add_shop_product_to_data_base_after_search = function (shop_product_name) {
            var sending_data = {
                'shop_product_name': shop_product_name,
                'branch': $rootScope.user_data.branch
            };
            dashboardHttpRequest.addShopProduct(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        var new_shop_p = data['new_shop_product'];
                        $scope.add_item_shop(new_shop_p.id, new_shop_p.name, new_shop_p.sale_price, new_shop_p.buy_price);
                        $scope.search_data_shop_products.search_word = "";
                        $scope.can_add_shop_product = false;
                        $scope.get_shop_products();
                    }
                    else if (data['response_code'] === 3) {
                        $rootScope.show_toast(data.error_msg, 'danger');
                    }
                }, function (error) {
                    $rootScope.show_toast("خطای سرور ( پشتیبانان ما به زودی مشکل را برطرف خواهند کرد )", 'danger');
                });
        };

        $scope.delete_invoice_purchase = function (invoice_id) {
            dashboardHttpRequest.deleteInvoicePurchase(invoice_id)
                .then(function (data) {
                    $scope.get_all_invoice_purchases();
                }, function (error) {
                    $rootScope.show_toast(error.data.error_msg, 'danger');
                });
        };

        $scope.deleteNewItem = function (type, item_index) {
            if (type === 'material') {
                $scope.new_invoice_purchase_data.total_price -= $scope.new_invoice_purchase_data.material_items[item_index].total;
                $scope.new_invoice_purchase_data.material_items.splice(item_index, 1);
            }
            else {
                $scope.new_invoice_purchase_data.total_price -= $scope.new_invoice_purchase_data.shop_product_items[item_index].total;
                $scope.new_invoice_purchase_data.shop_product_items.splice(item_index, 1);
            }
        };

        $scope.save_and_open_modal = function () {
            $scope.addInvoicePurchase();
            $timeout(function () {
                $scope.openAddModal();
                $scope.getNextFactorNumber('BUY');
            }, 1000);
        };

        $scope.change_total_price = function () {
            var new_total_price = 0;
            for (var i = 0; i < $scope.new_invoice_purchase_data.shop_product_items.length; i++) {
                var entry = $scope.new_invoice_purchase_data.shop_product_items[i];
                new_total_price += entry.total;
            }
            for (var j = 0; j < $scope.new_invoice_purchase_data.material_items.length; j++) {
                var entry2 = $scope.new_invoice_purchase_data.material_items[j];
                new_total_price += entry2.total;
            }
            $scope.new_invoice_purchase_data.total_price = Number(new_total_price) + Number($scope.new_invoice_purchase_data.tax) - Number($scope.new_invoice_purchase_data.discount);
            $scope.new_invoice_purchase_data.total_price = Math.round($scope.new_invoice_purchase_data.total_price);
        };

        $scope.resetFrom = function () {
            $scope.selected_material = {
                "id": 0
            };
            $scope.new_invoice_purchase_data = {
                'id': 0,
                'factor_number': 0,
                'supplier_id': 0,
                'material_items': [],
                'shop_product_items': [],
                'total_price': 0,
                'settlement_type': '',
                'tax': 0,
                'discount': 0,
                'date': '',
                'branch_id': $rootScope.user_data.branch,
                'banking_id': '',
                'stock_id': ''
            };
            if ($scope.search_data_material.search_word) {
                $scope.search_data_material = {
                    'search_word': ''
                };
                $scope.get_materials();
            }
            if ($scope.search_data_shop_products.search_word) {
                $scope.search_data_shop_products = {
                    'search_word': ''
                };
                $scope.get_shop_products();
            }
        };
        initialize();
    });