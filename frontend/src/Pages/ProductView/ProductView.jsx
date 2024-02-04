import React, { useContext, useEffect, useState } from "react";
import "./ProductView.css";
import { useParams } from "react-router-dom";
import axios from "../../Constants/axios";
import { BASE_URL } from "../../Constants/config";
import { Heart } from "lucide-react";
import { authContext, userContext } from "../../Store/Context";
import Carousel from "react-multi-carousel";
import ProductCard from '../../Components/ProductCard/ProductCard'
import BackButton from '../../Components/BackButton/BackButton'

function ProductView(props) {
  const { loadNav } = props;

  const param = useParams();
  const { user } = useContext(userContext);
  const { setAuth } = useContext(authContext);

  const [product, setProduct] = useState(null);
  const [images, setImages] = useState({});
  const [isFavorite, setIsFavorite] = useState(null);
  const [inCart, setInCart] = useState(false);

  const [relatedProducts, setRelatedProducts] = useState([]);
  const [visibleRP, setVisibleRP] = useState(12);

  const rupeeFormatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  });

  useEffect(() => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
    setImages([])
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.get(`shop/product/${param.id}/`).then((response) => {
      const data = response.data;
      setProduct(data);
      setImages((prevVal) => ({
        ...prevVal,
        default: data.productimage_set[0].image,
      }));
      let variants = data.variants_set;
      for (let variant of variants) {
        setImages((prevVal) => ({
          ...prevVal,
          [variant.color]: variant.image,
        }));
      }
    });

    if (user !== false && user !== null) {
      axios.get(`shop/check-in-cart/${param.id}/`).then((response) => {
        setInCart(response.data);
      });

      axios.get(`shop/view-favorite?id=${param.id}/`).then((response) => {
        setIsFavorite(response.data);
      });
    }
  }, [inCart, isFavorite, param.id]);

  const addToCart = () => {
    if (user === true && user !== null) {
      axios.post(`shop/add-to-cart/${param.id}/`).then((response) => {
        setInCart(true);
        loadNav();
      });
    } else {
      setAuth("login");
      window.location.href = "/auth/register";
    }
  };

  const removeFromCart = () => {
    axios.post(`shop/remove-from-cart/${param.id}/`).then((response) => {
      setInCart(false);
      loadNav();
    });
  };
  useEffect(() => {
    if (product != null) {
      const data = {
        productId: product.id,
        category: product.category.id,
        subCategory: product.subcategory.id,
      };
      axios.get("shop/related-products/", { params: data }).then((res) => {
        setRelatedProducts(res.data)
      });
    }
  }, [product, param.id]);

  useEffect(() => {
    if (user === true) {
      addToFavorite();
    } else {
      setIsFavorite(false);
    }
  }, [isFavorite]);

  const addToFavorite = () => {
    if (isFavorite === true) {
      axios.post(`shop/add-to-favorite/${param.id}`);
    } else if (isFavorite === false) {
      axios.post(`shop/remove-from-favorite/${param.id}`);
    }
  };

const loadMoreProducts = async () => {
  setTimeout(() => {
  setVisibleRP(visibleRP + 8)
  }, 1000)

}

  const responsive = {
    superLargeDesktop: {
      breakpoint: { max: 4000, min: 1500 },
      items: 1,
    },
    desktop: {
      breakpoint: { max: 1500, min: 880 },
      items: 1,
    },
    tablet: {
      breakpoint: { max: 880, min: 520 },
      items: 1,
    },
    mobile: {
      breakpoint: { max: 520, min: 0 },
      items: 1,
    },
  };

  return (
    <div className="container" id="product-view">
      <BackButton/>
      {product && (
        <>
          {product.discount > 0 ?
            <div className="discount">{product.discount}% OFF</div>: null}
          <Carousel
            responsive={responsive}
            infinite={true}
            centerMode={false}
            draggable={false}
            className="image-section col-lg-6 col-md-12 col-sm-12"
          >
            {Object.entries(images).map(([color, image]) => {
              return <img key={color} src={BASE_URL + image} alt={color} />;
            })}
          </Carousel>
          <div className="detailes col-lg-6 col-md-12 col-sm-12">
            <h3 className="on-top prod-title mt-3 mb-3">{product.name}</h3>
            <div className="on-top">
              <h5 className="current-price price">
                {rupeeFormatter.format(product.current_price)}
              </h5>
              <h5 className="raw-price price">
                <del>{rupeeFormatter.format(product.raw_price)}</del>
              </h5>
            </div>

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
      <section className="recommendation-section">
        <h2 className="related-products-title">Related Products</h2>
              <div className="related-products">
              {
                relatedProducts.slice(0, visibleRP).map((product) => {
                 return <ProductCard key={product.id} product={product} />
                })
              }
              </div>
              {
                relatedProducts.length > visibleRP ? 
              <button className="load-more btn btn-dark" onClick={loadMoreProducts}>Load More</button>
              : null
              }
      </section>
    </div>
  );
}

export default ProductView;
