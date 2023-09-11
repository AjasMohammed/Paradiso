import React, { useContext, useEffect, useState } from "react";
import "./ProductView.css";
import { useParams } from "react-router-dom";
import axios from "../../Constants/axios";

import { BASE_URL } from "../../Constants/config";

import { Heart } from "lucide-react";
import { userContext } from "../../Store/Context";

function ProductView() {
  const param = useParams();
  const {user} = useContext(userContext)
  
  const [product, setProduct] = useState(null);
  const [images, setImages] = useState(null);
  const [isFavorite, setIsFavorite] = useState(null);
  const [inCart, setInCart] = useState(null);

  const rupeeFormatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  });

  useEffect(() => {
    console.log(user);
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.get(`shop/product/${param.id}`).then((response) => {
      const data = response.data;
      setProduct(data);
      setImages(data.productimage_set);
    });

    if(user !== false){
          console.log(user);

          axios.get(`shop/check-in-cart/${param.id}`).then((response) => {
            setInCart(response.data);
          });

          axios.get(`shop/view-favorite?id=${param.id}`).then((response) => {
            setIsFavorite(response.data);
          });
    }
  }, []);

  const addToCart = () => {
    axios.post(`shop/add-to-cart/${param.id}`).then((response) => {
      console.log(response.data);
      setInCart(true);
    });
  };
  const removeFromCart = () => {
    axios.post(`shop/remove-from-cart/${param.id}`).then((response) => {
      console.log(response.data);
      setInCart(false);
    });
  };

  useEffect(() => {
    addToFavorite();
  }, [isFavorite]);

  const addToFavorite = () => {
    if (isFavorite === true) {
      axios
        .post(`shop/add-to-favorite/${param.id}`)

        .then((response) => console.log(response.data));
    } else if (isFavorite === false) {
      axios
        .post(`shop/remove-from-favorite/${param.id}`)

        .then((response) => console.log(response.data));
    }
  };

  return (
    <div className="container">
      {product && (
        <>
          <div className="on-top image-section col-lg-6 col-md-12 col-sm-12">
            {images.map((image) => {
              return <img key={image.id} src={BASE_URL + image.image} alt="" />;
            })}
          </div>
          <div className="detailes col-lg-6 col-md-12 col-sm-12">
            <h1 className="on-top prod-title m-3">{product.name}</h1>
            <h5 className="on-top">{rupeeFormatter.format(product.price)}</h5>

            <p className="prod-description">{product.description}</p>

            <button className="btn btn-outline-dark m-2">Buy Now</button>
            {inCart == false ? (
              <button className="btn btn-outline-dark m-2" onClick={addToCart}>
                Add to Cart
              </button>
            ) : (
              <button
                className="del-btn btn btn-outline-dark m-2"
                onClick={removeFromCart}
              >
                Remove From Cart
              </button>
            )}
            <button className="btn fav-btn m-2">
              <Heart
                className={isFavorite ? "heart-icon" : ""}
                color="black"
                onClick={() => setIsFavorite(!isFavorite)}
              />
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ProductView;
