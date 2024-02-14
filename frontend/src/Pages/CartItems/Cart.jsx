import React, { useContext, useEffect, useState } from "react";
import "./Cart.css";
import axios from "../../Constants/axios";
import { cartContext } from "../../Store/Context";
import { Link } from "react-router-dom";
import CheckoutCard from "../../Components/CheckoutCard/CheckoutCard";
import CheckoutForm from "../../Components/CheckoutForm/CheckoutForm";

function Cart() {
  const { cartItems, setCartItems } = useContext(cartContext);
  const { totalAmount, setTotalAmount } = useContext(cartContext);
  const [refreshCart, setRefreshCart] = useState(true);

  useEffect(() => {
    axios
      .get("shop/get-cart-items/false/")
      .then((response) => {
        let context = response.data;
        if (context !== "") {
          const { total, data } = context;
          const cart = data.cart_items;
          // setCartItems(cart);
          setTotalAmount(total);
          return cart;
        }
      })
      .then((res) => {
        let sortedCartItems = res.slice().sort((a, b) => {
          return a.id - b.id;
        });
        setCartItems(sortedCartItems);
      })
      .catch((e) => {
        console.log(e);
      });
  }, [refreshCart]);

  const refresh = () => {
    setRefreshCart(!refreshCart);
  };
  return (
    <div className="cart-view">
      {cartItems.length > 0 ? (
        <>
          <h3 className="page-title">CART ITEMS</h3>
          <div className="card-items">
            {cartItems &&
              cartItems.map((item) => {
                return (
                  <CheckoutCard
                    key={item.id}
                    product={item.product}
                    quantity={item.quantity}
                    refresh={refresh}
                  />
                );
              })}
          </div>
          <div className="place-order">
            <h2><u>Order Details</u></h2>
            <p className="sub-total">
              <span> Sub Total:</span> <span>₹{totalAmount}</span>
            </p>
            <p htmlFor="" className="delivery-fee">
              <span>Delivery Fee:</span>
              <span>
                <del>₹50</del> free
              </span>
            </p>
            <p htmlFor="" className="total-price">
              <span>Total:</span> <span>₹{totalAmount}</span>
            </p>
            <Link to="/shop/cart/confirm-order">
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
