import React, { useEffect, useState } from 'react'
import "./CategoryPage.css"
import ProductCard from '../../Components/ProductCard/ProductCard'
import axios from '../../Constants/axios'
import { useParams } from 'react-router-dom'

function CategoryPage() {
  const param = useParams()
  const [products, setProducts] = useState([])
  useEffect(() => {
    axios
      .get(`shop/product-category?category=${param.categoryName}`)
      .then((response) => {
        const data = response.data;
        setProducts(data);
      });
  }, []);
  return (
    <>
      <h1 className="category-page category-title">{param.categoryName}</h1>
      <div className="card-items">
        {products.map((product) => {
          return <ProductCard key={product.id} product={product} />;
        })}
      </div>
    </>
  );
}

export default CategoryPage