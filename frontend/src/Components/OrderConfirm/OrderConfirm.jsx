import React, { useEffect, useState } from "react";
import "./OrderConfirm.css";
import axios from "../../Constants/axios";

function OrderConfirm({ orderId }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get(`shop/confirm-order/${orderId}/`).then((response) => {
      console.log(response.data);
      setData(response.data);
    });
  }, []);
  return (
    <div id="invoice-container">
      <div className="invoice-header">
        <h1><u>Order Details</u></h1>
      </div>
      {data && (
        <div id="invoice">
          <div id="invoice-details">
            <p>
              <span>Order ID</span> <span className="values">{data.id}</span>
            </p>
            <p>
              <span>Status</span> <span className="values" style={{textTransform: 'uppercase'}}>{data.status}</span>
            </p>
            <p>
              <span>Amount</span> <span className="values">₹{data.amount}</span>
            </p>

            <p>
              <span>City</span> <span className="values">{data.city}</span>
            </p>
            <p>
              <span>Zipcode</span>
              <span className="values">{data.zipcode}</span>
            </p>
            <p>
              <span>Phone</span> <span className="values">{data.phone}</span>
            </p>
            <p>
              <span>Address</span>
              <span className="values">{data.address}</span>
            </p>
          </div>
          <table id="invoice-items">
            <thead>
              <tr>
                <th>Products</th>
                <th>Quantity</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              {/* Loop through order items here Example */}
              {data.products.map((item, index) => (
                <tr key={index}>
                  <td className="products-name">{item.product.name}</td>
                  <td>{item.quantity}</td>
                  <td>{item.product.current_price}</td>
                </tr>
              ))}
              <tr id="total">
                <td></td>
                <th>Total: </th>
                <th>{data.amount}</th>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default OrderConfirm;
