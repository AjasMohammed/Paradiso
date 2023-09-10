import React from 'react'
import './ProductCard.css'
import { BASE_URL } from '../../Constants/config';
import { Link } from 'react-router-dom';
import TruncateText from '../TruncateText/TruncateText';


function ProductCard(props) {
    const {product} = props

     const rupeeFormatter = new Intl.NumberFormat("en-IN", {
       style: "currency",
       currency: "INR",
     });

  return (
    <>
      <Link to={"/shop/product-view/" + product.id} className="prod-link">
        <div className="card">
          <img
            src={BASE_URL + product.productimage_set[0].image}
            className="card-img-top"
            alt="..."
          />
          <div className="card-body">
            <h5 className="card-title prod-name">
              <TruncateText text={product.name} max_length={20} />
            </h5>
            <p className="card-text prod-price">
              <span className="price-tag">Price: </span>
              {rupeeFormatter.format(product.price)}
            </p>
          </div>
        </div>
      </Link>
    </>
  );
}

export default ProductCard