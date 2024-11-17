import React from "react";

function SignUpForm() {
    return (
        <>
            <h2>Sign Up</h2>
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
                <label htmlFor='profile-pic'>Profile Pic Image URL: </label>
                <input
                id='profile-pic'
                name='profile-pic'
                />
                <label htmlFor='bio'>Bio: </label>
                <input
                id='bio'
                name='bio'
                />
                <br />
                <button>Sign Up</button>
        </form>
      </>
    )
}

export default SignUpForm