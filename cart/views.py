
from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer,ProductSerializer
from .permissions import IsSuperUser 



class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)



class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            # Fetch the cart item by ID and ensure it belongs to the authenticated user's cart
            cart_item = CartItem.objects.get(id=kwargs['pk'], cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        quantity_to_remove = request.data.get('quantity', None)
        if quantity_to_remove is None:
            return Response({"detail": "Quantity must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity_to_remove = int(quantity_to_remove)
        except ValueError:
            return Response({"detail": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_to_remove <= 0:
            return Response({"detail": "Quantity must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_to_remove >= cart_item.quantity:
            # If the quantity to remove is greater than or equal to the cart item's quantity, delete the item
            cart_item.delete()
            return Response({"detail": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Otherwise, decrease the quantity of the item in the cart
            cart_item.quantity -= quantity_to_remove
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only superusers can create products
            return [IsSuperUser()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # Save the new product
        serializer.save()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]