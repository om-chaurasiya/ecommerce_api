from django.contrib import admin
from .models import Product, Cart, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description', 'price', 'discount')
    search_fields = ('name', 'description')
    list_filter = ('price', 'discount')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user_id', 'created_at')
    search_fields = ('user__email',)  # Assuming user model uses email field

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id','cart__user__id','cart__id', 'product__id', 'quantity', 'total_price')
    list_filter = ('cart', 'product')
    search_fields = ('product__name',)