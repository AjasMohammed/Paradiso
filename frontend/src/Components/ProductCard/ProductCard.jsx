import React from "react";
import "./ProductCard.css";
import { BASE_URL } from "../../Constants/config";
import { Link } from "react-router-dom";

function ProductCard(props) {
  const { product } = props;

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
              src={BASE_URL + product.productimage_set[0].thumbnail}
              className="card-img-top"
              alt={product.name}
              loading="lazy"
            />
            </div>
            <div className="card-body">
              <h5 className="card-title prod-name">
                {product.name}
              </h5>
              <div className="price-tag">
              <p className="card-text current-price">
                {rupeeFormatter.format(product.current_price)}
              </p>
              <p className="card-text raw-price">
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
