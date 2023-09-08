import React, { useContext } from "react";
import "./UserAuth.css";
import Register from "../../Components/RegisterUser/Register";
import LoginUser from "../../Components/LoginUser/LoginUser";
import { authContext } from "../../Store/Context";

function UserAuth() {
  const { auth } = useContext(authContext);

  let component = null;

  if (auth === "signup") {
   component = <Register />;
  }else{
    component = <LoginUser />;
  }
  return <div className="auth container">{component}</div>;
}

export default UserAuth;
