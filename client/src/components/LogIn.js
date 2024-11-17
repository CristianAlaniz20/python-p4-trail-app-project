import React from "react";

function LogIn() {
    return (
        <form>
            <label for='username'>Username: </label>
            <input
            id='username' 
            name='username' 
            />
            <br />
            <label for='password'>Password: </label>
            <input
            id='password'
            name='password'
            />
      </form>
    )
}

export default LogIn;