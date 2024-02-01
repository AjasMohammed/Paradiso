import { createContext, useEffect, useState } from "react";
import axios from "../Constants/axios";

export const userContext = createContext(null);

function CheckUser({ children }) {
  const [user, setUser] = useState(
    localStorage.getItem("access_token") === null ? false : true
    
  );
  return (
    <userContext.Provider value={{ user, setUser }}>
      {children}
    </userContext.Provider>
  );
}

export const authContext = createContext(null);
function CheckAuth({ children }) {
  const [auth, setAuth] = useState();
  return (
    <authContext.Provider value={{ auth, setAuth }}>
      {children}
    </authContext.Provider>
  );
}

export const cartContext = createContext(null);
function CartItems({ children }) {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);

  return (
    <cartContext.Provider
      value={{ cartItems, setCartItems, totalAmount, setTotalAmount }}
    >
      {children}
    </cartContext.Provider>
  );
}

export { CheckUser, CheckAuth, CartItems };
