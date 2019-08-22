from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Branch(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=4 * 255, null=False, blank=False)
    start_working_time = models.TimeField(null=True)
    end_working_time = models.TimeField(null=True)


class Employee(models.Model):
    # Personal Data
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    father_name = models.CharField(max_length=30, null=True, blank=True)
    national_code = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=False, blank=False)
    home_address = models.CharField(max_length=500, null=False, blank=True)
    # Banking Data
    bank_name = models.CharField(max_length=30, null=True, blank=True)
    bank_card_number = models.CharField(max_length=30, null=True, blank=True)
    shaba_number = models.CharField(max_length=255, null=True, blank=True)
    # Employee Data
    card_number = models.CharField(max_length=30, null=False, blank=True)
    password = models.TextField(null=False, blank=False)
    birthday_date = models.DateField(null=True, blank=True)
    membership_card_number = models.CharField(max_length=50, null=False, blank=True)
    base_worksheet_salary = models.FloatField(null=False, blank=False)
    base_worksheet_count = models.FloatField(null=False, blank=False)
    discount_percentage = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(null=True, verbose_name='last login', blank=True)


class EmployeeToBranch(models.Model):
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    auth_level = models.IntegerField(default=3)
    position = models.CharField(max_length=55, blank=True)


class Stock(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)


class StockToBranch(models.Model):
    branch = models.ForeignKey(Branch, null=True, blank=False, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, null=True, blank=False, on_delete=models.CASCADE)


class Printer(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)


class MenuCategory(models.Model):
    KIND = (
        ('KITCHEN', 'آشپزخانه'),
        ('BAR', 'بار'),
    )
    name = models.CharField(max_length=30, null=True, blank=True)
    kind = models.CharField(max_length=50, choices=KIND, blank=False, null=False)


class PrinterToCategory(models.Model):
    printer = models.ForeignKey(Printer, null=True, blank=False, on_delete=models.CASCADE)
    menu_category = models.ForeignKey(MenuCategory, null=True, blank=False, on_delete=models.CASCADE)


