import React, { useState, useEffect, useContext } from "react";
import "./StripeElement.css";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js/pure";
import StripeForm from "../StripeForm/StripeForm";
import axios from "../../Constants/axios";
import { cartContext } from "../../Store/Context";

const stripePromise = loadStripe(
  "pk_test_51Np6VHSA71CBHoaJrOi7kCIhgvbW0AvueVLGfP9WByg9sFlRVNlMXHZDGV88nbJTfyxJZr0PGWlXR6rLkt9wY1IG00OkMzrjGe"
);

function StripeElement({ onPaymentDetails }) {
  const [clientSecret, setClientSecret] = useState("");
  const { totalAmount } = useContext(cartContext);
  console.log(totalAmount);

  useEffect(() => {
    axios
      .post("/payments/initiate-payment/", { total: totalAmount })
      .then((res) => {
        setClientSecret(res.data.client_secret);
        console.log(res.data.client_secret);
      });
  }, []);

  const appearance = {
    theme: "stripe",
  };
  const options = {
    clientSecret,
    appearance,
  };

  return (
    clientSecret && (
      <Elements options={options} stripe={stripePromise}>
        <StripeForm onPaymentDetails={onPaymentDetails} options={options} />
      </Elements>
    )
  );
}

export default StripeElement;
