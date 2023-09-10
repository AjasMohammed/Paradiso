import React, { useEffect, useState } from "react";
import "./ProductRow.css";
import ProductCard from "../ProductCard/ProductCard";

import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";

function ProductRow(props) {
  const { id, productRow } = props;

  const responsive = {
    superLargeDesktop: {
      breakpoint: { max: 4000, min: 1500 },
      items: 8,
    },
    desktop: {
      breakpoint: { max: 1500, min: 880 },
      items: 5,
    },
    tablet: {
      breakpoint: { max: 880, min: 520 },
      items: 4,
    },
    mobile: {
      breakpoint: { max: 520, min: 0 },
      items: 2,
    },
  };

  return (
    <Carousel responsive={responsive} infinite={true} className="prod-row" centerMode={true} draggable={false}>
      {
        productRow.map(product => {
          return <ProductCard key={product.id} product={product} />
        })
      }
    </Carousel>
   
  );
}

export default ProductRow;