class MenuItem(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    price = models.CharField(max_length=30, null=True, blank=True)
    is_delete = models.SmallIntegerField(default=0, null=False)
    menu_category = models.ForeignKey(MenuCategory, null=True, blank=False, on_delete=models.CASCADE)


class Boardgame(models.Model):
    CATEGORY = (
        ('HEAVY', 'استراتژی سنگین'),
        ('LIGHT', 'استراتژی سبک'),
        ('FAMILY', 'خانواده و مهمانی'),
        ('ABSTRACT', 'استراتژی انتزاعی'),
    )
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=50, choices=CATEGORY, blank=False, null=False)
    min_players = models.IntegerField(null=False)
    max_players = models.IntegerField(null=False)
    best_players = models.IntegerField(null=False)
    rate = models.FloatField(null=True, default=5)
    learning_time = models.IntegerField(null=False)
    duration = models.IntegerField(null=False)
    image = models.ImageField(null=False)
    image_name = models.CharField(max_length=500, null=True, default="default.jpg")
    description = models.TextField()
    bgg_code = models.IntegerField(null=False)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Member(models.Model):
    INTRO_CHOICES = (
        ('search', 'جست‌وجوی اینترنت'),
        ('friends', 'معرفی دوستان'),
        ('instagram', 'اینستاگرام'),
        ('roomiz', 'سایت رومیز'),
        ('events', 'شرکت در رویدادها'),
        ('other', 'سایر'),
    )
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=50, null=False)
    card_number = models.CharField(max_length=20, null=False, unique=True)
    credit = models.FloatField(default=0, null=False)
    phone = models.CharField(max_length=15, null=False, unique=True)
    intro = models.CharField(max_length=50, choices=INTRO_CHOICES, default='other')
    year_of_birth = models.IntegerField(null=False)
    month_of_birth = models.IntegerField(null=False)
    day_of_birth = models.IntegerField(null=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Table(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return str(self.name)


class Game(models.Model):
    member = models.ForeignKey(to=Member, on_delete=models.CASCADE)
    credit_used = models.FloatField(default=0, null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=True, default="00:00:00")
    numbers = models.IntegerField(null=False)
    points = models.IntegerField(null=False, default=0)
    add_date = models.DateField(null=False)

    def __str__(self):
        return str(self.member.last_name + " " + str(self.start_time))


class ShopProduct(models.Model):
    name = models.CharField(max_length=50, null=False)
    price = models.FloatField(null=False, default=0)
    real_numbers = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name + ":" + str(self.price) + ":" + str(self.real_numbers)


class Cash(models.Model):
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ended_date_time = models.DateTimeField(null=True, blank=True)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
    is_close = models.SmallIntegerField(default=0, null=False)


class InvoiceSales(models.Model):
    SETTLEMENT_CHOICES = (
        ('BANK_CARD', 'کارت بانکی'),
        ('CASH', 'نقدی'),
    )
    factor_number = models.IntegerField(null=False, blank=False, default=0)
    created_time = models.DateTimeField(null=False)
    settle_time = models.DateTimeField(null=True, blank=True)
    cash = models.FloatField(null=False, default=0)
    pos = models.FloatField(null=False, default=0)
    discount = models.FloatField(null=False, default=0)
    employee_discount = models.FloatField(null=False, default=0)
    tax = models.FloatField(null=False, default=0)
    tip = models.FloatField(null=False, default=0)
    settlement_type = models.CharField(max_length=50, choices=SETTLEMENT_CHOICES, default='CASH')
    guest_numbers = models.IntegerField(null=False)
    is_settled = models.IntegerField(null=False, default=0)
    total_price = models.FloatField(default=0)
    member = models.ForeignKey(to=Member, on_delete=models.CASCADE, default=0)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)
    cash_desk = models.ForeignKey(Cash, null=True, blank=True, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)


class InvoicesSalesToMenuItem(models.Model):
    invoice_sales = models.ForeignKey(to=InvoiceSales, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(to=MenuItem, on_delete=models.CASCADE)
    numbers = models.IntegerField(null=False)
    description = models.CharField(max_length=60, blank=True)
    is_print = models.SmallIntegerField(default=0, null=False)


class InvoicesSalesToShopProducts(models.Model):
    invoice_sales = models.ForeignKey(to=InvoiceSales, on_delete=models.CASCADE)
    shop_product = models.ForeignKey(to=ShopProduct, on_delete=models.CASCADE)
    numbers = models.IntegerField(null=False)
    description = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return str(self.shop_product) + "+" + str(self.numbers) + "+" + str(self.id)


class InvoicesSalesToGame(models.Model):
    invoice_sales = models.ForeignKey(to=InvoiceSales, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)


class Supplier(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=30, null=False)
    salesman_name = models.CharField(max_length=50, null=False)
    salesman_phone = models.CharField(max_length=50, null=False)
    last_pay = models.DateField(blank=True, null=True)
    last_buy = models.DateField(blank=True, null=True)
    last_expense = models.DateField(blank=True, null=True)
    last_return = models.DateField(blank=True, null=True)
    remainder = models.FloatField(default=0)

    def __str__(self):
        return self.name + ":" + self.phone


class Visitor(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=30, null=False)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)


class InvoiceSettlement(models.Model):
    SETTLE_TYPES = (
        ('NOT_DEFINED', 'تعریف نشده'),
        ('CASH', 'نقدی'),
        ('CARD', 'کارت به کارت'),
        ('PAYA', 'پایا'),
        ('CHECK', 'چک'),
        ('SATNA', 'ساتنا'),
    )
    factor_number = models.IntegerField(null=False, blank=False, default=0)
    created_time = models.DateTimeField(null=False)
    payment_amount = models.FloatField(null=False)
    backup_code = models.CharField(max_length=150, null=False, default=0)
    settle_type = models.CharField(max_length=50, null=False, choices=SETTLE_TYPES, default="NOT_DEFINED")
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
    tax = models.FloatField(null=False, default=0)
    discount = models.FloatField(null=False, default=0)


class Material(models.Model):
    UNIT_TYPES = (
        ('NOT_DEFINED', 'تعریف نشده'),
        ('KG', 'کیلوگرم'),
        ('NUMBER', 'عدد'),
        ('BOX', 'بسته'),
    )
    name = models.CharField(max_length=50, null=False)
    unit = models.CharField(max_length=30, null=False, choices=UNIT_TYPES, default="NOT_DEFINED")

    def __str__(self):
        return self.name + ":" + self.unit


class MaterialToStock(models.Model):
    material = models.ForeignKey(to=Material, on_delete=models.CASCADE)
    stock = models.ForeignKey(to=Stock, on_delete=models.CASCADE)


class InvoicePurchase(models.Model):
    SETTLEMENT_TYPES = (
        ('CASH', 'نقدی'),
        ('CREDIT', 'اعتباری'),
        ('AMANi', 'امانی'),
    )
    factor_number = models.IntegerField(null=False, blank=False, default=0)
    created_time = models.DateTimeField(null=False)
    settlement_type = models.CharField(max_length=50, choices=SETTLEMENT_TYPES)
    tax = models.FloatField(null=False)
    discount = models.FloatField(null=False)
    total_price = models.FloatField(default=0)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)


