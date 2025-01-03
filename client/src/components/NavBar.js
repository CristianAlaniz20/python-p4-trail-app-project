import React, { useContext } from "react";
import { Link } from "react-router-dom/cjs/react-router-dom.min";
import { ResponseMessageContext } from "./ResponseMessageProvider";

function NavBar({ user, setUser }) {
    const { handleResponse } = useContext(ResponseMessageContext)

    function handleLogoutClick() {
        // DELETE request to Logout Resource
        fetch("/logout", { method: "DELETE" })
        .then(res => handleResponse(res, () => setUser(null)))
        .catch(error => console.error(error))
    }

    // NavBar CSS styling
    const NavBarStyling = {
        display: 'flex',
        justifyContent: 'space-between',
        width: '100%',
    }

    return (
        <nav style={NavBarStyling}>
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