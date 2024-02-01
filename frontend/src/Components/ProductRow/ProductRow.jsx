import React, { useEffect, useState } from "react";
import "./ProductRow.css";
import ProductCard from "../ProductCard/ProductCard";

import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";

function ProductRow(props) {
  const { productRow } = props;
  const [row1, setRow1] = useState([]);
  const [row2, setRow2] = useState([]);
  const [viewArrow, setViewArrow] = useState(false);
  const [isDraggable, setIsDraggable] = useState(false);

  const splitRow = (row) => {
    let midpoint = Math.ceil(row.length / 2);

    setRow1(row.slice(0, midpoint));
    setRow2(row.slice(midpoint));
  };
  useEffect(() => {
    splitRow(productRow);
  }, [productRow]);
  useEffect(() => {
    if (window.innerWidth >= 900) {
      setViewArrow(true);
      setIsDraggable(false)
    } else {
      setViewArrow(false);
      setIsDraggable(true)
    }
  }, []);

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
    <>
      <Carousel
        responsive={responsive}
        infinite={true}
        className="prod-row"
        centerMode={true}
        draggable={false}
        arrows={viewArrow}
      >
        {row1.map((product) => {
          return <ProductCard key={product.id} product={product} />;
        })}
      </Carousel>
      <Carousel
        responsive={responsive}
        infinite={true}
        className="prod-row"
        centerMode={true}
        draggable={false}
        arrows={viewArrow}
      >
        {row2.map((product) => {
          return <ProductCard key={product.id} product={product} />;
        })}
      </Carousel>
    </>
  );
}

export default ProductRow;
