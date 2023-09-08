import React, { useRef, useState, useEffect } from "react";
import "./LoginUser.css";
import axios from "../../Constants/axios";
import { Navigate } from "react-router-dom";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [authentication, setAuthentication] = useState(false);


  const nameInput = (e) => {
    setUsername(e.target.value);
  };

  const passwordInput = (e) => {
    setPassword(e.target.value);
  };


  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = {
      username: username,
      password: password,
    };
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.post("auth/login/", userData).then((response) => {
      console.log(response.data);
      console.log(response.status);
      setAuthentication(true);
    });
  };

  return (
    <div className="auth-container">
      <h1 className="title">Log In</h1>
      <form action="" className="register-form" onSubmit={handleSubmit}>
        <label className="inp-label" htmlFor="">User Name</label>
        <input className="register-inp" type="text" onChange={nameInput} />

        <label className="inp-label" htmlFor="">Password</label>
        <input
          className="register-inp"
          type="password"
          onChange={passwordInput}
        />

        <button
          type="submit"
          className="btn btn-outline-light sub-btn"
        >
          LogIn
        </button>
      </form>
      {authentication && (window.location.href='/')}
    </div>
  );
}

export default Register;
