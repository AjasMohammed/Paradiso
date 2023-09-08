import React from 'react'
import './Footer.css'

function Footer() {
  return (
    <footer>
      <div className="about col-md-6 col-sm-12">
        <h3 className="about-title">ABOUT</h3>
        <p className="about-content">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestiae
          fugit eius omnis expedita, rerum, dolor cupiditate repellendus, saepe
          quidem facilis officiis. Reiciendis fugiat nulla tenetur ab error
          molestiae, sed assumenda.
        </p>
      </div>
      <div className="socials col-md-6 col-sm-12">
        <h5>INSTAGRAM</h5>
        <h5>FACEBOOK</h5>
        <h5>TWITTER</h5>
      </div>
    </footer>
  );
}

export default Footer