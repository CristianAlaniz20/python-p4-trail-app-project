import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import LogIn from "./LogIn";

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

  return (
    <div>
      <h1>Hiking Trails</h1>
      <h2>Welcome to Hiking Trails! With us you can search for hiking trails by cities!</h2>
      <LogIn onLogin={setUser}/>
    </div>
  )
}

export default App;
