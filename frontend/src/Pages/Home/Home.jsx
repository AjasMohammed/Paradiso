import React, { useEffect, useState } from "react";
import "./Home.css";
import axios from "../../Constants/axios";
import SampleCard from "../../Components/SampleCard/SampleCard";

function Home() {
  const [imageArr, setImageArr] = useState([]);
  const [currentPair, setCurrentPair] = useState(0);

  const swapPair = () => {
    setCurrentPair((prevPair) => {
      let newPair = 0;
      if (prevPair < imageArr.length - 1) {
        newPair = prevPair + 1;
      }
      return newPair;
    });
  };
  useEffect(() => {
    axios.get("shop/sample-images").then((response) => {
      const data = response.data;
       setImageArr(data);
    })
     
  }, []);
 
  useEffect(() => {
    let intervalId
     if (imageArr.length > 0) {
         intervalId = setInterval(swapPair, 10000);
      } 
      return () => clearInterval(intervalId)   
  }, [imageArr])

  return (
    <div id="home">
      <div className="bg-image">
        <div className="blur-area"></div>
        <h1 className="intro">Welcome To Paradiso</h1>
        <h4 className="intro">We Have the Best Deals for You...</h4>
        <div className="sample-products">
          {imageArr.length !== 0 &&
            imageArr[currentPair].map((item) => {
              return <SampleCard key={item.id} image={item.image} />;
            })}
        </div>
      </div>
    </div>
  );
}

export default Home;
