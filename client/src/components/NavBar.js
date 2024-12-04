import React from "react";
import { Link } from "react-router-dom/cjs/react-router-dom.min";

function NavBar() {
    return (
        <nav>
            <button>Home</button>
            <button>My Account</button>
            <button>Logout</button>
        </nav>
    )
}

export default NavBar