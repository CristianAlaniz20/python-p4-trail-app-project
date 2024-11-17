import React from "react";

function SignUp() {
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
            <label for='profile-pic'>Profile Pic Image URL: </label>
            <input
            id='profile-pic'
            name='profile-pic'
            />
            <label for='bio'>Bio: </label>
            <input
            id='bio'
            name='bio'
            />
      </form>
    )
}

export default SignUp