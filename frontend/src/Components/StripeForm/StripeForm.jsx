import React, { useState, useEffect } from "react";
import "./StripeForm.css";
import {
  useElements,
  useStripe,
  PaymentElement,
} from "@stripe/react-stripe-js";

function StripeForm({ onPaymentDetails, options }) {
  const [error, setError] = useState(null);
  const stripe = useStripe();
  const elements = useElements();

  const [message, setMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const paymentElementOptions = {
    layout: "tabs",
  };

  useEffect(() => {
    if (!stripe) {
      return;
    }

    const clientSecret = options.clientSecret;

    if (!clientSecret) {
      return;
    }
    stripe.retrievePaymentIntent(clientSecret).then(({ paymentIntent }) => {
      switch (paymentIntent.status) {
        case "succeeded":
          setMessage("Payment succeeded!");
          onPaymentDetails();
          break;
        case "processing":
          setMessage("Your payment is processing.");
          break;
        case "requires_payment_method":
          setMessage("Your payment was not successful, please try again.");
          setIsLoading(false)
          break;
        default:
          setMessage("Something went wrong.");
          setIsLoading(false)
          break;
      }
    });
    return () => {
      setMessage("");
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      // Stripe.js hasn't yet loaded.
      // Make sure to disable form submission until Stripe.js has loaded.
      return;
    }
    setIsLoading(true);
    const { error, paymentIntent } = await stripe.confirmPayment({
      elements,
      redirect: "if_required",
      confirmParams: {
        // Make sure to change this to your payment completion page
        return_url: "",
      },
    });

    // This point will only be reached if there is an immediate error when
    // confirming the payment. Otherwise, your customer will be redirected to
    // your `return_url`. For some payment methods like iDEAL, your customer will
    // be redirected to an intermediate site first to authorize the payment, then
    // redirected to the `return_url`.
    if (error) {
      if (error.type === "card_error" || error.type === "validation_error") {
        setMessage(error.message);
      } else {
        console.log(error);
        setMessage("An unexpected error occurred.");
      }
    }else if (paymentIntent && paymentIntent.status == "succeeded"){
      onPaymentDetails(paymentIntent.id)
    }
    console.log(paymentIntent);
    
    setIsLoading(false);
  };

  return (
    <form id="payment-form" onSubmit={handleSubmit}>
      <PaymentElement id="payment-element" options={paymentElementOptions} />
      <button disabled={isLoading || !stripe || !elements} id="submit">
        <span id="button-text">
          {isLoading ? <div className="spinner" id="spinner"></div> : "Pay now"}
        </span>
      </button>
      {/* Show any error or success messages */}
      {message && <div id="payment-message">{message}</div>}
    </form>
  );
}

export default StripeForm;
