angular.module("dashboard")
    .controller("salaryCtrl", function( $scope, $interval, $rootScope, $filter, $http, $timeout, $window, dashboardHttpRequest, $location, $state){
        var initialize = function () {
            $scope.set_today_for_invoice();
            $scope.error_message = '';
            $scope.edit_mode = false;
            $scope.search_word ='';
            $scope.new_salary_data = {
                'id': 0,
                'factor_number': 0,
                'employee_id': 0,
                'base_salary': 0,
                'over_time_pay':0,
                'benefits':0,
                'bonuses':0,
                'reduction':0,
                'insurance':0,
                'tax':0,
                'total_price':0,
                'backup_code': '',
                'settle_type': '',
                'bonuses_description':'',
                'reduction_description':'',
                'description':'',
                'branch_id': $rootScope.user_data.branch,                
                'banking_id':'',
                
            };


            $scope.get_banking_data();
            $scope.get_employees_data();
            $scope.getInvoiceSalaries();
            jQuery.noConflict();
            (function ($) {
                $(document).ready(function () {

                    $("#datepicker").datepicker();
                    
                });
            })(jQuery);

            $scope.headers = [

                
                    {
                        name: "شماره فیش",
                        key: "factor_number"
                    },
                    {
                        name: "نام کارمند",
                        key: "employee_name"
                    },
                    {
                        name: "خالص پرداختی",
                        key: "total_price"
                    },
                    {
                        name: "نوع پرداخت",
                        key: "settle_type"
                    },
                    {
                        name: "بانکداری",
                        key: "banking"
                    },
                    {
                        name: "تاریخ پرداخت ",
                        key: "invoice_date"
                    },
                
                ];
            

                $scope.table_config ={
                    price_fields: ["price"],
                    has_detail_button: true,
                    has_delete_button: true,
                };
          

        };

        $scope.change_total_price = function () {
            $scope.new_salary_data.total_price = 0;
            $scope.new_salary_data.total_price = Number($scope.new_salary_data.base_salary) + Number($scope.new_salary_data.over_time_pay) + Number($scope.new_salary_data.benefits) + Number($scope.new_salary_data.bonuses) - Number($scope.new_salary_data.reduction) - Number($scope.new_salary_data.insurance) - Number($scope.new_salary_data.tax);
        };

        $scope.get_employees_data = function () {
            
            dashboardHttpRequest.getBranchEmployees($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    
                    $scope.employees = data['employees'];
                    

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error.data.error_msg;
                    $rootScope.open_modal('errorModal');
                });
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

        $scope.save_and_open_modal = function () {
            $scope.addSalary();
            $timeout(function () {
                $scope.openAddModal();
                $scope.getNextFactorNumber('SALARY');
            }, 1000);
        };

        $scope.resetFrom = function () {
            $scope.new_salary_data = {
                'id': 0,
                'factor_number': 0,
                'employee_id': 0,
                'base_salary': 0,
                'over_time_pay':0,
                'benefits':0,
                'bonuses':0,
                'reduction':0,
                'insurance':0,
                'tax':0,
                'total_price':0,
                'backup_code': '',
                'settle_type': '',
                'bonuses_description':'',
                'reduction_description':'',
                'description':'',
                'branch_id': $rootScope.user_data.branch,                
                'banking_id':'',
            };
        };

        $scope.get_banking_data = function () {
            dashboardHttpRequest.getBankingByBranch($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.allbanking_names = [];
                    data['bank'].forEach(function (bank) {
                        $scope.allbanking_names.push({'id':bank.id, 'name':bank.name});
                    });

                    data['tankhah'].forEach(function (tankhah) {
                        $scope.allbanking_names.push({'id':tankhah.id, 'name':tankhah.name});
                    });

                    data['cash_register'].forEach(function (cash_register) {
                        $scope.allbanking_names.push({'id':cash_register.id, 'name':cash_register.name});
                    });

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error;
                    $scope.openErrorModal();
                });
        };

        $scope.getNextFactorNumber = function (invoice_type) {
            var sending_data = {
                'invoice_type': invoice_type,
                'branch_id': $rootScope.user_data.branch,
                'username': $rootScope.user_data.username
            };
            dashboardHttpRequest.getNextFactorNumber(sending_data)
                .then(function (data) {
                    if (data['response_code'] === 2) {
                        $scope.new_salary_data.factor_number = data['next_factor_number'];
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


        $scope.addSalary = function () {
            jQuery.noConflict();
            (function ($) {
                $scope.new_salary_data.invoice_date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.addInvoiceSalary($scope.new_salary_data,'0')
                .then(function (data) {
                        $scope.getInvoiceSalaries();
                       
                        $scope.resetFrom();
                        $scope.close_modal('addModal');
                    
                }, function (error) {
                    console.log("fhhthtu")
                    $scope.error_message = error.data.error_msg;
                    $rootScope.open_modal('errorModal', 'addModal');
                });
        };

        $scope.getInvoiceSalaries= function () {

            dashboardHttpRequest.getSalaries($rootScope.user_data.branch)
                .then(function (data) {
                    $rootScope.is_page_loading = false;
                    $scope.salaries = data['invoices'];
                    
                   

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error.data.error_msg;
                    $rootScope.open_modal('errorModal');
                    
                });
        };

        $scope.delete_invoice_salary = function (invoice_id) {

            dashboardHttpRequest.deleteInvoiceSalary(invoice_id)
                .then(function (data) {
                    $scope.closeDeletePermissionModal();
                    $scope.getInvoiceSalaries();

                }, function (error) {
                    $rootScope.is_page_loading = false;
                    $scope.error_message = error.data.error_msg;
                    $rootScope.open_modal('errorModal');
                });
        };

        $scope.openDeletePermissionModal = function (invoice_id) {
            $scope.deleteing_invoice_id = invoice_id;
            $rootScope.open_modal("deleteInvoicePermissionModal")
        };

        $scope.closeDeletePermissionModal = function () {
            $scope.deleteing_invoice_id = 0;
            $rootScope.close_modal("deleteInvoicePermissionModal")
            $scope.resetFrom()
        };

        $scope.showInvoiceSalary = function (invoice_id) {

            
            dashboardHttpRequest.getInvoiceSalary(invoice_id)
                .then(function (data) {
                        console.log(data)
                        $scope.new_salary_data = {
                            'id': data['invoice']['id'],
                            'factor_number': data['invoice']['factor_number'],
                            'employee_id': data['invoice']['employee_id'],
                            'settle_type': data['invoice']['settle_type'],
                            'branch_id': $rootScope.user_data.branch,
                            'banking_id': data['invoice']['banking']['id'],
                            'backup_code': data['invoice']['backup_code'],
                            'invoice_date': data['invoice']['invoice_date'],


                            'base_salary': data['invoice']['base_salary'],
                            'over_time_pay':data['invoice']['over_time_pay'],
                            'benefits':data['invoice']['benefits'],
                            'bonuses':data['invoice']['bonuses'],
                            'reduction':data['invoice']['reduction'],
                            'insurance':data['invoice']['insurance'],
                            'tax':data['invoice']['tax'],
                            'total_price':data['invoice']['total_price'],
                            
    
                            'bonuses_description':data['invoice']['bonuses_description'],
                            'reduction_description':data['invoice']['reduction_description'],
                            'description':data['invoice']['description'],
                            
                            
                        };
                        $scope.edit_mode = true;
                        $scope.open_modal('addModal');
                        
                
                }, function (error) {
                    
                    $scope.error_message = error.data.error_msg;
                    $rootScope.open_modal('errorModal');
                });
        };

        $scope.editSalary= function (){
            jQuery.noConflict();
            (function ($) {
                $scope.new_salary_data.invoice_date = $("#datepicker").val();
            })(jQuery);
            dashboardHttpRequest.editInvoiceSalary($scope.new_salary_data,$scope.new_salary_data.id)
                .then(function (data) {
                        $scope.getInvoiceSalaries();
                        
                        $scope.resetFrom();
                        $scope.edit_mode = false;
                        $scope.close_modal('addModal');
                    
                }, function (error) {
                    
                    $scope.error_message = error.data.error_msg;
                    $rootScope.open_modal('errorModal', 'addModal');
                });
        };

        $scope.searchSalary = function () {
           
            if ($scope.search_word === '') {
                $scope.getInvoiceSalaries();
            }
            else {
                
                dashboardHttpRequest.searchSalary($scope.search_word, $rootScope.user_data.branch)
                    .then(function (data) {
                        $rootScope.is_page_loading = false;
                        $scope.salaries = data['invoices'];

                    }, function (error) {
                        $scope.error_message = error.data.error_msg;
                        $scope.open_modal('errorModal');
                    });
            }
        };

        initialize();



    });