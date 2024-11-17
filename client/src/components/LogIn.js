import React from "react";

function LogIn() {
    return (
        <>
            <h2>Log In</h2>
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
      </>
    )
}

export default LogIn;