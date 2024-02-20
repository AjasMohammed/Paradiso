from django.urls import path
from payments.views import InitiatePayment


urlpatterns = [
    path('initiate-payment/', InitiatePayment.as_view(), name='initiate_payment'),
    # path('customer/', CustomerView.as_view(), name='customer'),
]