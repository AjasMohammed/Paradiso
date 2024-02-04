import "./App.css";
import Home from "./Pages/Home/Home";
import Shop from "./Pages/Shop/Shop";
import UserAuth from "./Pages/UserAuth/UserAuth";
import NavBar from "./Components/Navbar/NavBar";
import Footer from "./Components/Footer/Footer";
import ProductView from "./Pages/ProductView/ProductView";
import Cart from "./Pages/CartItems/Cart";
import FavoriteItems from "./Pages/FavoriteItems/FavoriteItems";
import CategoryPage from "./Pages/CategoryPage/CategoryPage";
import ConformationPage from "./Pages/ConformationPage/ConformationPage";
import axios from "./Constants/axios";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { userContext, cartContext } from "./Store/Context";


function App() {
  const { user, setUser } = useContext(userContext);
  const { cartItems, setCartItems } = useContext(cartContext);
  const [refresh, setrefresh] = useState(false);

  useEffect(() => {
    const access_token = localStorage.getItem("access_token");
    console.log(access_token);
    if (access_token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;
    }
    axios.get("auth/check-user/").then((response) => {
      setUser(response.data);
      console.log(response.data);
      // localStorage.setItem("userStatus", JSON.stringify(response.data));
    });
  }, [refresh]);

  const refreshNavbar = () => {
    setrefresh(!refresh);
  };
  useEffect(() => {
    if (user === true) {
      axios.get("shop/get-cart-items/false").then((response) => {
        let context = response.data;
        if (context && "message" in context) {
          console.log(context.message);
        } else {
          const { data } = context;
          setCartItems(data);
        }
      });
    }
  }, []);

  return (
    <div className="App">
      <Router>
        <NavBar loadNav={refreshNavbar} />
        <div className="content">
          <Routes>
            <Route exact path="/" Component={Home} />
            <Route path="/auth/register" Component={UserAuth} />
            <Route path="/shop" Component={Shop} />
            <Route
              path="/shop/product-view/:id"
              element={<ProductView loadNav={refreshNavbar} />}
            />
            <Route path="/cart/" Component={Cart} />
            <Route path="/favorites/" Component={FavoriteItems} />
            <Route
              path="/shop/category/:categoryName/:subcategoryName?"
              Component={CategoryPage}
            />
            <Route path="/shop/cart/place-order" Component={ConformationPage} />
          </Routes>
        </div>

        <Footer />
      </Router>

    </div>
  );
}

export default App;
