from django.shortcuts import get_object_or_404
from shop.models import Product, Cart, CartItem
from shop.serializers import CartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class AddToCart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        product = Product.objects.get(id=id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response(status=status.HTTP_200_OK)


class GetCartItems(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, is_count):
        try:
            cart = Cart.objects.prefetch_related(
                'cartitem_set').get(user=request.user)

            items = cart.cartitem_set.all()
            if is_count == 'true':
                item_no = items.count()
                return Response({'count': item_no})
            elif is_count == 'false':
                serializer = CartItemSerializer(items, many=True)

                context = {
                    'data': serializer.data,
                    'total': cart.total
                }

            return Response(context, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Cart is Empty'}, status=status.HTTP_204_NO_CONTENT)


class RemoveFromCart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(id=id)
        user_cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=user_cart, product=product)

        cart_item.delete()
        return Response(status=status.HTTP_200_OK)


class Check_In_Cart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            cart_items = get_object_or_404(CartItem, cart=cart, product_id=id)
            return Response(True)
        except:
            return Response(False)
