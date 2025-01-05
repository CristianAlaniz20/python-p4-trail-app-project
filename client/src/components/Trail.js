import React, { useContext, useState, useEffect } from "react";
import { useHistory, useLocation, useParams } from "react-router-dom/cjs/react-router-dom.min";
import { ResponseMessageContext } from "./ResponseMessageProvider";
import "../styling/Trail.css"

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
        .then(res => {
            userTrail.is_saved = true
            handleResponse(res)
        })
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
        .then(res => {
            userTrail.is_hiked = true
            handleResponse(res)
        })
        .catch(error => console.error(error))
    }

    // Effect hook to retrieve a userTrail from db using trail id
    useEffect(() => {
        // GET request to EditUserTrail resource 
        fetch(`/user_trail/${id}`)
        .then(res => {
            if (res.status === 200) {
                res.json()
                .then(resUserTrail => {
                    setUserTrail(resUserTrail)
                })
            }
        })
        .catch(error => console.error(error))
    }, [id])

    // handle Unsave Trail button click
    function handleUnsaveTrailClick() {
        userTrail.is_saved = false
        updateUserTrail()
    }

    // handle Mark As Not Hiked button click
    function handleMarkAsNotHikedClick() {
        userTrail.is_hiked = false
        updateUserTrail()
    }

    function updateUserTrail() {
        // PUT request to EditUserTrail resource
        fetch(`/user_trail/${id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(userTrail, null, 2),
        })
        .then(res => handleResponse(res))
        .catch(error => console.error(error))
    }
    

    return (
        <div className="trail" >
            <>
                <img className="trail-pic" src={profileImage} alt={`${name} trail-pic`} />
                <h4 className="trail-name" >{name}</h4>
                {location.pathname === "/user" ? null : (
                    <>
                        <address className="trail-adress">{address}</address>
                        <p className="trail-length" >{length} miles</p>
                        <p className="trail-description" >{description}</p>
                    </>
                )}
            </>
            {/* condtional JSX rendering based on current path */}
            {trail_id ? null : <button onClick={handleViewTrailPageClick} >View Trail Page</button>}
            { userTrail && userTrail.is_saved ? <button onClick={handleUnsaveTrailClick} >Unsave Trail</button> : <button onClick={handleSaveTrailClick} >Save Trail</button>}
            { userTrail && userTrail.is_hiked ? <button onClick={handleMarkAsNotHikedClick} >Mark as not Hiked</button> : <button onClick={handleHikedTrailClick} >Mark as Hiked</button>}
        </div>
    )
}

export default Trail