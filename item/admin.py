from django.contrib import admin

# Register your models here.
from .models import (
    InhouseReagent,
    Item,
    Stock,
    StockEntry,
    StockValidation,
    Unit,
    Usage,
    WatchList,
)

admin.site.register(InhouseReagent)

admin.site.register(Item)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("source", "lot_number", "delivery_date", "expiry_date", "condition")
    list_filter = ("condition", "delivery_date", "expiry_date")


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ("stock", "ordinal_number", "in_use_date", "last_updated")
    list_filter = ("stock", "in_use_date")


@admin.register(StockValidation)
class StockValidationAdmin(admin.ModelAdmin):
    list_display = ("stock", "validation")
    list_filter = ("stock",)


admin.site.register(Unit)


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ("stock_entry", "used_quantity", "used_date", "used_unit", "used_by")
    list_filter = ("stock_entry", "used_date", "used_unit", "used_by")


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ("stock", "threshold", "threshold_type", "last_checked", "notification")
    list_filter = ("stock", "threshold_type", "last_checked", "notification")
