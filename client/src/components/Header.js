import React from "react";

function Header() {
    const headerStyle = {
        textAlign: 'center',
    }

    return (
        <div style={headerStyle}>
            <h1>Hiking Trails</h1>
            <h2>Welcome to Hiking Trails! With us you can search for hiking trails by cities!</h2>
        </div>
    )
}

export default Header