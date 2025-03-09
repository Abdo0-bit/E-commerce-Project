from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem ,Shipping
from django.contrib.admin import AdminSite

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'picture')  
    search_fields = ('name', 'description')             
    list_filter = ('price', 'stock')                    
    ordering = ('-id',)                                  
    readonly_fields = ('id',)                           


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')                  
    search_fields = ('user__username',)                 
    ordering = ('-created',)                         
    date_hierarchy = 'created'                           


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')  
    search_fields = ('product__name',)                             
    list_filter = ('cart__user',)                                 
    ordering = ('-id',)


    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'total_price')  
    search_fields = ('user__username',)                            
    list_filter = ('status', 'created_at')                       
    ordering = ('-created_at',)                                    
    date_hierarchy = 'created_at'

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    search_fields = ('product__name', 'order__user__username')
    ordering = ('-id',)


    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone', 'address', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
    ('User Information', {
        'fields': ('user', 'full_name', 'email')
    }),
    ('Shipping Details', {
        'fields': ('address', 'phone')
    }),
    ('Timestamps', {
        'fields': ('created_at',),
        'classes': ('collapse',),  
    }),
)

