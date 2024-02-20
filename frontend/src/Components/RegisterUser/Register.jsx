import React, { useRef, useState, useEffect, useContext } from "react";
import "./Register.css";
import axios from "../../Constants/axios";
import { Navigate } from "react-router-dom";
import { authContext } from "../../Store/Context";

function Register() {
  const [formData, setFormData] = useState({
    email: "",
    password1: "",
    password2: "",
  });

  const [isDisabled, setIsDisabled] = useState(true);
  const [authentication, setAuthentication] = useState(false);
  const { setAuth } = useContext(authContext);

  const passwordRef = useRef();

  const handleData = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  useEffect(() => {
    if (
      formData.password2 !== "" &&
      formData.password2 !== formData.password1
    ) {
      passwordRef.current.classList.add("wrong-password");
      setIsDisabled(true);
    } else {
      passwordRef.current.classList.remove("wrong-password");
      setIsDisabled(false)
    }
    return () => {
      setIsDisabled(true);
    };
  }, [formData.password1, formData.password2]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = {
      email: formData.email,
      password: formData.password1,
    };
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.post("auth/register/", userData).then((response) => {
      setAuthentication(true);
      setAuth("login");
      console.log(response);
    });
  };

  return (
    <div className="auth-container">
      <h1 className="title">Sign Up</h1>
      <form action="" className="register-form" onSubmit={handleSubmit}>
        <label className="inp-label" htmlFor="email">
          Email
        </label>
        <input
          className="register-inp"
          type="email"
          name="email"
          onChange={handleData}
        />

        <label className="inp-label" htmlFor="">
          Password
        </label>
        <input
          className="register-inp"
          type="password"
          onChange={handleData}
          name="password1"
        />
        <label className="inp-label" htmlFor="">
          Password(again)
        </label>
        <input
          ref={passwordRef}
          className="register-inp"
          type="password"
          onChange={handleData}
          name="password2"
        />

        <button
          type="submit"
          className="btn btn-outline-dark sub-btn"
          disabled={isDisabled}
        >
          Register
        </button>
      </form>
      {authentication && <Navigate to="/login" />}
    </div>
  );
}

export default Register;
