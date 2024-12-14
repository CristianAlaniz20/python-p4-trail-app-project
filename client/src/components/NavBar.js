import React from "react";
import { Link } from "react-router-dom/cjs/react-router-dom.min";

function NavBar({ user, setUser }) {
    function handleLogoutClick() {
        // DELETE request to Logout Resource
        fetch("/logout", { method: "DELETE" })
        .then(res => {
            if (res.status === 204) setUser(null)
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
            {user.role === "admin" ? (
                <Link to="/create_trail" >
                    <button>Create Trail</button>
                </Link>
            ) : null}
            <button onClick={handleLogoutClick} >Logout</button>
        </nav>
    )
}

export default NavBar