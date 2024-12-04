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
            <Link to="/">
                <button>Home</button>
            </Link>
            <Link to='/user' >
                <button>My Account</button>
            </Link>
            <button onClick={handleLogoutClick} >Logout</button>
        </nav>
    )
}

export default NavBar