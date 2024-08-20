from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Billing
from cart.models import Cart
from .serializers import BillingSerializer

class GenerateBillView(generics.CreateAPIView):
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        total_price = cart.total_price

        billing = Billing.objects.create(
            user=request.user,
            cart=cart,
            total_price=total_price
        )

        return Response(BillingSerializer(billing).data, status=status.HTTP_201_CREATED)
