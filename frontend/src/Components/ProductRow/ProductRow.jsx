import React, { useEffect, useState } from "react";
import "./ProductRow.css";
import ProductCard from "../ProductCard/ProductCard";

function ProductRow(props) {
  const { id, productRow } = props;

  const [carousel, setCarousel] = useState(false)
  useEffect(() => {
    if (productRow.length > 1){
      setCarousel(true)
    }
  })

  return (
    <div>
      <div id={id} className="carousel carousel-dark slide">
        <div className="carousel-inner">
          {productRow.map((row, index) => {
            return (
              <div
                key={index}
                className={`carousel-item ${index === 0 ? "active" : ""}`}
                data-bs-interval="10000"
              >
                <div className="prod-row">
                  {row.map((product) => {
                    return <ProductCard key={product.id} product={product} />;
                  })}
                </div>
              </div>
            );
          })}
        </div>
        { carousel &&
          <>
            <button
              className="carousel-control-prev carousel-btn"
              type="button"
              data-bs-target={`#${id}`}
              data-bs-slide="prev"
            >
              <span
                className="carousel-control-prev-icon"
                aria-hidden="true"
              ></span>
              <span className="visually-hidden">Previous</span>
            </button>
            <button
              className="carousel-control-next carousel-btn"
              type="button"
              data-bs-target={`#${id}`}
              data-bs-slide="next"
            >
              <span
                className="carousel-control-next-icon"
                aria-hidden="true"
              ></span>
              <span className="visually-hidden">Next</span>
            </button>
          </>
        }
      </div>
    </div>
  );
}

export default ProductRow;
