import React, { useState, useEffect } from "react";
import AllTrails from "../components/AllTrails";
import ChangeAccountRole from "../components/ChangeAccountRole";
import UpdateUserPage from "./UpdateUserPage";
import DeleteUserPage from "./DeleteUserPage";
import "../styling/UserPage.css"

function UserPage({ user, setUser }) {
    const [savedTrails, setSavedTrails] = useState([])
    const [hikedTrails, setHikedTrails] = useState([])
    const [showChangeAccRole, setShowChangeAccRole] = useState(false)
    const [updateUser, setUpdateUser] = useState(false)
    const [deleteAccount, setDeleteAccount] = useState(false)

    // Fetch saved trails for User
    useEffect(() => {
        fetch("/saved_trails")
        .then(res => {
            if (res.status === 200) {
                res.json()
                .then(resSavedTrails => setSavedTrails(resSavedTrails))
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
                .then(resHikedTrails => setHikedTrails(resHikedTrails))
            }
        })
        .catch(error => console.error(error))
    }, [])

    // Handle change account role button click
    const handleChangeAccountRoleClick = () => setShowChangeAccRole(true)

    // handle update user button click
    const handleUpdateUserClick = () => setUpdateUser(true)

    // handle delete account click
    const handleDeleteAccountClick = () => setDeleteAccount(true)

    // if showChangeAccRole is true return/redirect to ChangeAccountRole component
    if (showChangeAccRole) return <ChangeAccountRole setShowChangeAccRole={setShowChangeAccRole} />

    // if updateUser is true return/redirect to UpdateUserPage
    if (updateUser) return <UpdateUserPage user={user} setUser={setUser} setUpdateUser={setUpdateUser} />

    // if deleteAccout is true return/redirect to UpdateUserPage
    if (deleteAccount) return <DeleteUserPage setDeleteAccount={setDeleteAccount} setUser={setUser} />

    return (
        <div className="user" >
            <h1 className="user-username" >Username: {user.username}</h1>
            <img className="user-profile-pic" src={user.profile_image_url} alt={`${user.username} trail-pic`} />
            <p className="user-bio" >Bio: {user.bio}</p>
            <p>Role: {user.role}</p>
            <br />

            <button onClick={handleChangeAccountRoleClick} >Change Account Role</button>
            <button onClick={handleUpdateUserClick} >Update Account</button>
            <button onClick={handleDeleteAccountClick} >Delete Account</button>

            <h2>List of Saved Trails: </h2>
            <AllTrails trails={savedTrails} />
            <br />

            <h2>List of Hiked Trails: </h2>
            <AllTrails trails={hikedTrails} />            
        </div>
    )
}

export default UserPage