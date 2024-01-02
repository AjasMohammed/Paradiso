import React, { useState } from "react";
import "./LoginUser.css";
import axios from "../../Constants/axios";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [authentication, setAuthentication] = useState(false);

  const emailInput = (e) => {
    setEmail(e.target.value);
  };

  const passwordInput = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = {
      email: email,
      password: password,
    };
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios
      .post("auth/login/", userData)
      .then((response) => {
        const data = response.data;
        localStorage.setItem("access_token", data.access_token);
        setAuthentication(true);
      })
      .catch((error) => {
        alert("Login failed. Please check your credentials.");
      });
  };

  return (
    <div className="auth-container">
      <h1 className="title">Log In</h1>
      <form action="" className="register-form" onSubmit={handleSubmit}>
        <label className="inp-label" htmlFor="">
          Email
        </label>
        <input className="register-inp" type="text" onChange={emailInput} />

        <label className="inp-label" htmlFor="">
          Password
        </label>
        <input
          className="register-inp"
          type="password"
          onChange={passwordInput}
        />

        <button type="submit" className="btn btn-outline-light sub-btn">
          LogIn
        </button>
      </form>
      {authentication && (window.location.href = "/")}
    </div>
  );
}

export default Register;
