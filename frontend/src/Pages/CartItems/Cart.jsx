import React, { useEffect, useState } from "react";
import "./Cart.css";
import axios from "../../Constants/axios";
import ProductCard from "../../Components/ProductCard/ProductCard";

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  useEffect(() => {
    axios.get("shop/get-cart-items/false").then((response) => {
      let data = response.data;
      if ('message' in data){
        console.log(data.message);
      }else{
        setCartItems(data);
      }
    });
  }, []);
  return (
    <div className="cart-view">
      {cartItems &&
        cartItems.map((item) => {
          return <ProductCard key={item.id} product={item.product}/>;
        })}
    </div>
  );
}

export default Cart;
