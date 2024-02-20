from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class InitiatePayment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stripe.api_key = settings.STRIPE_API_KEY
        id = request.data.get('id')
        payment_list = stripe.PaymentIntent.retrieve(id)
        return Response(payment_list, status=status.HTTP_200_OK)

    def post(self, request):
        stripe.api_key = settings.STRIPE_API_KEY

        data = request.data
        print(data)
        email = request.user.email
        total = data.get('total')  # Use get method to safely get the value without raising KeyError

        total_in_paise = int(float(total) * 100)

        try:
            customer_data = stripe.Customer.list(email=email).data
            if len(customer_data) == 0:
                customer = stripe.Customer.create(
                    email=email,
                )
            else:
                customer = customer_data[0]

            test_payment_intent = stripe.PaymentIntent.create(
                customer=customer,
                amount=total_in_paise,
                currency='inr',
                automatic_payment_methods={
                    'enabled': True,
                }
            )

            data = {
                "client_secret": test_payment_intent['client_secret']
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other exceptions
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


