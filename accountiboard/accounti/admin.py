from django.contrib import admin
from accounti.models import *


class CashAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date_time',)


admin.site.register(User)
admin.site.register(CafeOwner)
admin.site.register(Organization)
admin.site.register(Employee)
admin.site.register(EmployeeToBranch)
admin.site.register(Branch)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(Stock)
admin.site.register(StockToBranch)
admin.site.register(Boardgame)
admin.site.register(Member)
admin.site.register(Table)
admin.site.register(TableCategory)
admin.site.register(InvoiceSales)
admin.site.register(InvoicesSalesToMenuItem)
admin.site.register(Game)
admin.site.register(InvoicesSalesToGame)
admin.site.register(Printer)
admin.site.register(PrinterToCategory)
admin.site.register(Supplier)
admin.site.register(Visitor)
admin.site.register(InvoiceSettlement)
admin.site.register(Material)
admin.site.register(MaterialToStock)
admin.site.register(ShopProduct)
admin.site.register(InvoicePurchase, InvoicePurchaseAdmin)
admin.site.register(InvoiceExpense)
admin.site.register(PurchaseToMaterial)
admin.site.register(PurchaseToShopProduct, PurchaseToShopProductAdmin)
admin.site.register(InvoicesSalesToShopProducts, InvoicesSalesToShopProductsAdmin)
admin.site.register(InvoiceReturn)
admin.site.register(DeletedItemsInvoiceSales)
admin.site.register(DeletedInvoiceSale)
admin.site.register(ExpenseTag)
admin.site.register(ExpenseToTag)
admin.site.register(Reservation)
admin.site.register(ReserveToTables)
admin.site.register(AmaniSale, AmaniSaleAdmin)
admin.site.register(AmaniSaleToInvoiceReturn)
admin.site.register(PurchaseToInvoiceReturn)
admin.site.register(AmaniSaleToInvoicePurchaseShopProduct)
admin.site.register(Lottery)
admin.site.register(Cash, CashAdmin)
admin.site.register(Credit)
admin.site.register(CreditToInvoiceSale)
admin.site.register(GiftCodeSupplier)
admin.site.register(GiftCode)
admin.site.register(Transaction)
admin.site.register(Bundle)
admin.site.register(LatestNews)
