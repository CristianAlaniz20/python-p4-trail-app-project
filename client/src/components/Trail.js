import React from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Trail({ id, name, address, length, description, profileImage }) {
    const history = useHistory()

    function handleClick() {
        history.push(`/trails/${id}`)
    }

    return (
        <div onClick={handleClick} >
            <img className="trail-pic" src={profileImage} alt={`${name} trail-pic`} />
            <h4 className="trail-name" >{name}</h4>
            <address className="trail-adress">{address}</address>
            <p className="trail-length" >{length} miles</p>
            <p className="trail-description" >{description}</p>
        </div>
    )
}

export default Trail