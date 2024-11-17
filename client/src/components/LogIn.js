import React from "react";

function LogIn() {
    return (
        <form>
            <label htmlFor='username'>Username: </label>
            <input
            id='username' 
            name='username' 
            />
            <br />
            <label htmlFor='password'>Password: </label>
            <input
            id='password'
            name='password'
            />
            <br />
            <button>Log In</button>
      </form>
    )
}

export default LogIn;