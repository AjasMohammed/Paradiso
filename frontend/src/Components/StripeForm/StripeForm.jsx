import React, { useState, useContext } from "react";
import "./StripeForm.css";
import { CardElement, useElements, useStripe } from "@stripe/react-stripe-js";
import axios from "../../Constants/axios";
import { cartContext } from "../../Store/Context";

function StripeForm({ onPaymentDetails }) {
  const [error, setError] = useState(null);
  const [email, setEmail] = useState("");
  const stripe = useStripe();
  const elements = useElements();

  const { totalAmount } = useContext(cartContext);

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
    const data = {
      payment_method_id: paymentMethod.id,
      email: email,
      total: totalAmount
    };
    axios.post("/payments/payment/", data).then((response) => {
      console.log(response.data);
      onPaymentDetails();
    });
  };

  return (
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

        <label for="card-element">Credit or Debit Card</label>
        <CardElement
          id="card-element"
          className="form-control"
          onChange={handleChange}
        />
        <div className="card-errors" role="alert">
          {error}
        </div>
      </div>
      <button type="submit" className="submit-btn btn btn-dark">
        Submit Payment
      </button>
    </form>
  );
}

export default StripeForm;
