from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import stripe
from decouple import config

class Payment(APIView):

    def post(self, request):
        stripe.api_key = config('STRIPE_KEY')
        test_payment_intent = stripe.PaymentIntent.create(
            amount=1000, currency='inr',
            payment_method_types=['card'],
            receipt_email='test@example.com')

        return Response(data=test_payment_intent, status=status.HTTP_200_OK)

