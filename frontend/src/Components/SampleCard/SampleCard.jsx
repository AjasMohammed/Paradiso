import React, { useEffect, useState } from "react";
import "./SampleCard.css";
import { BASE_URL } from "../../Constants/config";
import { Link } from 'react-router-dom'


function SampleCard(props) {
  const [image, setImage] = useState(null);
  const { subCategory, category } = props;
  useEffect(() => {
    if (category == "women" && subCategory.image_secondary != null) {
      setImage(subCategory.image_secondary);
    } else {
      setImage(subCategory.image_primary);
    }
  }, []);
  return (
    <Link
    to={`/shop/category/${category}/${subCategory.name}`}
    className="sample-card">
      <div className="second-layer"></div>
      <h3 className="subcategory-title">{subCategory.name}</h3>
      {image && (
        <img
          src={BASE_URL + image}
          alt={subCategory.name}
          className="card-img"
          loading="lazy"
        />
      )}
    </Link>
  );
}

export default SampleCard;
