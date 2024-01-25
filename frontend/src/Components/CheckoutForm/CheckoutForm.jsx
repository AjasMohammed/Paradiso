import React from "react";
import { CardElement, useElements, useStripe } from "@stripe/react-stripe-js";
import { useState } from "react";
import axios from "../../Constants/axios";

function CheckoutForm() {
  const [error, setError] = useState(null);
  const [email, setEmail] = useState("");
  const stripe = useStripe();
  const elements = useElements();

  // Handle real-time validation errors from the CardElement.
  const handleChange = (event) => {
    if (event.error) {
      setError(event.error.message);
    } else {
      setError(null);
    }
  };

  // Handle form submission.
  const handleSubmit = async (event) => {
    event.preventDefault();
    const card = elements.getElement(CardElement);
    const { paymentMethod, error } = await stripe.createPaymentMethod({
      type: "card",
      card: card,
    });
    console.log(paymentMethod);
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="stripe-form">
        <div className="form-row">
          <label htmlFor="email">Email Address</label>
          <br />
          <input
            className="form-control"
            id="email"
            name="name"
            type="email"
            placeholder="jenny.rosen@example.com"
            required
            value={email}
            onChange={(event) => {
              setEmail(event.target.value);
            }}
          />
        </div>
        <div className="form-row">
          <label for="card-element">Credit or debit card</label>
          <CardElement id="card-element" onChange={handleChange} />
          <div className="card-errors" role="alert">
            {error}
          </div>
        </div>
        <button type="submit" className="submit-btn">
          Submit Payment
        </button>
      </form>
    </div>
  );
}

export default CheckoutForm;