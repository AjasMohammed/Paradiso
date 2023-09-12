import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { CheckAuth, CheckUser, CartItems } from "./Store/Context";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <CheckUser>
      <CheckAuth>
        <CartItems>
          <App />
        </CartItems>
      </CheckAuth>
    </CheckUser>
  </React.StrictMode>
);