class PurchaseToMaterial(models.Model):
    material = models.ForeignKey(to=Material, on_delete=models.CASCADE)
    invoice_purchase = models.ForeignKey(to=InvoicePurchase, on_delete=models.CASCADE)
    base_unit_price = models.FloatField(null=False)
    unit_numbers = models.FloatField(null=False)
    description = models.TextField(null=True, blank=True)


class PurchaseToShopProduct(models.Model):
    shop_product = models.ForeignKey(to=ShopProduct, on_delete=models.CASCADE)
    invoice_purchase = models.ForeignKey(to=InvoicePurchase, on_delete=models.CASCADE)
    base_unit_price = models.FloatField(null=False)
    unit_numbers = models.IntegerField(null=False)
    buy_numbers = models.IntegerField(null=False, default=0)
    sale_price = models.FloatField(null=False, default=0)
    description = models.TextField(null=True, blank=True)


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)


class InvoiceExpense(models.Model):
    SETTLEMENT_TYPES = (
        ('CASH', 'نقدی'),
        ('CREDIT', 'اعتباری'),
    )
    factor_number = models.IntegerField(null=False, blank=False, default=0)
    created_time = models.DateTimeField(null=False)
    price = models.FloatField(null=False)
    settlement_type = models.CharField(max_length=50, choices=SETTLEMENT_TYPES)
    tax = models.FloatField(null=False)
    discount = models.FloatField(null=False)
    expense_category = models.ForeignKey(to=ExpenseCategory, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)


class InvoiceExpenseToService(models.Model):
    service_name = models.CharField(max_length=50, null=False, blank=False, default="NOT DEFINED")
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=False)
    invoice_expense = models.ForeignKey(to=InvoiceExpense, on_delete=models.CASCADE)


class InvoiceReturn(models.Model):
    RETURN_TYPES = (
        ('CUSTOMER_TO_CAFE', 'مشتری به کافه'),
        ('CAFE_TO_SUPPLIER', 'کافه به تامین‌کننده'),
    )
    factor_number = models.IntegerField(null=False, blank=False, default=0)
    created_time = models.DateTimeField(null=False)
    return_type = models.CharField(max_length=50, choices=RETURN_TYPES)
    buy_price = models.FloatField(null=False)
    total_price = models.FloatField(null=False)
    numbers = models.IntegerField(null=False)
    shop_product = models.ForeignKey(to=ShopProduct, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)


class DeletedItemsInvoiceSales(models.Model):
    ITEM_TYPES = (
        ('SHOP', 'Shop Product'),
        ('MENU', 'Menu Item'),
        ('GAME', 'Game Item'),
    )
    created_time = models.DateTimeField(null=False)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    item_numbers = models.IntegerField(null=False)
    message = models.CharField(max_length=255)
    employee = models.ForeignKey(to=Employee, on_delete=models.SET_NULL, null=True)
    invoice_sales = models.ForeignKey(to=InvoiceSales, on_delete=models.SET_NULL, null=True)


class Reservation(models.Model):
    STATES = (
        ('waiting', 'waiting'),
        ('arrived', 'arrived'),
        ('walked', 'walked'),
    )
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    numbers = models.IntegerField(null=False)
    reserve_date = models.DateTimeField(null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    reserve_state = models.CharField(max_length=50, choices=STATES)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE, null=True)


class ReserveToTables(models.Model):
    reserve = models.ForeignKey(to=Reservation, on_delete=models.CASCADE)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)


class AmaniSale(models.Model):
    invoice_sale_to_shop = models.ForeignKey(to=InvoicesSalesToShopProducts, on_delete=models.CASCADE)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    numbers = models.IntegerField(null=False)
    sale_price = models.FloatField(null=False)
    buy_price = models.FloatField(null=False)
    created_date = models.DateTimeField(null=True, blank=True)

