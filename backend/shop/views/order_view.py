from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from shop.models import Order, OrderItem, Product
from shop.serializers import OrderSerializer


class PlaceOrder(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.pk

        order_items = data.pop('products', [])
        order_items_ids = [id['product'] for id in order_items]
        products = Product.objects.filter(id__in=order_items_ids)

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()

            for product in products:
                OrderItem.objects.create(order=order, product=product)
            
            return Response({'message': 'Order Placed Successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
