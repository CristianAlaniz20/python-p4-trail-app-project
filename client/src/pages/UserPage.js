import React, { useState, useEffect } from "react";
import AllTrails from "../components/AllTrails";

function UserPage({ user }) {
    const [savedTrails, setSavedTrails] = useState([])
    const [hikedTrails, setHikedTrails] = useState([])

    // Fetch saved trails for User
    useEffect(() => {
        fetch("/saved_trails")
        .then(res => {
            if (res.status === 200) {
                res.json()
                .then(resSavedTrails => {
                    console.log(`resSavedTrails: ${resSavedTrails}`)
                    setSavedTrails(resSavedTrails)
                })
            }
        })
        .catch(error => console.error(error))
    }, [])

    // fetch hiked trails for User
    useEffect(() => {
        fetch("/hiked_trails")
        .then(res => {
            if (res.status === 200) {
                res.json()
                .then(resHikedTrails => {
                    console.log(`resHikedTrails: ${resHikedTrails}`)
                    setHikedTrails(resHikedTrails)
                })
            }
        })
        .catch(error => console.error(error))
    }, [])

    return (
        <div>
            <h1 id="user-username" >Username: {user.username}</h1>
            <img id="user-profile-pic" src={user.profile_image_url} alt={`${user.username} trail-pic`} />
            <p id="user-bio" >Bio: {user.bio}</p>
            <br />

            <h2>List of Saved Trails: </h2>
            <AllTrails trails={savedTrails} />
            <br />

            <h2>List of Hiked Trails: </h2>
            <AllTrails trails={hikedTrails} />            
        </div>
    )
}

export default UserPage