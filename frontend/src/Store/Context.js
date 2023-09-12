import { createContext, useState } from "react";

export const userContext = createContext(null);

function CheckUser({ children }) {
  const [user, setUser] = useState(null);
  return (
    <userContext.Provider value={{ user, setUser }}>
      {children}
    </userContext.Provider>
  );
}

export const authContext = createContext(null);
function CheckAuth({ children }) {
  const [auth, setAuth] = useState();
  return (
    <authContext.Provider value={{ auth, setAuth }}>
      {children}
    </authContext.Provider>
  );
}

export { CheckUser, CheckAuth };
