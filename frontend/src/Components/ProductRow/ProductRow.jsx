import React, { useEffect, useState } from "react";
import "./ProductRow.css";
import ProductCard from "../ProductCard/ProductCard";
import SamplCard from '../SampleCard/SampleCard'
import axios from "../../Constants/axios";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import { Link } from 'react-router-dom'


function ProductRow(props) {
  const { productRow, category } = props;
  const [viewArrow, setViewArrow] = useState(false);
  const [isDraggable, setIsDraggable] = useState(false);
  const [subCategories, setSubCategories] = useState([])

  const categoryText = {
    men: "Upgrade Your Wardrobe, Elevate Your Style – Shop Men's Fashion Today!",
    women: "Embrace Elegance! Discover the Perfect Look in Women's Fashion",
    bags: "Carry Chic, Unveil Your Style with our Trendsetting Bags and Wallets Collection",
    shoes: "Step into Style! Explore Fashion-forward Shoes for Every Occasion!",
  };
  const getSubCategory = (category) => {
    axios.get(`shop/product-subcategory/${category}/`).then((response) => {
      setSubCategories(response.data);
    });
  };
  useEffect(() => {
    getSubCategory(category);
    if (window.innerWidth >= 900) {
      setViewArrow(true);
      setIsDraggable(false);
    } else {
      setViewArrow(false);
      setIsDraggable(true);
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
      <div className={`bg-image-shop-${category} bg-img`}>
        <h1 className={`title-text-${category} category-title`}>{categoryText[category]}</h1>
         <h5 className="category-link-title">
              <Link to={`/shop/category/${category}`} className='category-link'>{category}</Link>
            </h5>
      </div>
      <Carousel
        responsive={responsive}
        infinite={true}
        className="prod-row"
        centerMode={true}
        draggable={isDraggable}
        arrows={viewArrow}
      >
        {productRow.map((product) => {
          return <ProductCard key={product.id} product={product} />;
        })}
      </Carousel>
      <div className={`subcategory-section section-${category}`}>
        { subCategories &&
          subCategories.map((subCategory) => {
            return (<SamplCard key={subCategory.id} subCategory={subCategory} category={category} />)
          })
        }
      </div>
    </>
  );
}

export default ProductRow;
