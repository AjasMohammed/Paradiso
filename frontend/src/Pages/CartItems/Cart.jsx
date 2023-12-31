import React, { useContext, useEffect, useState } from "react";
import "./Cart.css";
import axios from "../../Constants/axios";
import { cartContext } from "../../Store/Context";
import ProductCard from "../../Components/ProductCard/ProductCard";
import { Link } from "react-router-dom";

function Cart() {
  const { cartItems, setCartItems } = useContext(cartContext);
  const { totalAmount, setTotalAmount } = useContext(cartContext);

  useEffect(() => {
    const access = localStorage.getItem("access_token");
    axios
      .get("shop/get-cart-items/false", {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      })
      .then((response) => {
        let context = response.data;
        if ("message" in context) {
          console.log(context.message);
        } else {
          const { total, data } = context;
          setCartItems(data);
          setTotalAmount(total);
        }
      })
      .catch((e) => {
        console.log(e);
      });
  }, []);
  return (
    <div className="cart-view">
      {cartItems.length > 0 ? (
        <>
          <div className="card-items">
            {cartItems &&
              cartItems.map((item) => {
                return <ProductCard key={item.id} product={item.product} />;
              })}
          </div>
          <div className="place-order">
            <label htmlFor="" className="total-price">
              Total: ₹{totalAmount}
            </label>
            <Link to="/shop/cart/place-order">
              <button className="btn btn-outline-dark">Place Order</button>
            </Link>
          </div>
        </>
      ) : (
        <div>
          <h4>Cart is Empty</h4>
        </div>
      )}
    </div>
  );
}

export default Cart;
