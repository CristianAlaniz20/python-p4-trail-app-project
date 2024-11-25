import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import LogIn from "../pages/LogIn";
import AllTrails from "./AllTrails";
import Header from "./Header";

function App() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    // auto-login
    fetch("/check_session")
    .then((res) => {
      if (res.status === 200) {
        res.json()
        .then((resUser) => setUser(resUser));
      }
    })
    .catch(error => console.error(error))
  }, []);

  if (!user) {
    return (
      <div>
        <LogIn onLogin={setUser}/>
      </div>
    )
  }

  return (
    <div>
      <Header />
      <AllTrails />
    </div>
  )
}

export default App;
