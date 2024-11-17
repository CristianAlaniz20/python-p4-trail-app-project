import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import LogInForm from "./LogIn";

function App() {
  return (
    <div>
      <h1>Hiking Trails</h1>
      <h2>Welcome to Hiking Trails! With us you can search for hiking trails by cities!</h2>
      <LogInForm />
    </div>
  )
}

export default App;
