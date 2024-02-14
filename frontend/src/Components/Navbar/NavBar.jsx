import React, { useState, useRef, useContext, useEffect } from "react";
import "./NavBar.css";
import { userContext, authContext } from "../../Store/Context";
import { NavLink, Link } from "react-router-dom";
import axios from "../../Constants/axios";

import { ShoppingCart, UserCircle, Heart } from "lucide-react";
import { Tooltip } from "react-tooltip";
import SearchField from "./SearchField/SearchField";

function NavBar(props) {
  const { loadNav } = props;

  const [hambtn, setHambtn] = useState(false);
  const [cartItemsCount, setCartItemsCount] = useState(0);
  const [loggedOut, setLoggedOut] = useState(false);

  const expandMenu = useRef(null);
  const expandMid = useRef(null);
  const hamBtn = useRef(null);

  const { user, setUser } = useContext(userContext);
  const { setAuth } = useContext(authContext);

  const expand = () => {
    setHambtn(!hambtn);
    const win = window.innerWidth;
    if (hambtn === true) {
      if (win <= 800) {
        expandMid.current.classList.add("expand");
      } else {
        expandMenu.current.classList.add("expand");
      }
      hamBtn.current.classList.add("close-btn");
    } else {
      expandMenu.current.classList.remove("expand");
      expandMid.current.classList.remove("expand");
      hamBtn.current.classList.remove("close-btn");
    }
  };

  const handleClick = (e) => {
    const btnClicked = e.target.text.toLowerCase();
    setAuth(btnClicked);
  };

  useEffect(() => {
    console.log(user);
    if (user == true) {
      axios.get("shop/get-cart-items/true/").then((response) => {
        let data = response.data;
        const { count } = data;
        setCartItemsCount(count);
      });
    }
  });

  const logOut = () => {
    localStorage.removeItem("userStatus");
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios
      .post("auth/logout/")
      .then((response) => {
        localStorage.removeItem("access_token");
        axios.defaults.headers.common["Authorization"] = null;
        setLoggedOut(!loggedOut);
        setUser(false);
        loadNav();
        window.location.href = "/";
      })
      .catch((e) => {
        if (e.response.status == 400) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("userStatus");
          setLoggedOut(!loggedOut);
          setUser(false);
          loadNav();
          window.location.href = "/";
        } else {
          alert("Somthing went wrong!");
        }
      });
  };



  return (
    <>
      <nav>
        <div className="hamburger-btn" ref={hamBtn} onClick={expand}>
          <span className="line"></span>
          <span className="line"></span>
          <span className="line"></span>
        </div>
        <div className="logo">
          <h3>Paradiso</h3>
        </div>
        <div className="mid" ref={expandMid}>
          <div className="menu" ref={expandMenu}>
            <ul>
              <li className="line-effect">
                <NavLink to="/">HOME</NavLink>
              </li>
              <li className="line-effect">
                <NavLink to="/shop">SHOP</NavLink>
              </li>
              <li className="line-effect">
                <NavLink to="/contact">CONTACT</NavLink>
              </li>
              <li className="line-effect">
                <NavLink to="/about">ABOUT</NavLink>
              </li>
            </ul>
          </div>

          <div className="form-area">
            <SearchField/>
          </div>
        </div>

        {user == true ? (
          <div className="profile">
            <div className="wish-list">
              <Link to="/favorites/">
                <Heart />
              </Link>
            </div>
            <div className="cart">
              <Link to="/cart/">
                {cartItemsCount > 0 ? (
                  <span className="cart-items">{cartItemsCount}</span>
                ) : null}
                <ShoppingCart />
              </Link>
            </div>
            <div className="profile-info">
              <button data-tooltip-id="profile-btn" className="profile-btn">
                <UserCircle size={30} strokeWidth={1.5} />
              </button>
              <Tooltip
                className="profile-tooltip"
                clickable
                id="profile-btn"
                openOnClick
                content={
                  <button className="btn btn-dark" onClick={logOut}>
                    Logout
                  </button>
                }
              />
            </div>
          </div>
        ) : (
          <div className="auth-btn profile">
            <button className="btn btn-dark">
              <Link
                to="/auth/register"
                className="auth-user-btn"
                onClick={handleClick}
              >
                SignUp
              </Link>
            </button>
            <button className="btn btn-dark">
              <Link
                to="/auth/register"
                className="auth-user-btn"
                onClick={handleClick}
              >
                LogIn
              </Link>
            </button>
          </div>
        )}
      </nav>
    </>
  );
}

export default NavBar;
