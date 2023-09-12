import React, { useContext, useEffect, useState } from "react";
import "./Cart.css";
import axios from "../../Constants/axios";
import { cartContext } from "../../Store/Context";
import ProductCard from "../../Components/ProductCard/ProductCard";
import { Link } from "react-router-dom";


function Cart() {
  const { cartItems, setCartItems } = useContext(cartContext);
  const {totalAmount, setTotalAmount} = useContext(cartContext)

  useEffect(() => {
    axios.get("shop/get-cart-items/false").then((response) => {
      let context = response.data;
      if ("message" in context) {
        console.log(context.message);
      } else {
        const {total, data} = context
        setCartItems(data);
        setTotalAmount(total);
      }
    });
  }, []);
  return (
    <>
    <div className="card-items">
      {cartItems &&
        cartItems.map((item) => {
          return <ProductCard key={item.id} product={item.product} />;
        })}
    </div>
    <div className="place-order">
      <label htmlFor="" className="total-price">{totalAmount}</label>
      <Link to='/shop/cart/place-order'>
      <button className="btn btn-outline-dark">
        Place Order
      </button>
      </Link>
    </div>
    </>
  );
}

export default Cart;
