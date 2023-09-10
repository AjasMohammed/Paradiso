import React, { useEffect, useState } from 'react'
import './FavoriteItems.css'
import axios from '../../Constants/axios'
import ProductCard from '../../Components/ProductCard/ProductCard'


function FavoriteItems() {
    const [products, setProducts] = useState([])
    useEffect(() => {
        axios.get('shop/view-favorite').then((response) => {
        let data = response.data
            const {products} = data
            console.log(products);
            setProducts(products)
        })
    },[])
  return (
    <div className="card-items">
      {products.map((product) => {
        return <ProductCard key={product.id} product={product} />;
      })}
    </div>
  );
}

export default FavoriteItems