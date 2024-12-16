from django.contrib import admin
from orders.models import Item, OrderItem, Order

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'description', 'slug']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['price', 'discount_price']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity', 'get_total_item_price', 'get_total_discount_item_price', 'get_amount_saved']
    list_filter = ['item', 'user']
    search_fields = ['user__username', 'item__title']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'ordered_date', 'get_total']
    list_filter = ['status', 'ordered_date', 'user']
    search_fields = ['user__username', 'status']
    readonly_fields = ['ordered_date']
    inlines = []

    def get_total(self, obj):
        return obj.get_total()

    get_total.short_description = 'Total'

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)