import React from "react";

function Trail({ name, address, length, description, profileImage }) {


    return (
        <div>
            <img id="trail-pic" src={profileImage} alt="trail-pic" />
            <h4 id="trail-name" >{name}</h4>
            <address>{address}</address>
            <p id="trail-length" >{length} miles</p>
            <p id="trail-description" >{description}</p>
        </div>
    )
}

export default Trail