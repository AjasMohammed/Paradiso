import "./App.css";
import Home from "./Pages/Home/Home";
import Shop from "./Pages/Shop/Shop";
import UserAuth from "./Pages/UserAuth/UserAuth";
import NavBar from "./Components/Navbar/NavBar";
import Footer from "./Components/Footer/Footer";
import ProductView from "./Pages/ProductView/ProductView";
import Cart from "./Pages/CartItems/Cart";
import FavoriteItems from "./Pages/FavoriteItems/FavoriteItems";


import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import axios from "./Constants/axios";
import { useContext, useEffect } from "react";
import { userContext } from "./Store/Context";


function App() {
  const { setUser } = useContext(userContext);

  useEffect(() => {
    axios.get("auth/check-user/").then((response) => {
      setUser(response.data);
    });
  });
  return (
    <div className="App">
      <Router>
      <NavBar />
        <Routes>
          <Route exact path="/" Component={Home} />
          <Route path="/auth/register" Component={UserAuth} />
          <Route path="/shop" Component={Shop} />
          <Route path="/shop/product-view/:id" Component={ProductView} />
          <Route path="/cart/" Component={Cart} />
          <Route path="/favorites/" Component={FavoriteItems} />
        </Routes>
      <Footer />
      </Router>
    </div>
  );
}

export default App;
