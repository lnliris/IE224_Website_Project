from django.contrib import admin
from orders.models import Order, Coupon, OrderHistory

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'ordered_date', 'get_total']
    list_filter = ['status', 'ordered_date', 'user']
    search_fields = ['user__username', 'status']
    readonly_fields = ['ordered_date']

    def get_total(self, obj):
        return obj.get_total()

    get_total.short_description = 'Total'


# Register Coupon model
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']
    search_fields = ['code']
    list_filter = ['amount']


# Register OrderHistory model
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'status', 'updated_at']
    list_filter = ['status', 'updated_at', 'user']
    search_fields = ['user__username', 'order__id']
