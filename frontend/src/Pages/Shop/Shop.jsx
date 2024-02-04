import React, {useEffect, useState} from 'react'
import './Shop.css'
import axio from '../../Constants/axios'
import ProductRow from '../../Components/ProductRow/ProductRow'
import ErrorBoundary from '../../Components/ErrorBoundries/ErrorBoundries'

function Shop() {

    const [data, setData] = useState(null)

    useEffect (() => {
        axio.get('shop/products/').then((response) => {
            const data = response.data
            const keys = Object.entries(data)
            setData(keys)

        })
    }, [])
  return (
    <>
    <ErrorBoundary>

      {data && data.map(([category, productRow], index) => {
        return (
          <div key={index} className={`product-row bg-${category}`}>
            <ProductRow productRow={productRow} category={category} id={index} />
          </div>
        );
      })
    }
    </ErrorBoundary>
    </>
    
  );
}

export default Shop