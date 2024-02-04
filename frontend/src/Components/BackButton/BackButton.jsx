import React from 'react'
import './BackButton.css'
import { ArrowLeft } from "lucide-react";
import { useNavigate } from 'react-router-dom';

function BackButton() {
    const navigate = useNavigate()
    const goBack = () => {
        navigate(-1)
    }
  return (
    <>
        <a className="back-btn" onClick={goBack}>
          <ArrowLeft />
      </a>
    </>
  )
}

export default BackButton