import React from "react";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js/pure";
import StripeForm from "../StripeForm/StripeForm";

const stripPromise = loadStripe(
  "pk_test_51Np6VHSA71CBHoaJrOi7kCIhgvbW0AvueVLGfP9WByg9sFlRVNlMXHZDGV88nbJTfyxJZr0PGWlXR6rLkt9wY1IG00OkMzrjGe"
);
function StripeElement({ onPaymentDetails }) {
  return (
    <Elements stripe={stripPromise}>
      <StripeForm onPaymentDetails={onPaymentDetails} />
    </Elements>
  );
}

export default StripeElement;
