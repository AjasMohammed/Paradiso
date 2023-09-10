import React from 'react'
import "./SampleCard.css"
import { BASE_URL } from "../../Constants/config";

function SampleCard(props) {
    const {image} = props
  return (
    <div className='sample-card'>
        <img src={ BASE_URL + image} alt="" className="prod-img" />
    </div>
  )
}

export default SampleCard