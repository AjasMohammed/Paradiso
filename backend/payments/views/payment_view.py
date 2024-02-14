from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class PaymentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stripe.api_key = settings.STRIPE_API_KEY
        id = request.data.get('id')
        payment_list = stripe.PaymentIntent.retrieve(id)
        confirm = stripe.PaymentIntent.confirm(
            id
        )
        return Response(payment_list, status=status.HTTP_200_OK)

    def post(self, request):
        stripe.api_key = settings.STRIPE_API_KEY

        data = request.data
        email = data['email']
        payment_method_id = data['payment_method_id']
        total = data['total']

        total_in_paise = int(float(total) * 100)

        customer_data = stripe.Customer.list(email=email).data
        if len(customer_data) == 0:
            customer = stripe.Customer.create(
                email=email,
                payment_method=payment_method_id,
            )
        else:
            customer = customer_data[0]

        test_payment_intent = stripe.PaymentIntent.create(
            customer=customer,
            amount=total_in_paise, currency='inr',
            payment_method=payment_method_id,
            confirm=True,
            automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never'
                }
        )

        conformation = stripe.PaymentIntent.confirm(
            test_payment_intent['id'],
        )
        print(conformation)

        return Response(data=test_payment_intent, status=status.HTTP_200_OK)


# class CustomerView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         stripe.api_key = settings.STRIPE_API_KEY
        
#         return Response({'message': 'success', 'customer_id': customer.id}, status=status.HTTP_200_OK)
