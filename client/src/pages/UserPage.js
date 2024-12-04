import React from "react";

function UserPage({ user }) {
    return (
        <div>
            <h1 id="user-username" >Username: {user.username}</h1>
            <img id="user-profile-pic" src={user.profile_image_url} alt={`${user.username} trail-pic`} />
            <p id="user-bio" >Bio: {user.bio}</p>
        </div>
    )
}

export default UserPage