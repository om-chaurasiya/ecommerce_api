
from rest_framework import serializers
from .models import Cart, CartItem, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discount']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_discount = serializers.SerializerMethodField()
    def get_total_discount(self, obj):
        total_discount = sum(
            item.quantity * item.product.discount for item in obj.items.all() if item.product.discount
        )
        return total_discount

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price','total_discount']
