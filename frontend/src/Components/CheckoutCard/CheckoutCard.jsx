import React, { useEffect, useState } from "react";
import "./CheckoutCard.css";
import { BASE_URL } from "../../Constants/config";
import { Plus, Minus, X } from "lucide-react";
import axios from "../../Constants/axios";

function CheckoutCard(props) {
  const { product, quantity, refresh } = props;
  const [qty, setQty] = useState(quantity);
  const [isDisabled, setIsDisabled] = useState(false);


  useEffect(() => {
    if (qty === 1) {
        setIsDisabled(true);
      }else{
        setIsDisabled(false);
      }
  }, [qty])
  const incrementQuantity = () => {
    axios.post(`shop/increment-quantity/${product.id}/`).then((response) => {
      setQty(response.data.quantity);
      refresh()
    });
  };
  const decrementQuantity = () => {
    axios.post(`shop/decrement-quantity/${product.id}/`).then((response) => {
      setQty(response.data.quantity);
      refresh()
      
    });
  };

  const removeFromCart = () => {
    axios
      .post(`shop/remove-from-cart/${product.id}/`)
      .then((response) => {
        refresh();
      });
  }

  const rupeeFormatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  });
  return (
    <div className="checkout-card">
      <div className="img-section">
        <img
          className="card-img"
          src={BASE_URL + product.productimage_set[0].thumbnail}
          alt=""
        />
      </div>
      <div className="detailes-section">
        <h3 className="prod-name">{product.name}</h3>
        <p className="off">{product.discount}%off</p>
        <div className="quantity-section">
          <p>Qty:</p>
          <div className="quantity">
            <button className="plus-btn" onClick={incrementQuantity}>
              <Plus className="card-icons" />
            </button>
            <p className="item-quantity">{qty}</p>
            <button
              className="minus-btn"
              onClick={decrementQuantity}
              disabled={isDisabled}
            >
              <Minus className="card-icons" />
            </button>
          </div>
        </div>
        <p className="price">{rupeeFormatter.format(product.current_price)}</p>
      </div>
      <button className="close-btn" onClick={removeFromCart}>
        <X className="card-icons" />
      </button>
    </div>
  );
}

export default CheckoutCard;
