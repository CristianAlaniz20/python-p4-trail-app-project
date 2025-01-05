import React, { useEffect, useState, useContext } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import LogIn from "../pages/LogIn";
import NavBar from "./NavBar";
import Header from "./Header";
import Home from "../pages/Home";
import TrailPage from "../pages/TrailPage"
import ReviewForm from "./ReviewForm";
import UserPage from "../pages/UserPage";
import CreateTrailPage from "../pages/CreateTrailPage";
import UpdateUserPage from "../pages/UpdateUserPage";
import ResponseMessage from "./ResponseMessage";
import { ResponseMessageContext }from "./ResponseMessageProvider";

function App() {
  const [user, setUser] = useState(null)
  const {message, statusCode} = useContext(ResponseMessageContext)

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

  // Check if user state has a value and return LogIn component if doesn't
  if (!user) {
    return <LogIn onLogin={setUser}/>
  }

  return (
    <Router>
      <div>
        {/* Routes for different pages of the Application */}
        <Header />
        <NavBar user={user} setUser={setUser} />
        {message && statusCode ? <ResponseMessage /> : null}
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/trails/:trail_id" component={TrailPage} />
          <Route path="/reviews/:trail_id" component={ReviewForm} />
          <Route path="/user" >
            <UserPage user={user} setUser={setUser} />
          </Route>
          {user.role === "admin" ? (
            <Route path="/create_trail" component={CreateTrailPage} />
          ) : null}
          <Route path="/edit_user" component={UpdateUserPage} />
        </Switch>
      </div>
    </Router>
  )
}

export default App;
