from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('cart_id', 'created_at', 'updated_at')
#
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('product', 'cart', 'quantity', 'is_active')
#
# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem, CartItemAdmin)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'total_price'

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'created_at', 'updated_at']
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)

