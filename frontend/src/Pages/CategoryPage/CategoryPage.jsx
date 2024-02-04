import React, { useEffect, useState } from 'react'
import "./CategoryPage.css"
import ProductCard from '../../Components/ProductCard/ProductCard'
import axios from '../../Constants/axios'
import { useParams } from 'react-router-dom'
import BackButton from '../../Components/BackButton/BackButton'


function CategoryPage() {
  const param = useParams()
  const [products, setProducts] = useState([])
  useEffect(() => {
    axios
      .get(`shop/product-category/?category=${param.categoryName}&subcategory=${param.subcategoryName}`)
      .then((response) => {
        const data = response.data;
        setProducts(data);
      });
  }, []);
  return (
    <div id='category-container' className='container'>
      <BackButton/>
      <div className="card-items">
        {products.map((product) => {
          return <ProductCard key={product.id} product={product} />;
        })}
      </div>
    </div>
  );
}

export default CategoryPage