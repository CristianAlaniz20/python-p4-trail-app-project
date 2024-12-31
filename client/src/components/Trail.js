import React, { useContext, useState } from "react";
import { useHistory, useLocation, useParams } from "react-router-dom/cjs/react-router-dom.min";
import { ResponseMessageContext } from "./ResponseMessageProvider";

function Trail({ id, name, address, length, description, profileImage }) {
    const history = useHistory()
    const { handleResponse } = useContext(ResponseMessageContext)
    // for conditional JSX rendering
    const location = useLocation()
    const { trail_id } = useParams()
    // for condtional rendering of save and hike button 
    const [userTrail, setUserTrail] = useState(null)

    // Re route to Trail Page
    const handleViewTrailPageClick = () => history.push(`/trails/${id}`)

    // Handle Saving Trail 
    function handleSaveTrailClick() {
        const trailIdObject = { id: id }
        // POST request to SavedTrailsbyUserId resource
        fetch("/saved_trails", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(trailIdObject, null, 2),
        })
        .then(res => handleResponse(res))
        .catch(error => console.error(error))
    }

    // Handle setting trail hiked value to True
    function handleHikedTrailClick() {
        const trailIdObject = { id: id }
        // POST request to HikedTrailsbyUserId resource
        fetch("/hiked_trails", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(trailIdObject, null, 2),
        })
        .then(res => handleResponse(res))
        .catch(error => console.error(error))
    }

    return (
        <>
            <div>
                <img className="trail-pic" src={profileImage} alt={`${name} trail-pic`} />
                <h4 className="trail-name" >{name}</h4>
                {location.pathname === "/user" ? null : (
                    <>
                        <address className="trail-adress">{address}</address>
                        <p className="trail-length" >{length} miles</p>
                        <p className="trail-description" >{description}</p>
                    </>
                )}
            </div>
            {/* condtional JSX rendering based on current path */}
            {trail_id ? null : <button onClick={handleViewTrailPageClick} >View Trail Page</button>}
            { location.pathname === "/user" ? null : <button onClick={handleSaveTrailClick} >Save Trail</button>}
            { location.pathname === "/user" ? null : <button onClick={handleHikedTrailClick} >Mark as Hiked</button>}
        </>
    )
}

export default Trail