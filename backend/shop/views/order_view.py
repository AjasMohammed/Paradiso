from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from shop.models import OrderItem, Product, Order
from shop.serializers import OrderSerializer


class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.pk

        order_items = sorted(data.pop('products', []),
                             key=lambda item: item['id'])
        order_items_ids = [id['id'] for id in order_items]

        products = Product.objects.filter(
            id__in=order_items_ids).order_by('id')

        serializer = OrderSerializer(data=data)
        index = 0
        if serializer.is_valid():
            order = serializer.save()
            order_id = order.id
            for product in products:
                OrderItem.objects.create(
                    order=order, product=product, quantity=order_items[index]['quantity'])
                index += 1
            context = {
                'order_id': order_id
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderConformation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        order = Order.objects.prefetch_related(
            'orderitem_set').get(user=user, id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        payment_id = request.data.get('payment_id')
        order = Order.objects.get(id=id)
        order.is_paid = True
        order.payment_id = payment_id
        order.status = 'processing'
        order.save()
        return Response(status=status.HTTP_200_OK)
