import React, {useEffect, useState} from 'react'
import './Shop.css'
import axio from '../../Constants/axios'
import ProductRow from '../../Components/ProductRow/ProductRow'
import { Link } from 'react-router-dom'

function Shop() {

    const [data, setData] = useState(null)

    useEffect (() => {
        axio.get('shop/products').then((response) => {
            const data = response.data
            const keys = Object.entries(data)
            setData(keys)

        })
    }, [])
  return (
    <>
      {data && data.map(([category, productRow], index) => {
        return (
          <div key={index} className="product-row">
            <h1 className="category-title line-effect">
              <Link to={'#'} className='category-link'>{category}</Link>
            </h1>
            <ProductRow productRow={productRow[0]} id={index} />
          </div>
        );
      })
        }
    </>
    
  );
}

export default Shop