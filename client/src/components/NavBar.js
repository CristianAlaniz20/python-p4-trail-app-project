import React from "react";
import { Link } from "react-router-dom/cjs/react-router-dom.min";

function NavBar({ setUser }) {
    function handleLogoutClick() {
        fetch("/logout", { method: "DELETE" })
        .then(res => {
            if (res.status === 204) {
                console.log("Successfully logged out.")
                setUser(null)
            }
        })
        .catch(error => console.error(error))
    }

    return (
        <nav>
            <button as={Link} to='/' >Home</button>
            <button as={Link} to='/user' >My Account</button>
            <button onClick={handleLogoutClick} >Logout</button>
        </nav>
    )
}

export default NavBar