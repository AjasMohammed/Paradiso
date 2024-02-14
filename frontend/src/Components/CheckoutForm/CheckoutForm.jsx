import React, { useContext, useState } from "react";
import "./CheckoutForm.css";
import axios from "../../Constants/axios";
import { cartContext } from "../../Store/Context";

function CheckoutForm(props) {
  const { onUserDetails } = props;
  const { cartItems, totalAmount } = useContext(cartContext);

  const [phone, setPhone] = useState(null);
  const [address, setAddress] = useState(null);
  const [city, setCity] = useState(null);
  const [zipCode, setZipCode] = useState(null);
  const handleSubmit = (e) => {
    e.preventDefault();
    // const prodId = cartItems.map((item)=>{
    //   let data = {
    //     product: item.id,
    //     // quantity: 1
    //   }
    //   return data
    // })
    // console.log(prodId);
    const data = {
      phone: phone,
      address: address,
      city: city,
      zipcode: zipCode,
      amount: totalAmount,
      products: cartItems,
    };
    // axios.defaults.xsrfCookieName = "csrftoken";
    // axios.defaults.xsrfHeaderName = "X-CSRFToken";
    // axios.post("shop/place-order/", data).then((response) => {
    //   if (response.status === 200){
    //     onUserDetails()
    //   }
    // });
    onUserDetails()
  };
  return (
    <>
      <div className="order-form">
        <form className="row g-3" onSubmit={handleSubmit}>
          <div className="col-md-6">
            <label htmlFor="inputPhone4" className="form-label">
              Phone Number
            </label>
            <input
              required="true"
              type="tel"
              className="form-control"
              id="inputPhone4"
              onChange={(e) => {
                setPhone(e.target.value);
              }}
            />
          </div>
          <div className="col-12">
            <label htmlFor="inputAddress" className="form-label">
              Address
            </label>
            <textarea
              required="true"
              type="text"
              className="form-control"
              id="inputAddress"
              onChange={(e) => {
                setAddress(e.target.value);
              }}
            />
          </div>
          <div className="col-md-4">
            <label htmlFor="inputCity" className="form-label">
              City
            </label>
            <input
              required="true"
              type="text"
              className="form-control"
              id="inputCity"
              onChange={(e) => {
                setCity(e.target.value);
              }}
            />
          </div>
          <div className="col-md-3">
            <label htmlFor="inputZip" className="form-label">
              Zip
            </label>
            <input
              required="true"
              type="text"
              className="form-control"
              id="inputZip"
              onChange={(e) => {
                setZipCode(e.target.value);
              }}
            />
          </div>
          {/* <div className="payment-section">
            <Elements stripe={stripPromise}>
            <StripeForm />
          </Elements>
          </div> */}
          <div className="col-12">
            <button type="submit" className="btn btn-dark">
              Next
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

export default CheckoutForm;
