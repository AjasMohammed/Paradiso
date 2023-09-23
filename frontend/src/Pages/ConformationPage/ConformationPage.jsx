import React, { useContext, useEffect, useState } from "react";
import "./ConformationPage.css";
import { cartContext } from "../../Store/Context";
import ProductCard from "../../Components/ProductCard/ProductCard";
import axios from "../../Constants/axios";

function ConformationPage() {
  const { cartItems, setCartItems, totalAmount, setTotalAmount } = useContext(cartContext);

  const [phone, setPhone] = useState(null);
  const [address, setAddress] = useState(null);
  const [city, setCity] = useState(null);
  const [zipCode, setZipCode] = useState(null);


  const handleSubmit = (e) => {
    e.preventDefault();
    const prodId = cartItems.map((item)=>{
      let data = {
        product: item.id,
        // quantity: 1
      }
      return data
    })
    console.log(prodId);
    const data = {
      products: prodId,
      phone: phone,
      address: address,
      city: city,
      zipcode: zipCode,
      amount: totalAmount
    };
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.post("shop/place-order", data).then((response) => {
      console.log(response.data);
    });
  };

  return (
    <div className="container" id="conformation">
      <div className="order-items">
        {cartItems &&
          cartItems.map((products) => {
            return <ProductCard key={products.id} product={products.product} />;
          })}
      </div>
      <div className="order-form">
        <form class="row g-3" onSubmit={handleSubmit}>
          <div class="col-md-6">
            <label for="inputPhone4" class="form-label">
              Phone Number
            </label>
            <input
              type="tel"
              class="form-control"
              id="inputPhone4"
              autocomplete="off"
              onChange={(e) => {
                setPhone(e.target.value);
              }}
            />
          </div>
          {/* <div class="col-md-6">
            <label for="inputPassword4" class="form-label">
              Password
            </label>
            <input
              type="password"
              class="form-control"
              id="inputPassword4"
              autocomplete="off"
            />
          </div> */}
          <div class="col-12">
            <label for="inputAddress" class="form-label">
              Address
            </label>
            <textarea
              type="text"
              class="form-control"
              id="inputAddress"
              autocomplete="off"
              onChange={(e) => {
                setAddress(e.target.value);
              }}
            />
          </div>
          {/* <div class="col-12">
            <label for="inputAddress2" class="form-label">
              Address 2
            </label>
            <input
              type="text"
              class="form-control"
              id="inputAddress2"
              placeholder="Apartment, studio, or floor"
              autocomplete="off"
            />
          </div> */}
          <div class="col-md-4">
            <label for="inputCity" class="form-label">
              City
            </label>
            <input
              type="text"
              class="form-control"
              id="inputCity"
              autocomplete="off"
              onChange={(e) => {
                setCity(e.target.value);
              }}
            />
          </div>
          {/* <div class="col-md-4">
            <label for="inputState" class="form-label">
              State
            </label>
            <select id="inputState" class="form-select">
              <option selected>Choose...</option>
              <option>...</option>
            </select>
          </div> */}
          <div class="col-md-3">
            <label for="inputZip" class="form-label">
              Zip
            </label>
            <input
              type="text"
              class="form-control"
              id="inputZip"
              autocomplete="off"
              onChange={(e) => {
                setZipCode(e.target.value);
              }}
            />
          </div>
          {/* <div class="col-12">
            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                id="gridCheck"
                autocomplete="off"
              />
              <label class="form-check-label" for="gridCheck">
                Check me out
              </label>
            </div>
          </div> */}
          <div class="col-12">
            <button type="submit" class="btn btn-dark">
              Place Order
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ConformationPage;
