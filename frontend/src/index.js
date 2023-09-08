import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { CheckAuth, CheckUser } from "./Store/Context";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <CheckUser>
      <CheckAuth>
        <App />
      </CheckAuth>
    </CheckUser>
  </React.StrictMode>
);
