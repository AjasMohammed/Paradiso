import React from "react";
import "./ProductCard.css";
import { BASE_URL } from "../../Constants/config";
import { Link } from "react-router-dom";
import TruncateText from "../TruncateText/TruncateText";

function ProductCard(props) {
  const { product } = props;
  console.log(product.productimage_set[0].thumbnail);

  const rupeeFormatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  });

  return (
    <>
      {product.productimage_set[0] && product.productimage_set[0].image ? (
        <Link to={"/shop/product-view/" + product.id} className="prod-link">
          <div className="card">
            <div className="card-image">
            <img
              src={BASE_URL + product.productimage_set[0].image}
              className="card-img-top"
              alt={product.name}
            />
            </div>
            <div className="card-body">
              <h5 className="card-title prod-name">
                {/* <TruncateText text={product.name} max_length={20} /> */}
                {product.name}
              </h5>
              <div className="price-tag">
              <p className="card-text current-price">
                {/* <span className="price-tag">Price: </span> */}
                {rupeeFormatter.format(product.current_price)}
              </p>
              <p className="card-text raw-price">
                {/* <span className="price-tag">Price: </span> */}
                <del>{rupeeFormatter.format(product.raw_price)}</del>
              </p>
              </div>
            </div>
          </div>
        </Link>
      ) : null}
    </>
  );
}

export default ProductCard;
