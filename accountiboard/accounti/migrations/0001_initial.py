# Generated by Django 2.1.5 on 2020-05-31 19:45

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmaniSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField()),
                ('sale_price', models.FloatField()),
                ('buy_price', models.FloatField()),
                ('is_amani', models.BooleanField(default=True)),
                ('return_numbers', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AmaniSaleToInvoicePurchaseShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('amani_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.AmaniSale')),
            ],
        ),
        migrations.CreateModel(
            name='AmaniSaleToInvoiceReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('amani_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.AmaniSale')),
            ],
        ),
        migrations.CreateModel(
            name='Boardgame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('HEAVY', 'استراتژی سنگین'), ('LIGHT', 'استراتژی سبک'), ('FAMILY', 'خانواده و مهمانی'), ('ABSTRACT', 'استراتژی انتزاعی')], max_length=50)),
                ('min_players', models.IntegerField()),
                ('max_players', models.IntegerField()),
                ('best_players', models.IntegerField()),
                ('rate', models.FloatField(default=5, null=True)),
                ('learning_time', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('image_name', models.CharField(default='default.jpg', max_length=500, null=True)),
                ('description', models.TextField()),
                ('bgg_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=1020)),
                ('start_working_time', models.TimeField(null=True)),
                ('end_working_time', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CafeOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('ended_date_time', models.DateTimeField(blank=True, null=True)),
                ('income_report', models.IntegerField(default=0)),
                ('outcome_report', models.IntegerField(default=0)),
                ('event_tickets', models.IntegerField(default=0)),
                ('current_money_in_cash', models.IntegerField(default=0)),
                ('is_close', models.SmallIntegerField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_categories', multiselectfield.db.fields.MultiSelectField(choices=[('BAR', 'آیتم\u200cهای بار'), ('KITCHEN', 'آیتم\u200cهای آشپزخانه'), ('OTHER', 'آیتم\u200cهای سایر'), ('SHOP', 'محصولات فروشگاهی'), ('GAME', 'بازی')], max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('expire_time', models.DateTimeField()),
                ('total_price', models.IntegerField()),
                ('used_price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CreditToInvoiceSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('used_price', models.IntegerField(default=0)),
                ('credit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounti.Credit')),
            ],
        ),
        migrations.CreateModel(
            name='DeletedInvoiceSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedItemsInvoiceSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField()),
                ('item_type', models.CharField(choices=[('SHOP', 'Shop Product'), ('MENU', 'Menu Item'), ('GAME', 'Game Item')], max_length=50)),
                ('item_numbers', models.IntegerField()),
                ('message', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_roles', multiselectfield.db.fields.MultiSelectField(choices=[('MANAGER', 'MANAGER'), ('CASHIER', 'CASHIER'), ('ACCOUNTANT', 'ACCOUNTANT'), ('STAFF', 'STAFF')], default='STAFF', max_length=50)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('national_code', models.CharField(blank=True, max_length=30, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_card_number', models.CharField(blank=True, max_length=30, null=True)),
                ('shaba_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeToBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_level', models.IntegerField(default=3)),
                ('position', models.CharField(blank=True, max_length=55)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseToTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(default='00:00:00', null=True)),
                ('numbers', models.IntegerField()),
                ('points', models.IntegerField(default=0)),
                ('add_date', models.DateField()),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='GiftCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_categories', multiselectfield.db.fields.MultiSelectField(choices=[('BAR', 'آیتم\u200cهای بار'), ('KITCHEN', 'آیتم\u200cهای آشپزخانه'), ('OTHER', 'آیتم\u200cهای سایر'), ('SHOP', 'محصولات فروشگاهی'), ('GAME', 'بازی')], max_length=50)),
                ('name', models.CharField(max_length=30)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expire_time', models.DateTimeField()),
                ('price', models.IntegerField()),
                ('number_will_use', models.IntegerField(default=1)),
                ('number_used', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GiftCodeSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_number', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField()),
                ('price', models.FloatField()),
                ('settlement_type', models.CharField(choices=[('CASH', 'نقدی'), ('CREDIT', 'اعتباری')], max_length=255)),
                ('expense_kind', models.CharField(choices=[('JARI_MASRAFI', 'جاری مصرفی'), ('JARI_NOT_MASRAFI', 'جاری غیر مصرفی'), ('NOT_JARI_MASRAFI', 'غیر جاری مصرفی'), ('NOT_JARI_NOT_MASRAFI', 'غیر جاری غیر مصرفی')], max_length=255)),
                ('tax', models.FloatField()),
                ('discount', models.FloatField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceExpenseToService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(default='NOT DEFINED', max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField()),
                ('invoice_expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceExpense')),
            ],
        ),
        migrations.CreateModel(
            name='InvoicePurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_number', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField()),
                ('settlement_type', models.CharField(choices=[('CASH', 'نقدی'), ('CREDIT', 'اعتباری'), ('AMANi', 'امانی')], max_length=50)),
                ('tax', models.FloatField()),
                ('discount', models.FloatField()),
                ('total_price', models.FloatField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_number', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField()),
                ('return_type', models.CharField(choices=[('CUSTOMER_TO_CAFE', 'مشتری به کافه'), ('CAFE_TO_SUPPLIER', 'کافه به تامین\u200cکننده')], max_length=50)),
                ('total_price', models.FloatField(default=0)),
                ('numbers', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_number', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField()),
                ('settle_time', models.DateTimeField(blank=True, null=True)),
                ('cash', models.FloatField(default=0)),
                ('pos', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('employee_discount', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('tip', models.FloatField(default=0)),
                ('settlement_type', models.CharField(choices=[('BANK_CARD', 'کارت بانکی'), ('CASH', 'نقدی')], default='CASH', max_length=50)),
                ('guest_numbers', models.IntegerField()),
                ('is_settled', models.IntegerField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('ready_for_settle', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_do_not_want_order', models.BooleanField(default=False)),
                ('game_state', models.CharField(choices=[('NO_GAME', 'بازی نمی\u200cخواهد'), ('PLAYING', 'در حال بازی'), ('WAIT_GAME', 'منتظر بازی'), ('END_GAME', 'بازی تمام شده')], default='WAIT_GAME', max_length=50)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
                ('cash_desk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Cash')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceSettlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_number', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField()),
                ('payment_amount', models.FloatField()),
                ('backup_code', models.CharField(default=0, max_length=150)),
                ('settle_type', models.CharField(choices=[('NOT_DEFINED', 'تعریف نشده'), ('CASH', 'نقدی'), ('CARD', 'کارت به کارت'), ('PAYA', 'پایا'), ('CHECK', 'چک'), ('SATNA', 'ساتنا')], default='NOT_DEFINED', max_length=50)),
                ('tax', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='InvoicesSalesToGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Game')),
                ('invoice_sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceSales')),
            ],
        ),
        migrations.CreateModel(
            name='InvoicesSalesToMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=60)),
                ('is_print', models.SmallIntegerField(default=0)),
                ('invoice_sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceSales')),
            ],
        ),
        migrations.CreateModel(
            name='InvoicesSalesToShopProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=60)),
                ('invoice_sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceSales')),
            ],
        ),
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('prize', models.CharField(max_length=255)),
                ('is_give_prize', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('unit', models.CharField(choices=[('NOT_DEFINED', 'تعریف نشده'), ('KG', 'کیلوگرم'), ('NUMBER', 'عدد'), ('BOX', 'بسته')], default='NOT_DEFINED', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialToStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Material')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=20, unique=True)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('intro', models.CharField(choices=[('search', 'جست\u200cوجوی اینترنت'), ('friends', 'معرفی دوستان'), ('instagram', 'اینستاگرام'), ('roomiz', 'سایت رومیز'), ('events', 'شرکت در رویدادها'), ('other', 'سایر')], default='other', max_length=255)),
                ('year_of_birth', models.IntegerField()),
                ('month_of_birth', models.IntegerField()),
                ('day_of_birth', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('kind', models.CharField(choices=[('KITCHEN', 'آشپزخانه'), ('BAR', 'بار'), ('OTHER', 'سایر')], max_length=50)),
                ('list_order', models.IntegerField(default=0)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('price', models.CharField(blank=True, max_length=30, null=True)),
                ('is_delete', models.SmallIntegerField(default=0)),
                ('menu_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.MenuCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('shortcut_login_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='PrinterToCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.MenuCategory')),
                ('printer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Printer')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseToInvoiceReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseToMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_unit_price', models.FloatField()),
                ('unit_numbers', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('invoice_purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoicePurchase')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Material')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseToShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_unit_price', models.FloatField()),
                ('unit_numbers', models.IntegerField()),
                ('buy_numbers', models.IntegerField(default=0)),
                ('return_numbers', models.IntegerField(default=0)),
                ('sale_price', models.FloatField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('invoice_purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoicePurchase')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('numbers', models.IntegerField()),
                ('reserve_date', models.DateTimeField(blank=True, null=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('reserve_state', models.CharField(choices=[('waiting', 'waiting'), ('arrived', 'arrived'), ('walked', 'walked'), ('call_waiting', 'call_waiting')], max_length=50)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='ReserveToTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Reservation')),
            ],
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockToBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=30)),
                ('salesman_name', models.CharField(max_length=50)),
                ('salesman_phone', models.CharField(max_length=50)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TableCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=False)),
                ('password', models.TextField()),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'cafe_owner'), (2, 'employee')])),
                ('birthday_date', models.DateField(blank=True, null=True)),
                ('home_address', models.CharField(blank=True, max_length=2500)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=30)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier')),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.TableCategory'),
        ),
        migrations.AddField(
            model_name='reservetotables',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Table'),
        ),
        migrations.AddField(
            model_name='purchasetoshopproduct',
            name='shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.ShopProduct'),
        ),
        migrations.AddField(
            model_name='purchasetoinvoicereturn',
            name='invoice_purchase_to_shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.PurchaseToShopProduct'),
        ),
        migrations.AddField(
            model_name='purchasetoinvoicereturn',
            name='invoice_return',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceReturn'),
        ),
        migrations.AddField(
            model_name='member',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='materialtostock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Stock'),
        ),
        migrations.AddField(
            model_name='material',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='lottery',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='lottery',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Member'),
        ),
        migrations.AddField(
            model_name='invoicessalestoshopproducts',
            name='shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.ShopProduct'),
        ),
        migrations.AddField(
            model_name='invoicessalestomenuitem',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.MenuItem'),
        ),
        migrations.AddField(
            model_name='invoicesettlement',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier'),
        ),
        migrations.AddField(
            model_name='invoicesales',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Member'),
        ),
        migrations.AddField(
            model_name='invoicesales',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Table'),
        ),
        migrations.AddField(
            model_name='invoicereturn',
            name='shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.ShopProduct'),
        ),
        migrations.AddField(
            model_name='invoicereturn',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier'),
        ),
        migrations.AddField(
            model_name='invoicepurchase',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier'),
        ),
        migrations.AddField(
            model_name='invoiceexpense',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier'),
        ),
        migrations.AddField(
            model_name='giftcodesupplier',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='giftcode',
            name='gift_code_supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.GiftCodeSupplier'),
        ),
        migrations.AddField(
            model_name='game',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Member'),
        ),
        migrations.AddField(
            model_name='expensetotag',
            name='invoice_expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceExpense'),
        ),
        migrations.AddField(
            model_name='expensetotag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.ExpenseTag'),
        ),
        migrations.AddField(
            model_name='expensetag',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.User'),
        ),
        migrations.AddField(
            model_name='deleteditemsinvoicesales',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounti.User'),
        ),
        migrations.AddField(
            model_name='deleteditemsinvoicesales',
            name='invoice_sales',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounti.InvoiceSales'),
        ),
        migrations.AddField(
            model_name='deletedinvoicesale',
            name='invoice_sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceSales'),
        ),
        migrations.AddField(
            model_name='credittoinvoicesale',
            name='invoice_sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceSales'),
        ),
        migrations.AddField(
            model_name='credit',
            name='gift_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.GiftCode'),
        ),
        migrations.AddField(
            model_name='credit',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Member'),
        ),
        migrations.AddField(
            model_name='cash',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounti.User'),
        ),
        migrations.AddField(
            model_name='cafeowner',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='cafeowner',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.User'),
        ),
        migrations.AddField(
            model_name='branch',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Organization'),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch'),
        ),
        migrations.AddField(
            model_name='amanisaletoinvoicereturn',
            name='invoice_return',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoiceReturn'),
        ),
        migrations.AddField(
            model_name='amanisaletoinvoicepurchaseshopproduct',
            name='invoice_purchase_to_shop_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.PurchaseToShopProduct'),
        ),
        migrations.AddField(
            model_name='amanisale',
            name='invoice_sale_to_shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.InvoicesSalesToShopProducts'),
        ),
        migrations.AddField(
            model_name='amanisale',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier'),
        ),
    ]
