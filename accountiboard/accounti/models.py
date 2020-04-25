from django.db import models
from django.contrib import admin
from multiselectfield import MultiSelectField
from django.core.mail import send_mail


class User(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'cafe_owner'),
        (2, 'employee')
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30, null=False, blank=False, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, verbose_name='last login', blank=True)
    is_active = models.BooleanField(default=False)
    password = models.TextField(null=False, blank=False)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    birthday_date = models.DateField(null=True, blank=True)
    home_address = models.CharField(max_length=2500, null=False, blank=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Organization(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    shortcut_login_url = models.CharField(max_length=255, null=False, blank=False)


class Branch(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=4 * 255, null=False, blank=False)
    start_working_time = models.TimeField(null=True)
    end_working_time = models.TimeField(null=True)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)


class Employee(models.Model):
    # Personal Data
    father_name = models.CharField(max_length=255, null=True, blank=True)
    national_code = models.CharField(max_length=30, null=True, blank=True)
    # Banking Data
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_card_number = models.CharField(max_length=30, null=True, blank=True)
    shaba_number = models.CharField(max_length=255, null=True, blank=True)
    # User Base
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class CafeOwner(models.Model):
    # User Base
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)


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
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)


class MenuCategory(models.Model):
    KIND = (
        ('KITCHEN', 'آشپزخانه'),
        ('BAR', 'بار'),
        ('OTHER', 'سایر'),
    )
    name = models.CharField(max_length=30, null=True, blank=True)
    kind = models.CharField(max_length=50, choices=KIND, blank=False, null=False)
    list_order = models.IntegerField(default=0, blank=False, null=False)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    card_number = models.CharField(max_length=20, null=False, unique=True)
    phone = models.CharField(max_length=30, null=False, unique=True)
    intro = models.CharField(max_length=255, choices=INTRO_CHOICES, default='other')
    year_of_birth = models.IntegerField(null=False)
    month_of_birth = models.IntegerField(null=False)
    day_of_birth = models.IntegerField(null=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()



class TableCategory(models.Model):
    name = models.CharField(max_length=255, null=False)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Table(models.Model):
    name = models.CharField(max_length=255, null=False)
    category = models.ForeignKey(to=TableCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Game(models.Model):
    member = models.ForeignKey(to=Member, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=True, default="00:00:00")
    numbers = models.IntegerField(null=False)
    points = models.IntegerField(null=False, default=0)
    add_date = models.DateField(null=False)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member) + " " + str(self.start_time)


class ShopProduct(models.Model):
    name = models.CharField(max_length=50, null=False)
    price = models.FloatField(null=False, default=0)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ":" + str(self.price)


class Cash(models.Model):
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ended_date_time = models.DateTimeField(null=True, blank=True)
    income_report = models.IntegerField(null=False, default=0)
    outcome_report = models.IntegerField(null=False, default=0)
    event_tickets = models.IntegerField(null=False, default=0)
    current_money_in_cash = models.IntegerField(null=False, default=0)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    new_employee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
    is_close = models.SmallIntegerField(default=0, null=False)


class InvoiceSales(models.Model):
    SETTLEMENT_CHOICES = (
        ('BANK_CARD', 'کارت بانکی'),
        ('CASH', 'نقدی'),
    )
    GAME_STATES = (
        ('NO_GAME', 'بازی نمی‌خواهد'),
        ('PLAYING', 'در حال بازی'),
        ('WAIT_GAME', 'منتظر بازی'),
        ('END_GAME', 'بازی تمام شده'),
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
    member = models.ForeignKey(to=Member, on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey(to=Table, on_delete=models.CASCADE)
    ready_for_settle = models.BooleanField(default=False)
    cash_desk = models.ForeignKey(Cash, null=True, blank=True, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_do_not_want_order = models.BooleanField(default=False)
    game_state = models.CharField(max_length=50, choices=GAME_STATES, default='WAIT_GAME')

    def __str__(self):
        return "num: " + str(self.factor_number) + " total_p: " + str(self.total_price) + " Is Settled: " + str(
            self.is_settled)


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


class InvoicesSalesToShopProductsAdmin(admin.ModelAdmin):
    search_fields = ('shop_product__name',)


class InvoicesSalesToGame(models.Model):
    invoice_sales = models.ForeignKey(to=InvoiceSales, on_delete=models.CASCADE)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)


class Supplier(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=30, null=False)
    salesman_name = models.CharField(max_length=50, null=False)
    salesman_phone = models.CharField(max_length=50, null=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

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
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

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

    def __str__(self):
        return "FactorNumber: " + str(self.factor_number) + " Time: " + str(self.created_time) + str(self.supplier.name) + str(self.total_price)


class InvoicePurchaseAdmin(admin.ModelAdmin):
    search_fields = ('supplier__name',)


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
    return_numbers = models.IntegerField(null=False, default=0)
    sale_price = models.FloatField(null=False, default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "FactorNumber: " + str(self.invoice_purchase.factor_number) + " id(" + str(self.id) + ")" + str(self.shop_product.name) + "InvoicePId(" + str(
            self.invoice_purchase.id) + ")" + str(
            self.invoice_purchase.supplier.name)


class PurchaseToShopProductAdmin(admin.ModelAdmin):
    search_fields = ('shop_product__name', 'invoice_purchase__supplier__name',)


class ExpenseTag(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)


class InvoiceExpense(models.Model):
    SETTLEMENT_TYPES = (
        ('CASH', 'نقدی'),
        ('CREDIT', 'اعتباری'),
    )
    EXPENSE_KIND = (
        ("JARI_MASRAFI", "جاری مصرفی"),
        ("JARI_NOT_MASRAFI", "جاری غیر مصرفی"),
        ("NOT_JARI_MASRAFI", "غیر جاری مصرفی"),
        ("NOT_JARI_NOT_MASRAFI", "غیر جاری غیر مصرفی")
    )
    factor_number = models.IntegerField(null=False, blank=False, default=0)
    created_time = models.DateTimeField(null=False)
    price = models.FloatField(null=False)
    settlement_type = models.CharField(max_length=255, choices=SETTLEMENT_TYPES)
    expense_kind = models.CharField(max_length=255, choices=EXPENSE_KIND)
    tax = models.FloatField(null=False)
    discount = models.FloatField(null=False)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE)


class ExpenseToTag(models.Model):
    invoice_expense = models.ForeignKey(to=InvoiceExpense, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=ExpenseTag, on_delete=models.CASCADE)


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
    total_price = models.FloatField(null=False, default=0)
    numbers = models.IntegerField(null=False)
    shop_product = models.ForeignKey(to=ShopProduct, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(to=Supplier, on_delete=models.CASCADE, blank=True, null=True)
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
    new_employee = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    invoice_sales = models.ForeignKey(to=InvoiceSales, on_delete=models.SET_NULL, null=True)


class Reservation(models.Model):
    STATES = (
        ('waiting', 'waiting'),
        ('arrived', 'arrived'),
        ('walked', 'walked'),
        ('call_waiting', 'call_waiting'),
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
    is_amani = models.BooleanField(default=True)
    return_numbers = models.IntegerField(null=False, default=0)
    created_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "id(" + str(self.id) + ")" + str(self.created_date) + str(self.supplier.name) + str(
            self.invoice_sale_to_shop.shop_product.name) + "(Number : " + str(self.numbers) + ")"


class AmaniSaleAdmin(admin.ModelAdmin):
    search_fields = ('supplier__name',)


class AmaniSaleToInvoiceReturn(models.Model):
    amani_sale = models.ForeignKey(to=AmaniSale, on_delete=models.CASCADE)
    invoice_return = models.ForeignKey(to=InvoiceReturn, on_delete=models.CASCADE)
    numbers = models.IntegerField(null=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True)


class AmaniSaleToInvoicePurchaseShopProduct(models.Model):
    amani_sale = models.ForeignKey(to=AmaniSale, on_delete=models.CASCADE)
    invoice_purchase_to_shop_product = models.ForeignKey(to=PurchaseToShopProduct, on_delete=models.CASCADE)
    numbers = models.IntegerField(null=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "id(" + str(self.id) + ")" + "InvoicePtoSid(" + str(
            self.invoice_purchase_to_shop_product_id) + ")" + "amani_id(" + str(self.amani_sale_id) + ")" + str(
            self.created_date) + str(
            self.amani_sale.supplier.name) + str(
            self.invoice_purchase_to_shop_product.shop_product.name)


class PurchaseToInvoiceReturn(models.Model):
    invoice_purchase_to_shop_product = models.ForeignKey(to=PurchaseToShopProduct, on_delete=models.CASCADE)
    invoice_return = models.ForeignKey(to=InvoiceReturn, on_delete=models.CASCADE)
    numbers = models.IntegerField(null=False, default=0)
    created_date = models.DateTimeField(auto_now_add=True)


class DeletedInvoiceSale(models.Model):
    invoice_sale = models.ForeignKey(to=InvoiceSales, on_delete=models.CASCADE)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Lottery(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    prize = models.CharField(max_length=255, null=False)
    is_give_prize = models.IntegerField(default=0)
    user = models.ForeignKey(to=Member, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)


class GiftCodeSupplier(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    phone = models.CharField(max_length=30, blank=False, null=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GiftCode(models.Model):
    CATEGORIES = (
        ("BAR", "آیتم‌های بار"),
        ("KITCHEN", "آیتم‌های آشپزخانه"),
        ("OTHER", "آیتم‌های سایر"),
        ("SHOP", "محصولات فروشگاهی"),
        ("GAME", "بازی"),
    )
    credit_categories = MultiSelectField(max_length=50, choices=CATEGORIES)
    name = models.CharField(max_length=30, blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    number_will_use = models.IntegerField(default=1)
    number_used = models.IntegerField(default=0)
    gift_code_supplier = models.ForeignKey(to=GiftCodeSupplier, on_delete=models.CASCADE)

    def __str__(self):
        return "Name: %s, Price: %d" % (self.name, self.price)


class Credit(models.Model):
    CATEGORIES = (
        ("BAR", "آیتم‌های بار"),
        ("KITCHEN", "آیتم‌های آشپزخانه"),
        ("OTHER", "آیتم‌های سایر"),
        ("SHOP", "محصولات فروشگاهی"),
        ("GAME", "بازی"),
    )
    credit_categories = MultiSelectField(max_length=50, choices=CATEGORIES)
    created_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=False, blank=False)
    total_price = models.IntegerField(null=False, blank=False)
    used_price = models.IntegerField(default=0)
    member = models.ForeignKey(to=Member, on_delete=models.CASCADE)
    gift_code = models.ForeignKey(to=GiftCode, on_delete=models.CASCADE, blank=True, null=True)


class CreditToInvoiceSale(models.Model):
    credit = models.ForeignKey(to=Credit, null=True, on_delete=models.SET_NULL)
    invoice_sale = models.ForeignKey(to=InvoiceSales, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    used_price = models.IntegerField(default=0)
