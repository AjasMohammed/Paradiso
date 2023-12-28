import React, { useRef, useState, useEffect, useContext } from "react";
import "./Register.css";
import axios from "../../Constants/axios";
import { Navigate } from "react-router-dom";
import { authContext } from "../../Store/Context";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const [isDisabled, setIsDisabled] = useState(true);
  const [authentication, setAuthentication] = useState(false);
  const { setAuth } = useContext(authContext);

  const passwordRef = useRef();

  const emailInput = (e) => {
    setEmail(e.target.value);
  };
  const passwordInput = (e) => {
    setPassword(e.target.value);
  };
  const passwordInput2 = (e) => {
    setPassword2(e.target.value);
  };

  useEffect(() => {
    if (password2 !== "" && password2 !== password) {
      passwordRef.current.classList.add("wrong-password");
      setIsDisabled(true);
    } else {
      passwordRef.current.classList.remove("wrong-password");
    }
    return () => {
      setIsDisabled(false);
    };
  }, [password, password2]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = {
      email: email,
      password: password,
    };
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.post("auth/register/", userData).then((response) => {
      console.log(response.data);
      setAuthentication(true);
      setAuth('login')
    });
  };

  return (
    <div className="auth-container">
      <h1 className="title">Sign Up</h1>
      <form action="" className="register-form" onSubmit={handleSubmit}>
        <label className="inp-label" htmlFor="">
          Email
        </label>
        <input className="register-inp" type="email" onChange={emailInput} />

        <label className="inp-label" htmlFor="">
          Password
        </label>
        <input
          className="register-inp"
          type="password"
          onChange={passwordInput}
        />
        <label className="inp-label" htmlFor="">
          Password(again)
        </label>
        <input
          ref={passwordRef}
          className="register-inp"
          type="password"
          onChange={passwordInput2}
        />

        <button
          type="submit"
          className="btn btn-outline-light sub-btn"
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
